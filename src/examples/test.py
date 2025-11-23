from ..utils.dataAPI import get_data
from ..utils.tradingAPI.trading_api import TradingAPI
from datetime import datetime
import time


def monitor_price_and_place_hedge_order(
        instrumentID: str, 
        quantity: int, 
        buySell: str,
        stopLoss: str,
        poll_interval_sec: int = 2
) -> dict:
    print(f"[StopLoss] Bắt đầu monitor {instrumentID}, side={buySell}, stopLoss={stopLoss}")
    while True:
        try:
            price = get_data.get_current_price(instrumentID)
        except Exception as e:
            print("[StopLoss] Lỗi lấy giá:", e)
            time.sleep(poll_interval_sec)
            continue

        # Điều kiện kích hoạt stop loss theo hướng vị thế
        trigger = False
        if buySell == "B" and price <= stopLoss:
            trigger = True
        elif buySell == "S" and price >= stopLoss:
            trigger = True

        print(f"[StopLoss] Giá hiện tại: {price} | trigger = {trigger}")

        if trigger:
            # Đặt lệnh ngược lại
            hedge_side = "S" if buySell == "B" else "B"
            req = TradingAPI.new_BullBear_order(hedge_side)
            print(f"[StopLoss] Kích hoạt! Đặt lệnh {hedge_side} {quantity} {instrumentID} @ {price}")
            res = TradingAPI.client.der_new_order(req)
            print("[StopLoss] Response hedge order:", res)
            break

        time.sleep(poll_interval_sec)
    

def main():
    # ===== INPUT BAN ĐẦU ============================
    price = get_data.get_current_price(instrumentIDValue)
    instrumentIDValue: str = "VN30F1M"  # Mã phái sinh
    marketValue: str = "VNFE"           # Thị trường phái sinh
    buySellValue: str = "B"             # 'B' = Buy, 'S' = Sell    
    orderTypeValue: str = "MP"          # 'MP' = Market Price, 'LO' = Limit Order
    priceValue: float = 0               # Giá đặt lệnh (0 cho lệnh MP)
    quantityValue: int = 1              # Khối lượng
    accountValue: str = "R205098"       # Tài khoản phái sinh

    stopOrderValue: bool = True
    stopPriceValue: float = price + 5
    stopTypeValue: str = 'B'            # Lệnh BullBear
    stopStepValue: float = 5            # Giảm 5 điểm → cắt lỗ
    lossStepValue: float = 5        
    profitStepValue: float = 10         # Tăng 10 điểm → chốt lời

    
    # ===== 1. ĐẶT LỆNH BAN ĐẦU ======================
    # Tạo request NewOrder
    req1 = TradingAPI.new_order(buySellValue, price)


    # ===== 2. MONITOR GIÁ VÀ TẠO LỆNH BÙ LỖ =========
    monitor_price_and_place_hedge_order(
        instrumentIDValue,
        quantityValue,
        buySellValue,
        
    )


if __name__ == "__main__":
    main()