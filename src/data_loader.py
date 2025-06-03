import pandas as pd
import os

def load_all_historical_data(data_dir='../data'):
    historical_dfs = {}
    for filename in os.listdir(data_dir):
        if filename.endswith('_historical_data.csv'):
            filepath = os.path.join(data_dir, filename)
            ticker = filename.split('_')[0]
            try:
                df = pd.read_csv(filepath)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.set_index('Date').sort_index()

                for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    else:
                        print(f"Warning: Column '{col}' not found in {filename}. Some TA-Lib functions might fail.")
                df.dropna(subset=['Open', 'High', 'Low', 'Close'], inplace=True)

                historical_dfs[ticker] = df
                print(f"Loaded {ticker} data from {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return historical_dfs

# Add name == 'main' block for testing if not already there
if __name__ == '__main__':
    print("Testing data_loader.py:")
    loaded_data = load_all_historical_data()
    for ticker, df in loaded_data.items():
        print(f"\n{ticker} Data Head:")
        print(df.head())
        print(f"{ticker} Data Info:")
        df.info()