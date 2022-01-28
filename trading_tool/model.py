import yfinance as yf
import pandas as pd
from pandas_datareader import data
from datetime import datetime
import os

class StockTool():

    def __init__(self, 
        target_stock = '0050.tw', 
        date_range = "20200101-20210101",
        csv_save_path = r"data"
    ):

        self.targetStock = target_stock         # 股票代號
        self.dateRange = date_range             # 起訖日期
        self.CSVSavePath = csv_save_path        # CSV 存放位置

    def crawler2pandas(self):                   # 爬取股價並以 pandas 格式存取
        yf.pdr_override()                       # 以 pandasreader格式

        date_range = self.dateRange             # 繼承區間
        start_date = datetime(int(date_range[0:4]), int(date_range[5:6]), int(date_range[7:8]))         # 日期解析
        end_date = datetime(int(date_range[9:13]), int(date_range[14:15]), int(date_range[16:17]))

        return data.get_data_yahoo([self.targetStock], start_date, end_date)    # 將資料存入 Dataframe

    def crawler2CSV(self):                      # 爬取股價並以 CSV 存取 
        df = self.crawler2pandas()
        filename = os.path.join(str(self.CSVSavePath), self.targetStock)
        print("save at :", filename + '.csv')
        df.to_csv(filename + '.csv')            #將df轉成CSV保存


if __name__ == '__main__':

    target_stock = '0050.tw'
    date_range = "20200101-20210101"

    st_tool = StockTool()
    df = st_tool.crawler2pandas()
    # st_tool.crawler2CSV()
