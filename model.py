import yfinance as yf
import pandas as pd
from pandas_datareader import data
from datetime import datetime

class StockTool():

    def __init__(self, 
        target_stock = ['0050.tw'], 
        date_range = "20200101-20210101"
    ):

        self.targetStock = target_stock         # 股票代號
        self.dateRange = date_range             # 起訖日期

    def crawler2pandas(self):
        yf.pdr_override()                       # 以 pandasreader格式

        date_range = self.dateRange             # 繼承區間
        start_date = datetime(int(date_range[0:4]), int(date_range[5:6]), int(date_range[7:8]))         # 日期解析
        end_date = datetime(int(date_range[9:13]), int(date_range[14:15]), int(date_range[16:17]))

        return data.get_data_yahoo(self.targetStock, start_date, end_date)    # 將資料存入 Dataframe


    # # filename = f'./data/{target_stock}.csv' #以股票名稱命名檔案，放在data資料夾下面
    # # df.to_csv(filename) #將df轉成CSV保存


if __name__ == '__main__':
    st_tool = StockTool()
    print(st_tool.crawler2pandas())             # 顯示 pandas 
