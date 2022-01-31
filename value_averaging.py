#%%
from backtesting import Backtest, Strategy      # 引入回測和交易策略功能

class ValueAveraging(Strategy): 
    mounthCost = 5000       # 定期定額金額
    dayContcycle = 30       # 定期定額週期
    
    
    def init(self):
        self.dayCont = 0            # 天數計數
        self.mounthCont = 1         # 週期計數

        self.expectedValue = 0      # 預期價值
        self.actualValue = 0        # 實際價值
        self.sumShares = 0          # 股數總和
        self.cashSurplus = 0        # 現金盈餘

        self.buySharessize = 0      # 買入數量
        self.sellSharessize = 0     # 賣出數量


    def next(self):
        
        if self.dayCont >= self.dayContcycle:    # 當到了定期購買週期
            self.dayCont = 0

            print("第N次交易 :", self.mounthCont)

            self.expectedValue = self.mounthCont * self.mounthCost
            self.actualValue = self.sumShares * self.data.Close[-1]

            print("預期價值 :", self.expectedValue, "實際價值 :", round(self.actualValue))

            if self.expectedValue ==  0:                  # 第一次購入
                self.buySharessize = self.mounthCost // self.data.Close[-1]
                self.buy(size = self.buySharessize)              # 買入第一次股數
                self.sumShares += self.buySharessize

            else:
                if self.actualValue > self.expectedValue :      # 如果實際價值大於預計價值
                    self.sellSharessize = (self.actualValue - self.expectedValue) // self.data.Close[-1]
                    self.sell(size = self.sellSharessize)            # 賣出多餘股數
                    self.cashSurplus = self.sellSharessize * self.data.Close[-1]
                    self.sumShares -= self.sellSharessize

                elif self.actualValue < self.expectedValue :
                    self.buySharessize = (self.expectedValue - self.actualValue) // self.data.Close[-1]
                    self.buy(size = self.buySharessize)              # 買入不足股數
                    self.sumShares += self.buySharessize

            print("股票價值 :", round(self.sumShares * self.data.Close[-1]), "現金盈餘 :", round(self.cashSurplus))
            print("購買股數 :", self.buySharessize)
            print("-----------------------------")


            self.mounthCont += 1

        else:
            self.dayCont += 1

if __name__ == '__main__':
    from trading_tool.model import StockTool

    target_stock='0050.tw'
    date_range = "20200101-20220128"

    st_tool = StockTool(target_stock='0050.tw', date_range = "19990101-20211231")
    df = st_tool.crawler2pandas()
    # st_tool.crawler2CSV()

    test = Backtest(df, ValueAveraging, cash=510000, commission=.004)
    # 指定回測程式為test，在Backtest函數中依序放入(資料來源、策略、現金、手續費)

    result = test.run()
    #執行回測程式並存到result中

    print(result) # 直接print文字結果
    print(result['_trades'])

    test.plot(filename=f"./backtest_result/SmaCross_{target_stock}_{date_range}.html") #將線圖網頁依照指定檔名保存