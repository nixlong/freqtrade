import numpy as np
import pandas as pd
import talib as ta
from .IndKey import IndKey as IK

class KindleIndicators:

    def __init__(self, dataframe: pd.DataFrame):
        """\
        初始化类，从 DataFrame 中提取价格和成交量数据\
        :param dataframe: 包含以下列的 DataFrame（区分大小写）:\
                          'open', 'high', 'low', 'close', 'volume'\
        """
        # 检查必要列是否存在
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in dataframe.columns for col in required_columns):
            missing = [col for col in required_columns if col not in dataframe.columns]
            raise ValueError(f"DataFrame 缺少必要列: {missing}")

        # 提取 numpy 数组格式数据
        self.open = dataframe['open'].values
        self.high = dataframe['high'].values
        self.low = dataframe['low'].values
        self.close = dataframe['close'].values
        self.volumes = dataframe['volume'].values
        self.df = dataframe  # 保留原始 DataFrame 引用

    # ----------------- 动量/震荡类指标 -----------------
    def RSI(self, period=14):
        """相对强弱指数 (默认14周期) """
        return ta.RSI(self.close, timeperiod=period)

    def STOCH_K_D(self, k_period=5, d_period=3, slowk=0):
        """随机指标K值 (默认5,3,0参数)"""
        k, d = ta.STOCH(self.high, self.low, self.close,
                        fastk_period=k_period, slowk_period=d_period,
                        slowk_matype=slowk, slowd_period=d_period)
        return k, d

    def CCI(self, period=20):
        """顺势指标 (默认20周期)"""
        cci20 = ta.CCI(self.high, self.low, self.close, timeperiod=period)
        cci20_previous = ta.CCI(self.df['high'].shift(1), self.df['low'].shift(1), self.df['close'].shift(1), timeperiod=period) 
        return cci20, cci20_previous

    def ADX(self, period=14):
        """
        平均趋向指数 (默认14周期)
        """
        # 计算ADX（默认周期14日）
        adx = ta.ADX(self.df['high'], self.df['low'], self.df['close'], timeperiod=period)  # 平均趋向指数
        # 计算+DI和-DI
        plus_di = ta.PLUS_DI(self.df['high'], self.df['low'], self.df['close'], timeperiod=period)  # 正向指标
        minus_di = ta.MINUS_DI(self.df['high'], self.df['low'], self.df['close'], timeperiod=period) # 负向指标

        return adx,plus_di,minus_di

    def AO(self, fast_period=5, slow_period=34):
        """动量震荡器 (固定5/34周期EMA差)"""
        median_price = (self.high + self.low) / 2
        sma_fast = ta.SMA(median_price, timeperiod=fast_period)
        sma_slow = ta.SMA(median_price, timeperiod=slow_period)
        return sma_fast - sma_slow

        # return ta.AO(self.high, self.low)

    def Mom(self, period=10):
        """动量指标 (默认10周期)"""
        return ta.MOM(self.close, timeperiod=period)

    def MACD(self, fast=12, slow=26, signal=9):
        """MACD指标 (默认12/26/9周期)"""
        macd, signal_line, _ = ta.MACD(self.close, fastperiod=fast,
                                      slowperiod=slow, signalperiod=signal)
        return macd, signal_line

    def Stoch_RSI(self, period=14, k_period=3, d_period=3):
        """随机RSI (需自定义实现)"""
        rsi = self.RSI(period)
        stoch_k, _ = ta.STOCH(rsi, rsi, rsi,  # 使用RSI替代价格
                             fastk_period=k_period, slowk_period=d_period,
                             slowk_matype=0, slowd_period=d_period)
        return stoch_k

    def WR(self, period=14):
        """威廉指标 (默认14周期)"""
        return ta.WILLR(self.high, self.low, self.close, timeperiod=period)

    def BBP(self, period=20, nbdev=2):
        """布林带宽度百分比 (需自定义计算)"""
        upper, middle, lower = ta.BBANDS(self.close, timeperiod=period,
                                         nbdevup=nbdev, nbdevdn=nbdev)
        return upper, middle, lower, (upper - lower) / middle

    def UO(self, period1=7, period2=14, period3=28):
        """终极震荡器 (需自定义实现)"""
        # 计算加权平均动量
        avg1 = ta.SMA(self.close, period1)
        avg2 = ta.SMA(self.close, period2)
        avg3 = ta.SMA(self.close, period3)
        return (4*avg1 + 2*avg2 + avg3) / 7 * 100

    # ----------------- 均线类指标 -----------------
    def _ma_factory(ma_type, period):
        """工厂函数生成EMA/SMA方法"""
        def ma(self):
            return getattr(ta, ma_type)(self.close, timeperiod=period)
        return ma

    # 动态生成EMA/SMA方法 (EMA10, SMA10等)
    for period in [5, 10, 20, 30, 50, 100, 200]:
        locals()[f'EMA{period}'] = _ma_factory('EMA', period)
        locals()[f'SMA{period}'] = _ma_factory('SMA', period)

    def Ichimoku(self):
        """一目均衡表 (固定9/26/52周期)"""
        tenkan = (ta.MAX(self.high, 26) + ta.MIN(self.low, 26)) / 2
        kijun = (ta.MAX(self.high, 52) + ta.MIN(self.low, 52)) / 2
        senkou_span_a = (tenkan + kijun) / 2
        senkou_span_b = (ta.MAX(self.high, 52) + ta.MIN(self.low, 52)) / 2
        return tenkan, kijun, senkou_span_a, senkou_span_b

    def VWMA(self, period=20):
        """成交量加权均线 (需自定义实现)"""
        vwma = np.convolve(self.close * self.volumes, np.ones(period), 'valid') / \
               np.convolve(self.volumes, np.ones(period), 'valid')
        return np.concatenate([np.full(period-1, np.nan), vwma])

    def HullMA(self, period=20):
        """赫尔均线 (需自定义实现)"""
        wma_half = ta.WMA(self.close, timeperiod=period//2)
        wma_full = ta.WMA(self.close, timeperiod=period)
        hull_raw = 2 * wma_half - wma_full
        return ta.WMA(hull_raw, timeperiod=int(np.sqrt(period)))

    def cacl_all_indicators(self):
        """\
        生成所有指标的 DataFrame 分析\
        :return: 包含所有指标的 DataFrame\
        """

        self.df[IK.RSI] = self.RSI()
        self.df[IK.STOCH_K],self.df[IK.STOCH_D] = self.STOCH_K_D()
        self.df[IK.CCI20], self.df[IK.CCI201] = self.CCI()
        self.df[IK.ADX],self.df[IK.PLUS_DI],self.df[IK.MINUS_DI] = self.ADX()
        self.df[IK.AO] = self.AO()
        self.df[IK.Mom] = self.Mom()
        self.df[IK.MACD], self.df[IK.MACD_Signal] = self.MACD()
        self.df[IK.Stoch_RSI] = self.Stoch_RSI()
        self.df[IK.WR] = self.WR()
        self.df[IK.BBP_UB],self.df[IK.BBP_MD],self.df[IK.BBP_LB],self.df[IK.BBP_BAND] = self.BBP()
        self.df[IK.UO] = self.UO()

        self.df['EMA5'] = self.EMA5()
        self.df['SMA5'] = self.SMA5()
        self.df['EMA10'] = self.EMA10()
        self.df['SMA10'] = self.SMA10()
        self.df['EMA20'] = self.EMA20()
        self.df['SMA20'] = self.SMA20()
        self.df['EMA30'] = self.EMA30()
        self.df['SMA30'] = self.SMA30()
        self.df['EMA50'] = self.EMA50()
        self.df['SMA50'] = self.SMA50()
        self.df['EMA100'] = self.EMA100()
        self.df['SMA100'] = self.SMA100()
        self.df['EMA200'] = self.EMA200()
        self.df['SMA200'] = self.SMA200()
        # self.df['Ichimoku'] = self.Ichimoku()
        self.df['VWMA'] = self.VWMA()
        self.df['HullMA'] = self.HullMA()

        print(self.df[IK.CCI20], self.df[IK.CCI201])
        return self.df
