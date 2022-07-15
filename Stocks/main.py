import json
import time
import boto3
import yfinance as yf
import pandas as pd




def update_data():
    pass


def main():
    market_open = True
    file_name = 'stock_data.json'
    save_file = f'./Data/{file_name}'
    s3 = boto3.resource('s3',
                        aws_access_key_id=AWS_ACCESS_ID,
                        aws_secret_access_key=AWS_ACCESS_KEY
                        )

    ticker_names = ['AAPL', 'TSLA', 'MSFT', 'GOOG']
    hist = yf.Tickers(ticker_names)

    aapl = hist.tickers['AAPL']
    tsla = hist.tickers['TSLA']
    msft = hist.tickers['MSFT']
    goog = hist.tickers['GOOG']

    while market_open:
        update_data()

        aapl_info = aapl.history(period='1d', interval='5m')['Close']
        tsla_info = tsla.history(period='1d', interval='5m')['Close']
        msft_info = msft.history(period='1d', interval='5m')['Close']
        goog_info = goog.history(period='1d', interval='5m')['Close']

        stock_info = pd.concat([aapl_info, tsla_info, msft_info, goog_info], axis=1)
        # stock_info.index = stock_info.index.time
        stock_info.reset_index(inplace=True)
        stock_info.columns = pd.Index(['Time', 'Apple', 'Tesla', 'Microsoft', 'Google'], dtype='object')
        stock_info.to_json(save_file, orient="records")

        s3.meta.client.upload_file(
            Filename=save_file,
            Bucket='my-stock-price-bucket',
            Key=f'LiveStockData/{file_name}'
        )
        time.sleep(300)  # Every 5 min


        # result = stock_info.to_json(orient="index")
        # parsed = json.loads(result)
        # print(json.dumps(parsed, indent=4))
        # time.sleep(10)  # Every 5 min


if __name__ == '__main__':
    main()
