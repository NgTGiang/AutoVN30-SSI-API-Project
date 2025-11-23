from ssi_fctrading import FCTradingStream, fc_stream
from ssi_fctrading import FCTradingClient
from urllib.parse import urlparse, urlunparse, urlencode, quote

import urllib3
import TradingConfig


def on_message(tapi_message):
    print("fc_received: " + tapi_message)


def on_error(tapi_error):
    print("fc_error: " + tapi_error)

def on_open():
    print('Connected to ' + TradingConfig.StreamURL)

def tapi_data_streaming(on_message, on_error):
    client = FCTradingClient(TradingConfig.Url, TradingConfig.ConsumerID,
                             TradingConfig.ConsumerSecret, TradingConfig.PrivateKey, TradingConfig.TwoFAType)
    print("access_token: " + client.get_access_token())
    stream_client = FCTradingStream(client, TradingConfig.StreamURL, on_message, on_error, TradingConfig.NotifyId, on_open=on_open)
    stream_client.start()
    message = None
    while message != "exit()":
        message = input(">> ")


# main function
if __name__ == '__main__':
    tapi_data_streaming(on_message, on_error)
