import pandas as pd
import talib
import numpy as np

def add_moving_averages(df, close_col='Close', periods=[10, 20, 50]):
    for p in periods:
        df[f'SMA_{p}'] = talib.SMA(df[close_col], timeperiod=p)
    return df

def add_rsi(df, close_col='Close', period=14):
    df['RSI'] = talib.RSI(df[close_col], timeperiod=period)
    return df

def add_macd(df, close_col='Close', fastperiod=12, slowperiod=26, signalperiod=9):
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = talib.MACD(
        df[close_col], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod
    )
    return df

def add_bollinger_bands(df, close_col='Close', timeperiod=20, nbdevup=2, nbdevdn=2):
    df['Upper_Band'], df['Middle_Band'], df['Lower_Band'] = talib.BBANDS(
        df[close_col], timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=0
    )
    return df

def add_stochastic_oscillator(df, high_col='High', low_col='Low', close_col='Close', fastk_period=14, slowk_period=3, slowd_period=3):
    df['STOCH_K'], df['STOCH_D'] = talib.STOCH(
        df[high_col], df[low_col], df[close_col],
        fastk_period=fastk_period, slowk_period=slowk_period, slowd_period=slowd_period
    )
    return df

def add_adx(df, high_col='High', low_col='Low', close_col='Close', timeperiod=14):
    df['ADX'] = talib.ADX(df[high_col], df[low_col], df[close_col], timeperiod=timeperiod)
    return df

def add_obv(df, close_col='Close', volume_col='Volume'):
    df['OBV'] = talib.OBV(df[close_col], df[volume_col])
    return df

def add_ad_line(df, high_col='High', low_col='Low', close_col='Close', volume_col='Volume'):
    df['AD'] = talib.AD(df[high_col], df[low_col], df[close_col], df[volume_col])
    return df

def add_atr(df, high_col='High', low_col='Low', close_col='Close', timeperiod=14):
    df['ATR'] = talib.ATR(df[high_col], df[low_col], df[close_col], timeperiod=timeperiod)
    return df

def add_all_common_indicators(df, open_col='Open', high_col='High', low_col='Low', close_col='Close', volume_col='Volume'):
    df_copy = df.copy()

    if not all(col in df_copy.columns for col in [open_col, high_col, low_col, close_col, volume_col]):
        print(f"Warning: Missing one or more required OHLCV columns in DataFrame for comprehensive indicator calculation. Ticker: {df.name if hasattr(df, 'name') else 'N/A'}")
        return df_copy

    df_copy = add_moving_averages(df_copy, close_col=close_col)
    df_copy = add_rsi(df_copy, close_col=close_col)
    df_copy = add_macd(df_copy, close_col=close_col)
    df_copy = add_bollinger_bands(df_copy, close_col=close_col)
    df_copy = add_stochastic_oscillator(df_copy, high_col=high_col, low_col=low_col, close_col=close_col)
    df_copy = add_adx(df_copy, high_col=high_col, low_col=low_col, close_col=close_col)
    df_copy = add_obv(df_copy, close_col=close_col, volume_col=volume_col)
    df_copy = add_ad_line(df_copy, high_col=high_col, low_col=low_col, close_col=close_col, volume_col=volume_col)
    df_copy = add_atr(df_copy, high_col=high_col, low_col=low_col, close_col=close_col)

    return df_copy

# Add name == 'main' block for testing if not already there
if __name__ == '__main__':
    print("Testing technical_analysis.py:")
    test_data = {
        'Date': pd.to_datetime(pd.date_range(start='2023-01-01', periods=100, freq='D')),
        'Open': np.random.rand(100)*10 + 100, 'High': np.random.rand(100)*10 + 105,
        'Low': np.random.rand(100)*10 + 95, 'Close': np.random.rand(100)*10 + 100,
        'Volume': np.random.randint(10000, 50000, 100)
    }
    test_df = pd.DataFrame(test_data).set_index('Date')
    processed_test_df = add_all_common_indicators(test_df)
    print("\nProcessed Test DataFrame Tail with Indicators:")
    print(processed_test_df.tail())