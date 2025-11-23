from ssi_fctrading import FCTradingClient
from ssi_fctrading.models import fcmodel_requests
from fastapi import FastAPI, Depends
import trading_config
import random


class TradingAPI:
    print("This is TradingAPI class")

    app = FastAPI()
    client = FCTradingClient(
        trading_config.Url, 
        trading_config.ConsumerID,
        trading_config.ConsumerSecret, 
        trading_config.PrivateKey, 
        trading_config.TwoFAType)
    print('Read token: ' + client.get_access_token())

    def __init__(self):
        print("TradingAPI initialized")
        self.app = TradingAPI.app
        self.client = TradingAPI.client




    """ FUNCTION: Place new order
        Args:
        ```	
        instrumentID (str): Mã chứng khoán
        market (str): Thị trường ('VN' hoặc 'VNFE')
        buySell (str): 'B' or 'S'
        orderType (str): Loại lệnh
        price (float): Giá. Với các lệnh điều kiện price=0
        quantity (int): Khối lượng
        account (str): Tài khoản
        stopOrder (bool, optional): Lệnh điều kiện (chỉ áp dụng với phái sinh). Defaults to False.
        stopPrice (float, optional): Giá trigger của lệnh điều kiện. Defaults to 0.
        stopType (str, optional): Loại lệnh điều kiện. Defaults to ''.
        stopStep (float, optional): . Defaults to 0.
        lossStep (float, optional): . Defaults to 0.
        profitStep (float, optional): . Defaults to 0.
        deviceId (str, optional): Định danh của thiết bị đặt lệnh
        userAgent (str, optional): Người dùng
        ```
    """
    @app.get("/newOrder")
    async def new_order(
        buySell: str, 
        stopPrice: float = 0, 
        stopType: str = 'B', 
        stopStep: float = 5, 
        lossStep: float = 5, 
        profitStep: float = 10, 
        price: float = 0, 
        instrumentID: str = 'VN30F2512', 
        market: str = 'VNFE', 
        account: str = 'R205098', 
        orderType: str = 'MP', 
        quantity: int = 1, 
        stopOrder: bool = True, 
        deviceId: str = FCTradingClient.get_deviceid(), 
        userAgent: str = FCTradingClient.get_user_agent(),
    ):
        fc_req = fcmodel_requests.NewOrder(
            str(account).upper(), 
            str(random.randint(0, 99999999)), 
            str(instrumentID).upper(), 
            str(market).upper(), 
            str(buySell).upper(), 
            str(orderType).upper(), 
            float(price), 
            int(quantity), 
            bool(stopOrder), 
            float(stopPrice), 
            str(stopType), 
            float(stopStep), 
            float(lossStep), 
            float(profitStep),
            deviceId= str(deviceId), 
            userAgent = str(userAgent))
        
        res = client.new_order(fc_req)
        return res

    @app.get("/newOrder")
    async def new_BullBear_order(
        buySell: str, 
        stopPrice: float = 0, 
        stopType: str = 'B', 
        stopStep: float = 5, 
        lossStep: float = 5, 
        profitStep: float = 10, 
        price: float = 0, 
        instrumentID: str = 'VN30F2512', 
        market: str = 'VNFE', 
        account: str = 'R205098', 
        orderType: str = 'MP', 
        quantity: int = 1, 
        stopOrder: bool = True, 
        deviceId: str = FCTradingClient.get_deviceid(), 
        userAgent: str = FCTradingClient.get_user_agent(),
    ):
        fc_req = fcmodel_requests.NewOrder(
            str(account).upper(), 
            str(random.randint(0, 99999999)), 
            str(instrumentID).upper(), 
            str(market).upper(), 
            str(buySell).upper(), 
            str(orderType).upper(), 
            float(price), 
            int(quantity), 
            bool(stopOrder), 
            float(stopPrice), 
            str(stopType), 
            float(stopStep), 
            float(lossStep), 
            float(profitStep),
            deviceId= str(deviceId), 
            userAgent = str(userAgent))
        
        res = client.new_order(fc_req)
        return res

if __name__ == "__main__":
    api = TradingAPI()
    print("TradingAPI module executed directly")