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

    from backtesting import Backtest, Strategy      # 引入回測和交易策略功能
    from backtesting.lib import crossover           # 引入判斷均線交會功能
    from backtesting.test import SMA                # 引入繪製均線功能


    class SmaCross(Strategy):                       # 交易策略命名為SmaClass，使用backtesting.py的Strategy功能
        n1 = 5                                      # 設定第一條均線日數為5日(周線)
        n2 = 20                                     # 設定第二條均線日數為20日(月線)，這邊的日數可自由調整

        def init(self):
            self.sma1 = self.I(SMA, self.data.Close, self.n1) #定義第一條均線為sma1，使用backtesting.py的SMA功能算繪
            self.sma2 = self.I(SMA, self.data.Close, self.n2) #定義第二條均線為sma2，使用backtesting.py的SMA功能算繪

        def next(self):
            if crossover(self.sma1, self.sma2):     #如果周線衝上月線，表示近期是上漲的，則買入
                self.buy()
            elif crossover(self.sma2, self.sma1):   #如果周線再與月線交叉，表示開始下跌了，則賣出
                self.sell()

    test = Backtest(df, SmaCross, cash=10000, commission=.002)
    # 指定回測程式為test，在Backtest函數中依序放入(資料來源、策略、現金、手續費)

    result = test.run()
    #執行回測程式並存到result中

    print(result) # 直接print文字結果

    test.plot(filename=f"./backtest_result/{target_stock}.html") #將線圖網頁依照指定檔名保存
