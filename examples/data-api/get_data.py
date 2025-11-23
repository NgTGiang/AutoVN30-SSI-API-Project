from ssi_fc_data import fc_md_client, model
import config


client = fc_md_client.MarketDataClient(config)
# def access_token():
#     print(client.access_token(model.accessToken(config.consumerID, config.consumerSecret)))

def get_intradate_data():
    print(client.intraday_ohlc(config, model.intraday_ohlc('VN30F2512', '19/11/2025', '19/11/2025', 1, 100, True, 1)))

def main():
    implement = True
    while implement:
        print('\n-----------------------')
        print('          MENU           ')
        print('-----------------------')
        print('01  - Get intraday data')
        print('00  - Exist\n')
        value = input('Enter your choice: ')

        if value == '01':
            get_intradate_data()
        if value == '00':
            implement = False
            print('\n-------------Exist-------------\n')

if __name__ == '__main__':
    main()