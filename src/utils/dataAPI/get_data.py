from ssi_fc_data import fc_md_client, model
import DataConfig
from datetime import datetime
from zoneinfo import ZoneInfo


client = fc_md_client.MarketDataClient(DataConfig)
def access_token():
    print(client.access_token(model.accessToken(DataConfig.consumerID, DataConfig.consumerSecret)))

def get_intradate_data():
    print(client.intraday_ohlc(DataConfig, model.intraday_ohlc('VN30F1M', '21/11/2025', '21/11/2025', 1, 100, True, 1)))

def get_current_price(symbol: str = 'VN30F1M', ) -> float:
    currentDate = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).strftime('%d/%m/%Y')
    response = client.intraday_ohlc(DataConfig, model.intraday_ohlc(symbol, currentDate, currentDate))
    data = response.get("data", [])
    if not data:
        raise RuntimeError(f"CAN NOT invoke data for {symbol}: {response}")
    latest_record = max(data, key=lambda x: x["Time"])
    currentPrice = latest_record["Close"]
    print(f"Current price of [{symbol}]: {currentPrice}")
    return currentPrice

def main():
    implement = True
    while implement:
        print('\n-----------------------')
        print('          MENU           ')
        print('-----------------------')
        print('01  - Get intraday data')
        print('02  - Get current price')
        print('00  - Exist\n')
        value = input('Enter your choice: ')

        if value == '01':
            get_intradate_data()
        if value == '02':
            get_current_price()
        if value == '00':
            implement = False
            print('\n-------------Exist-------------\n')

if __name__ == '__main__':
    main()