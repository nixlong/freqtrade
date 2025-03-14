import pandas as pd
import json

class FreqTradeUtils:

    def __init__(self):
        pass

    @staticmethod
    def load_ft_data(json_path: str) -> pd.DataFrame:
        # 读取JSON文件
        with open(json_path, 'r') as f:
            raw_data = json.load(f)
        
        # 数据转换（保持不变）
        df = pd.DataFrame(
            raw_data,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        
        # 时间戳转换（毫秒级时间戳处理）
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')  # 
        
        # # 列名标准化（根据FreqTrade数据特征）
        # column_mapping = {
        #     'open': 'Open',
        #     'high': 'High',
        #     'low': 'Low',
        #     'close': 'Close',
        #     'volume': 'Volume'
        # }
        # df = df.rename(columns=column_mapping)  # 
        
        # 设置时间索引
        df = df.set_index('timestamp')
        
        # 确保数值类型正确
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)  # 
        
        '''
        return format:
        
        timestamp       open     high      low    close      volume     datetime
        1704067200000  2281.87  2297.18  2281.27  2295.51   10771.9183  2024-01-01 00:00:00
        1704070800000  2295.52  2306.60  2292.90  2303.72   8413.4260   2024-01-01 01:00:00
        1704074400000  2303.72  2304.72  2291.20  2293.02   5808.2533   2024-01-01 02:00:00
        '''
        return df.sort_index()

