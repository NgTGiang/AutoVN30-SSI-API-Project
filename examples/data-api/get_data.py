from ssi_fc_data import fc_md_client, model
import config
from datetime import datetime


client = fc_md_client.MarketDataClient(config)
# def access_token():
#     print(client.access_token(model.accessToken(config.consumerID, config.consumerSecret)))

def get_intradate_data():
    print(client.intraday_ohlc(config, model.intraday_ohlc('VN30F1M', '21/11/2025', '21/11/2025', 1, 100, True, 1)))

def get_current_price():
    currentDate = datetime.now().strftime('%d/%m/%Y')
    response = client.intraday_ohlc(config, model.intraday_ohlc('VN30F1M', currentDate, currentDate, 1, 100))
    latest_record = max(response["data"], key=lambda x: x["Time"])
    currentPrice = latest_record["Close"]
    print("currentPrice: " + currentPrice)

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