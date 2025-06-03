import pandas as pd
import numpy as np

def add_daily_returns(df, close_col='Close'):
    """Calculates daily percentage returns."""
    df['Daily_Return'] = df[close_col].pct_change()
    return df

def add_log_returns(df, close_col='Close'):
    """Calculates daily logarithmic returns."""
    df['Log_Return'] = np.log(df[close_col] / df[close_col].shift(1))
    return df

def add_volatility(df, close_col='Close', window=20):
    """Calculates rolling standard deviation of daily returns as volatility."""
    df['Volatility'] = df[close_col].pct_change().rolling(window=window).std() * np.sqrt(252) # Annualized volatility
    return df

def add_price_change(df, close_col='Close', open_col='Open'):
    """Calculates the absolute price change from Open to Close."""
    df['Price_Change'] = df[close_col] - df[open_col]
    return df

def add_all_common_financial_metrics(df, open_col='Open', high_col='High', low_col='Low', close_col='Close', volume_col='Volume'):
    """
    Adds a comprehensive set of common financial metrics to the DataFrame.
    """
    df_copy = df.copy()

    # Basic Checks
    if not all(col in df_copy.columns for col in [open_col, high_col, low_col, close_col, volume_col]):
        print(f"Warning: Missing one or more required OHLCV columns for financial metrics calculation. Ticker: {df.name if hasattr(df, 'name') else 'N/A'}")
        return df_copy

    df_copy = add_daily_returns(df_copy, close_col=close_col)
    df_copy = add_log_returns(df_copy, close_col=close_col)
    df_copy = add_volatility(df_copy, close_col=close_col)
    df_copy = add_price_change(df_copy, close_col=close_col, open_col=open_col)

    # You could add more here, e.g., high-low range, average volume, etc.

    return df_copy

if __name__ == '__main__':
    # This block runs only when financial_metrics.py is executed directly
    print("Testing financial_metrics.py:")
    test_data = {
        'Date': pd.to_datetime(pd.date_range(start='2023-01-01', periods=100, freq='D')),
        'Open': np.random.rand(100)*10 + 100,
        'High': np.random.rand(100)*10 + 105,
        'Low': np.random.rand(100)*10 + 95,
        'Close': np.random.rand(100)*10 + 100,
        'Volume': np.random.randint(10000, 50000, 100)
    }
    test_df = pd.DataFrame(test_data).set_index('Date')
    processed_test_df = add_all_common_financial_metrics(test_df)
    print("\nProcessed Test DataFrame Tail with Financial Metrics:")
    print(processed_test_df.tail())