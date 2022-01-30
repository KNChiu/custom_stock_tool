from backtesting import Backtest, Strategy      # 引入回測和交易策略功能

class Costaveraging(Strategy): 
    mounthCost = 5000       # 定期定額金額
    dayContcycle = 30       # 定期定額週期
    
    def init(self):
        self.dayCont = 0             
        pass

    def next(self):
        if self.dayCont > self.dayContcycle:    # 當到了定期定額購買週期
            self.dayCont = 0

            numShares = self.mounthCost // self.data.Close[-1]      # 計算價值 mounthCost 金額等價股數
            self.buy(size = numShares)
        else:
            self.dayCont += 1

if __name__ == '__main__':
    from trading_tool.model import StockTool

    target_stock='0050.tw'
    date_range = "20200101-20220128"

    st_tool = StockTool(target_stock='0050.tw', date_range = "20200101-20220128")
    df = st_tool.crawler2pandas()
    # st_tool.crawler2CSV()

    test = Backtest(df, Costaveraging, cash=75000, commission=.004)
    # 指定回測程式為test，在Backtest函數中依序放入(資料來源、策略、現金、手續費)

    result = test.run()
    #執行回測程式並存到result中

    print(result) # 直接print文字結果

    test.plot(filename=f"./backtest_result/SmaCross_{target_stock}_{date_range}.html") #將線圖網頁依照指定檔名保存