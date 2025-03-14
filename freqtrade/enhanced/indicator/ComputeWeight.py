# Tradingview Technical Analysis (tradingview-ta)
# Author: deathlyface (https://github.com/deathlyface)
# Rewritten from https://www.tradingview.com/static/bundles/technicals.f2e6e6a51aebb6cd46f8.js
# License: MIT

import numpy as np
import pandas as pd
from .IndKey import IndKey as IK


class RecommendationX:
    buy = "BUY"
    strong_buy = "STRONG_BUY"
    sell = "SELL"
    strong_sell = "STRONG_SELL"
    neutral = "NEUTRAL"
    error = "ERROR"

class ComputeWeight:

    Indicator_Weight_Flag_RANGING  = 0  # 震荡行情的权重
    Indicator_Weight_Flag_TRENDING = 1  # 趋势行情的权重

    Indicator_Weight_Flag = Indicator_Weight_Flag_RANGING

    # 震荡行情的权重
    OSC_INDS_Weight =  [     # 震荡
                        {IK.RSI    :{'BUY': 12, 'NEUTRAL': 0, 'SELL': -12},   
                        IK.STOCH_K :{'BUY':  8, 'NEUTRAL': 0, 'SELL': - 8}, 
                        IK.CCI     :{'BUY':  8, 'NEUTRAL': 0, 'SELL': - 8}, 
                        IK.ADX      :{'BUY': 15, 'NEUTRAL': 0, 'SELL': -15}, 
                        IK.AO       :{'BUY':  7, 'NEUTRAL': 0, 'SELL': - 7}, 
                        IK.Mom      :{'BUY':  7, 'NEUTRAL': 0, 'SELL': - 7}, 
                        IK.MACD     :{'BUY': 15, 'NEUTRAL': 0, 'SELL': -15}, 
                        IK.Stoch_RSI:{'BUY':  6, 'NEUTRAL': 0, 'SELL': - 6}, 
                        IK.WR      :{'BUY':  5, 'NEUTRAL': 0, 'SELL': - 5}, 
                        IK.BBP      :{'BUY': 10, 'NEUTRAL': 0, 'SELL': -10}, 
                        IK.UO       :{'BUY':  7, 'NEUTRAL': 0, 'SELL': - 7}
                        },   # 趋势
                        {IK.RSI    :{'BUY': 12, 'NEUTRAL': 0, 'SELL': -12}, 
                        IK.STOCH_K :{'BUY':  8, 'NEUTRAL': 0, 'SELL': - 8}, 
                        IK.CCI     :{'BUY':  8, 'NEUTRAL': 0, 'SELL': - 8}, 
                        IK.ADX      :{'BUY': 15, 'NEUTRAL': 0, 'SELL': -15}, 
                        IK.AO       :{'BUY':  7, 'NEUTRAL': 0, 'SELL': - 7}, 
                        IK.Mom      :{'BUY':  7, 'NEUTRAL': 0, 'SELL': - 7}, 
                        IK.MACD     :{'BUY': 15, 'NEUTRAL': 0, 'SELL': -15}, 
                        IK.Stoch_RSI:{'BUY':  6, 'NEUTRAL': 0, 'SELL': - 6}, 
                        IK.WR      :{'BUY':  5, 'NEUTRAL': 0, 'SELL': - 5}, 
                        IK.BBP      :{'BUY': 10, 'NEUTRAL': 0, 'SELL': -10}, 
                        IK.UO       :{'BUY':  7, 'NEUTRAL': 0, 'SELL': - 7}
                        }
                    ]

    MA_INDS_Weight = [   # 震荡
                        {'EMA10'   :{'BUY':  7, 'NEUTRAL': 0, 'SELL': - 7},
                        'SMA10'   :{'BUY':  6, 'NEUTRAL': 0, 'SELL': - 6},
                        'EMA20'   :{'BUY':  8, 'NEUTRAL': 0, 'SELL': - 8},
                        'SMA20'   :{'BUY':  7, 'NEUTRAL': 0, 'SELL': - 7},
                        'EMA30'   :{'BUY':  5, 'NEUTRAL': 0, 'SELL': - 5},
                        'SMA30'   :{'BUY':  4, 'NEUTRAL': 0, 'SELL': - 4},
                        'EMA50'   :{'BUY':  3, 'NEUTRAL': 0, 'SELL': - 3},
                        'SMA50'   :{'BUY':  2, 'NEUTRAL': 0, 'SELL': - 2},
                        'EMA100'  :{'BUY':  2, 'NEUTRAL': 0, 'SELL': - 2},
                        'SMA100'  :{'BUY':  1, 'NEUTRAL': 0, 'SELL': - 1},
                        'EMA200'  :{'BUY':  1, 'NEUTRAL': 0, 'SELL': - 1},
                        'SMA200'  :{'BUY':  1, 'NEUTRAL': 0, 'SELL': - 1},
                        'Ichimoku':{'BUY': 18, 'NEUTRAL': 0, 'SELL': -18},
                        'VWMA'    :{'BUY': 15, 'NEUTRAL': 0, 'SELL': -15},
                        'HullMA'  :{'BUY': 20, 'NEUTRAL': 0, 'SELL': -20}
                        },  # 趋势
                        {'EMA10'   :{'BUY':  7, 'NEUTRAL': 0, 'SELL': - 7},
                        'SMA10'   :{'BUY':  6, 'NEUTRAL': 0, 'SELL': - 6},
                        'EMA20'   :{'BUY':  8, 'NEUTRAL': 0, 'SELL': - 8},
                        'SMA20'   :{'BUY':  7, 'NEUTRAL': 0, 'SELL': - 7},
                        'EMA30'   :{'BUY':  5, 'NEUTRAL': 0, 'SELL': - 5},
                        'SMA30'   :{'BUY':  4, 'NEUTRAL': 0, 'SELL': - 4},
                        'EMA50'   :{'BUY':  3, 'NEUTRAL': 0, 'SELL': - 3},
                        'SMA50'   :{'BUY':  2, 'NEUTRAL': 0, 'SELL': - 2},
                        'EMA100'  :{'BUY':  2, 'NEUTRAL': 0, 'SELL': - 2},
                        'SMA100'  :{'BUY':  1, 'NEUTRAL': 0, 'SELL': - 1},
                        'EMA200'  :{'BUY':  1, 'NEUTRAL': 0, 'SELL': - 1},
                        'SMA200'  :{'BUY':  1, 'NEUTRAL': 0, 'SELL': - 1},
                        'Ichimoku':{'BUY': 18, 'NEUTRAL': 0, 'SELL': -18},
                        'VWMA'    :{'BUY': 15, 'NEUTRAL': 0, 'SELL': -15},
                        'HullMA'  :{'BUY': 20, 'NEUTRAL': 0, 'SELL': -20}
                        }
                    ]

    
    @staticmethod
    def SetWeight(weight: int):
        if weight != ComputeWeight.Indicator_Weight_Flag_RANGING and weight != ComputeWeight.Indicator_Weight_Flag_TRENDING:
            return
        ComputeWeight.Indicator_Weight_Flag = weight
        pass

    ### Public Functions ###
    ### 所有参数条件:
    ###     条件1 : BUY
    ###     条件2 : SELL
    ###     条件3 : NEUTRAL, 通过 np.select 来实现

    @staticmethod
    def RSI(df : pd.DataFrame):
        """Compute Relative Strength Index

        Args:
            rsi (float): RSI value
            rsi1 (float): RSI[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """

        # RSI 权重
        rsi_conditions = [
            (df[IK.RSI] < 30) & (df[IK.RSI].shift(1) < df[IK.RSI]),  # 条件1, BUY
            (df[IK.RSI] > 70) & (df[IK.RSI].shift(1) > df[IK.RSI]),  # 条件2, SELL
        ]
        rsi_score = [ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.RSI]['BUY'], 
                     ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.RSI]['SELL']]  # 对应结果

        return np.select(rsi_conditions, rsi_score, default=0)
    
    @staticmethod
    def Stoch_K(df : pd.DataFrame):
        """Compute Stochastic

        Args:
            k (float): Stoch.K value
            d (float): Stoch.D value
            k1 (float): Stoch.K[1] value
            d1 (float): Stoch.D[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """

        _conditions = [
            (df[IK.STOCH_K] < 20) & (df[IK.STOCH_D] < 20) & (df[IK.STOCH_K] > df[IK.STOCH_D]) & (df[IK.STOCH_K].shift(1) < df[IK.STOCH_D].shift(1)),  # 条件1, BUY
            (df[IK.STOCH_K] > 80) & (df[IK.STOCH_D] > 80) & (df[IK.STOCH_K] < df[IK.STOCH_D]) & (df[IK.STOCH_K].shift(1) > df[IK.STOCH_D].shift(1)),  # 条件2. SELL
        ]
        _score = [ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.STOCH_K]['BUY'], 
                  ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.STOCH_K]['SELL']]  # 对应结果

        return np.select(_conditions, _score, default=0)

    @staticmethod
    def CCI(df : pd.DataFrame):
        """Compute Commodity Channel Index 20

        Args:
            cci20 (float): CCI20 value
            cci201 ([type]): CCI20[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        cci_conditions = [
            (df[IK.CCI20] < -100) & (df[IK.CCI20] > df[IK.CCI20].shift(1)),  # 条件1, BUY
            (df[IK.CCI20] > 100)  & (df[IK.CCI20] < df[IK.CCI20].shift(1)),  # 条件2, SELL
        ]
        cci_score = [ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.CCI]['BUY'], 
                     ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.CCI]['SELL']]
        
        return np.select(cci_conditions, cci_score, default=0)
    
    @staticmethod
    def ADX(df : pd.DataFrame):
        """Compute Average Directional Index

        Args:
            adx (float): ADX value
            adxpdi (float): ADX+DI value
            adxndi (float): ADX-DI value
            adxpdi1 (float): ADX+DI[1] value
            adxndi1 (float): ADX-DI[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        adx_conditions = [
            ((df[IK.ADX] > 20) & (df[IK.PLUS_DI].shift(1) < df[IK.MINUS_DI].shift(1)) & (df[IK.PLUS_DI] > df[IK.MINUS_DI])),  # 条件1, BUY
            ((df[IK.ADX] > 20) & (df[IK.PLUS_DI].shift(1) > df[IK.MINUS_DI].shift(1)) & (df[IK.PLUS_DI] < df[IK.MINUS_DI])),  # 条件2, SELL
        ]
        adx_score = [ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.ADX]['BUY'], 
                     ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.ADX]['SELL']]
        
        return np.select(adx_conditions, adx_score, default=0)

    @staticmethod
    def AO(df : pd.DataFrame):
        """Compute Awesome Oscillator

        Args:
            ao (float): AO value
            ao1 (float): AO[1] value
            ao2 (float): AO[2] value
        """
        ao_conditions = [
            ((df[IK.AO] > 0) & (df[IK.AO].shift(1) < 0)) | ((df[IK.AO] > 0) & (df[IK.AO].shift(1) > 0) & (df[IK.AO] > df[IK.AO].shift(1)) & (df[IK.AO].shift(2) > df[IK.AO].shift(1))),  
            ((df[IK.AO] < 0) & (df[IK.AO].shift(1) > 0)) | ((df[IK.AO] < 0) & (df[IK.AO].shift(1) < 0) & (df[IK.AO] < df[IK.AO].shift(1)) & (df[IK.AO].shift(2) < df[IK.AO].shift(1)))
        ]
        ao_score = [ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.AO]['BUY'], 
                    ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.AO]['SELL']]
        
        return np.select(ao_conditions, ao_score, default=0)
    
    @staticmethod
    def Mom(df : pd.DataFrame):
        """Compute Momentum

        Args:
            mom (float): Mom value
            mom1 (float): Mom[1] value
        """
        mom_conditions = [
            (df[IK.Mom] >  df[IK.Mom].shift(1)),  
            (df[IK.Mom] <  df[IK.Mom].shift(1))
        ]
        mom_score = [ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.Mom]['BUY'], 
                     ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.Mom]['SELL']]
        
        return np.select(mom_conditions, mom_score, default=0)
    
    @staticmethod
    def MACD(df : pd.DataFrame):
        """Compute Moving Average Convergence/Divergence

        Args:
            macd (float): MACD.macd value
            signal (float): MACD.signal value
        """
        macd_conditions = [
            (df[IK.MACD] > df[IK.MACD_Signal]),  
            (df[IK.MACD] < df[IK.MACD_Signal])
        ]
        macd_score = [ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.MACD]['BUY'], 
                      ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.MACD]['SELL']]
        
        return np.select(macd_conditions, macd_score, default=0)
    
    @staticmethod
    def WR(df : pd.DataFrame):
        """Compute Williams %R

        Args:
            wr (float): W%R value
        """
        wr_conditions = [
            (df[IK.WR] < -80),  
            (df[IK.WR] > -20)
        ]
        wr_score = [ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.WR]['BUY'], 
                    ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.WR]['SELL']]
        
        return np.select(wr_conditions, wr_score, default=0)

    @staticmethod
    def BBP(df : pd.DataFrame):
        """Compute Bull Bear Buy & Sell

        Args:
            close (float): close value
            bblower (float): BB.lower value
            bbupper (float): BB.upper value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        bbp_conditions = [
            (df[IK.CLOSE] < df[IK.BBP_LB]),  
            (df[IK.CLOSE] > df[IK.BBP_UB])
        ]
        bbp_score = [ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.BBP]['BUY'],
                     ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.BBP]['SELL']]
        
        return np.select(bbp_conditions, bbp_score, default=0)
        
    @staticmethod
    def UO(df : pd.DataFrame):
        """Compute Ultimate Oscillator

        Args:
            uo (float): UO value
        """
        uo_conditions = [
            (df[IK.UO] < 30),  
            (df[IK.UO] > 70)
        ]
        uo_score = [ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.UO]['BUY'], 
                    ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.UO]['SELL']]
        
        return np.select(uo_conditions, uo_score, default=0)
    
    @staticmethod
    def Stoch_RSI(df : pd.DataFrame):
        """Compute Stochastic RSI

        Args:
            stoch_rsi (float): Stoch.RSI value
        """
        stoch_rsi_conditions = [
            (df[IK.Stoch_RSI] < 20),  
            (df[IK.Stoch_RSI] > 80)
        ]
        stoch_rsi_score = [ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.Stoch_RSI]['BUY'], 
                           ComputeWeight.OSC_INDS_Weight[ComputeWeight.Indicator_Weight_Flag][IK.Stoch_RSI]['SELL']]
        
        return np.select(stoch_rsi_conditions, stoch_rsi_score, default=0)


    def MA(ma, close):
        """Compute Moving Average

        Args:
            ma (float): MA value
            close (float): Close value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (ma < close):
            return RecommendationX.buy
        elif (ma > close):
            return RecommendationX.sell
        else:
            return RecommendationX.neutral


    def PSAR(psar, open):
        """Compute Parabolic Stop-And-Reverse

        Args:
            psar (float): P.SAR value
            open (float): open value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (psar < open):
            return RecommendationX.buy
        elif (psar > open):
            return RecommendationX.sell
        else:
            return RecommendationX.neutral

    def Recommend(value):
        """Compute Recommend

        Args:
            value (float): recommend value

        Returns:
            string: "STRONG_BUY", "BUY", "NEUTRAL", "SELL", "STRONG_SELL", or "ERROR"
        """
        if value >= -1 and value < -.5:
            return RecommendationX.strong_sell
        elif value >= -.5 and value < -.1:
            return RecommendationX.sell
        elif value >= -.1 and value <= .1:
            return RecommendationX.neutral
        elif value > .1 and value <= .5 :
            return RecommendationX.buy
        elif value > .5 and value <= 1:
            return RecommendationX.strong_buy
        else:
            return RecommendationX.error

    def Simple(value):
        """Compute Simple

        Args:
            value (float): Rec.X value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (value == -1):
            return RecommendationX.sell
        elif (value == 1):
            return RecommendationX.buy
        else:
            return RecommendationX.neutral
