import time
from datetime import datetime
from zoneinfo import ZoneInfo

from ssi_fctrading import FCTradingClient
from ssi_fctrading.models import fcmodel_requests
import fc_config  # chỉnh lại import nếu fc_config ở package khác

# Nếu bạn đang dùng ssi_fc_data để lấy giá
from ssi_fc_data import fc_md_client
from ssi_fc_data import fc_md_model as md_model  # tên module có thể khác, bạn chỉnh theo project của bạn


from ..utils.dataAPI import get_data
from ..utils.tradingAPI.trading_api import TradingAPI

# =========================
# 1. HÀM LẤY GIÁ HIỆN TẠI
# =========================
price = get_data.get_current_price()


# def get_current_price(symbol: str) -> float:
#     """
#     Lấy giá hiện tại (Close mới nhất trong ngày) của mã phái sinh.
#     Dùng intraday_ohlc giống code bạn đã dùng trước đó.
#     """
#     # config cho MarketDataClient - thay bằng config Loader của bạn
#     # Ở đây giả sử bạn đã có hàm load_config() trả về object config
#     from config_loader import load_config   # nếu bạn dùng module này
#     md_config = load_config()

#     md_client = fc_md_client.MarketDataClient(md_config)

#     today = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).strftime("%d/%m/%Y")

#     # Ví dụ lấy intraday OHLC trong hôm nay, limit 100 dòng
#     response = md_client.intraday_ohlc(
#         md_config,
#         md_model.intraday_ohlc(symbol, today, today, 1, 100)
#     )
#     data = response.get("data", [])
#     if not data:
#         raise RuntimeError(f"Không lấy được dữ liệu giá cho {symbol}: {response}")

#     # Lấy record có Time mới nhất
#     latest = max(data, key=lambda x: x["Time"])
#     price = float(latest["Close"])
#     print(f"[MarketData] Latest {symbol} {latest['TradingDate']} {latest['Time']} Close={price}")
#     return price


# =========================
# 2. HÀM VERIFY OTP / PIN
# =========================
# def verify_twofa_if_needed(client: FCTradingClient):
#     """
#     Tùy theo TwoFAType trong fc_config:
#     - Nếu SMS/EMAIL: gọi get_otp, rồi yêu cầu user nhập OTP và gọi verifyCode
#     - Nếu PIN: yêu cầu nhập PIN và verifyCode
#     Bạn chỉ cần verify 1 lần trước khi chạy bot.
#     """
#     two_fa = getattr(fc_config, "TwoFAType", "").upper()
#     print(f"TwoFAType trong config: {two_fa}")

#     if two_fa in ("SMS", "EMAIL"):
#         # Gửi request nhận OTP
#         from ssi_fctrading.models import fcmodel_requests as tr_model
#         req = tr_model.GetOTP(fc_config.ConsumerID, fc_config.ConsumerSecret)
#         res = client.get_otp(req)
#         print("Response get_otp:", res)
#         otp = input("Nhập OTP (SMS/Email) để verify: ").strip()
#         print("verifyCode result:", client.verifyCode(otp))

#     elif two_fa == "PIN":
#         pin = input("Nhập PIN giao dịch: ").strip()
#         print("verifyCode result:", client.verifyCode(pin))

#     else:
#         print("TwoFAType không phải SMS/EMAIL/PIN hoặc không cần verify thêm.")


# =========================
# 3. ĐẶT LỆNH BAN ĐẦU
# =========================
def place_initial_order(
    # client: FCTradingClient,
    # account: str,
    symbol: str,
    # market: str,
    side: str,
    # quantity: int,
) -> dict:
    # Lấy giá hiện tại
    current_price = get_data.get_current_price(symbol)

    # Tạo request NewOrder
    req = TradingAPI.new_order(side, current_price)

    # order_ref = datetime.now().strftime("%H%M%S%f")  # refId bất kỳ
    # req = fcmodel_requests.NewOrder(
    #     str(account).upper(),
    #     order_ref,
    #     str(symbol).upper(),
    #     str(market).upper(),      # 'VNFE' cho phái sinh
    #     str(side).upper(),        # 'B' hoặc 'S'
    #     "LO",                     # Loại lệnh, ví dụ: 'LO' - bạn chỉnh theo SSI
    #     float(current_price),     # Giá hiện tại
    #     int(quantity),
    #     False,                    # stopOrder = False (đây là lệnh thường)
    #     0.0,                      # stopPrice
    #     "",                       # stopType
    #     0.0, 0.0, 0.0             # stopStep, lossStep, profitStep
    # )

    print(f"[Trading] Đặt lệnh {side} {quantity} {symbol} @ {current_price}")
    res = client.der_new_order(req)
    print("[Trading] Response new_order:", res)

    # Tùy format res (JSON string/ dict) bạn parse ra orderID
    # Ở đây giả sử res là dict hoặc JSON parseable
    if isinstance(res, str):
        import json
        res_json = json.loads(res)
    else:
        res_json = res

    order_id = res_json.get("orderId") or res_json.get("OrderId") or ""
    print(f"[Trading] Created orderId: {order_id}")

    return {
        "order_id": order_id,
        "entry_price": current_price,
        "side": side.upper(),
        "symbol": symbol.upper(),
        "quantity": quantity,
        "market": market.upper(),
    }


# =========================
# 4. HÀM MONITOR STOPLOSS
# =========================
def monitor_stoploss_and_hedge(
    client: FCTradingClient,
    account: str,
    position_info: dict,
    stop_loss: float,
    poll_interval_sec: int = 2,
):
    """
    Vòng lặp:
    - Liên tục lấy giá hiện tại.
    - Nếu:
        + Lệnh gốc là BUY: giá <= stop_loss --> đặt SELL cùng khối lượng
        + Lệnh gốc là SELL: giá >= stop_loss --> đặt BUY cùng khối lượng
    Sau khi đặt lệnh ngược để cắt lỗ thì dừng.
    """
    side = position_info["side"]
    symbol = position_info["symbol"]
    quantity = position_info["quantity"]
    market = position_info["market"]

    print(f"[StopLoss] Bắt đầu monitor {symbol}, side={side}, stopLoss={stop_loss}")

    while True:
        try:
            price = get_data.get_current_price(symbol)
        except Exception as e:
            print("[StopLoss] Lỗi lấy giá:", e)
            time.sleep(poll_interval_sec)
            continue

        # Điều kiện kích hoạt stop loss theo hướng vị thế
        trigger = False
        if side == "B" and price <= stop_loss:
            trigger = True
        elif side == "S" and price >= stop_loss:
            trigger = True

        print(f"[StopLoss] Giá hiện tại: {price} | trigger = {trigger}")

        if trigger:
            # Đặt lệnh ngược lại
            hedge_side = "S" if side == "B" else "B"
            order_ref = datetime.now().strftime("%H%M%S%f")
            req = fcmodel_requests.NewOrder(
                str(account).upper(),
                order_ref,
                str(symbol).upper(),
                str(market).upper(),
                hedge_side,
                "LO",
                float(price),
                int(quantity),
                False,
                0.0,
                "",
                0.0,
                0.0,
                0.0,
            )
            print(f"[StopLoss] Kích hoạt! Đặt lệnh {hedge_side} {quantity} {symbol} @ {price}")
            res = client.der_new_order(req)
            print("[StopLoss] Response hedge order:", res)
            print("[StopLoss] Dừng monitor (đã cắt lỗ xong).")
            break

        time.sleep(poll_interval_sec)


# =========================
# 5. MAIN
# =========================
def main():
    # ===== CẤU HÌNH CƠ BẢN =====
    symbol = "VN30F1M"       # Mã phái sinh
    market = "VNFE"          # Thị trường phái sinh SSI dùng 'VNFE'
    account = "YOUR_DERIV_ACCOUNT"   # TODO: thay bằng tài khoản phái sinh của bạn
    quantity = 1             # Khối lượng
    side = "B"               # 'B' = Buy, 'S' = Sell (lệnh đầu tiên)
    stop_loss = 1870.0       # Giá dừng lỗ

    # ===== KHỞI TẠO CLIENT TRADING =====
    client = FCTradingClient(
        fc_config.Url,
        fc_config.ConsumerID,
        fc_config.ConsumerSecret,
        fc_config.PrivateKey,
        fc_config.TwoFAType,
    )
    print("Access token:", client.get_access_token())

    # ===== 1. ĐẶT LỆNH BAN ĐẦU =====
    position_info = place_initial_order(
        client=client,
        account=account,
        symbol=symbol,
        market=market,
        side=side,
        quantity=quantity,
    )

    # ===== 2. MONITOR GIÁ VÀ CẮT LỖ =====
    monitor_stoploss_and_hedge(
        client=client,
        account=account,
        position_info=position_info,
        stop_loss=stop_loss,
        poll_interval_sec=2,
    )


if __name__ == "__main__":
    main()
