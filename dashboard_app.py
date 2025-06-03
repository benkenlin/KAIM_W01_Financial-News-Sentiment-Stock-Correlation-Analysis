# dashboard_app.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import os

# --- 1. Load Pre-processed Data ---
# Assuming you've saved your processed data from the notebooks
DATA_DIR = 'data/processed/' # Adjust path as needed based on where dashboard_app.py is located

# Load all processed stock data
processed_stock_data = {}
for filename in os.listdir(DATA_DIR):
    if filename.endswith('_processed_stock_data.csv'):
        ticker = filename.split('_')[0]
        df = pd.read_csv(os.path.join(DATA_DIR, filename), index_col='Date', parse_dates=True)
        processed_stock_data[ticker] = df

# Load all merged correlation data (sentiment + stock returns)
merged_correlation_data = {}
for filename in os.listdir(DATA_DIR):
    if filename.endswith('_merged_correlation_data.csv'):
        ticker = filename.split('_')[0]
        df = pd.read_csv(os.path.join(DATA_DIR, filename), index_col='Date', parse_dates=True)
        merged_correlation_data[ticker] = df

# Load overall correlation summary
try:
    overall_correlation_summary = pd.read_csv(os.path.join(DATA_DIR, 'overall_correlation_summary.csv'))
except FileNotFoundError:
    overall_correlation_summary = pd.DataFrame(columns=['Ticker', 'Sentiment_vs_Daily_Return_Correlation'])
    print("Warning: overall_correlation_summary.csv not found. Correlation plot will be empty.")


# Get list of available tickers
available_tickers = sorted(list(processed_stock_data.keys()))

# --- 2. Initialize the Dash App ---
app = dash.Dash(name, title="Financial Market Insights Dashboard")
server = app.server # For deployment

# --- 3. Define the App Layout ---
app.layout = html.Div([
    html.H1("Financial Market Insights Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),
    html.P("Analyze News Sentiment, Stock Performance, and their Correlation", style={'textAlign': 'center', 'marginBottom': '30px', 'color': '#7f8c8d'}),

    # Dropdown for Ticker Selection
    html.Div([
        html.Label("Select Stock Ticker:", style={'fontSize': '1.2em', 'marginRight': '10px'}),
        dcc.Dropdown(
            id='ticker-dropdown',
            options=[{'label': ticker, 'value': ticker} for ticker in available_tickers],
            value='AAPL', # Default value
            clearable=False,
            style={'width': '200px', 'display': 'inline-block', 'verticalAlign': 'middle'}
        ),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    html.Hr(),

    # --- Section 1: Stock Price & Technical Indicators ---
    html.H2("Stock Price & Technical Indicators", style={'textAlign': 'center', 'marginTop': '30px', 'color': '#34495e'}),
    dcc.Graph(id='stock-price-plot'),
    dcc.Graph(id='rsi-plot'),
    dcc.Graph(id='macd-plot'),

    html.Hr(),

    # --- Section 2: News Sentiment & Correlation ---
    html.H2("News Sentiment & Correlation", style={'textAlign': 'center', 'marginTop': '30px', 'color': '#34495e'}),
    dcc.Graph(id='sentiment-plot'),
    dcc.Graph(id='correlation-bar-plot'),
    dcc.Graph(id='sentiment-return-scatter'), # New scatter plot for sentiment vs returns

])

# --- 4. Define Callbacks for Interactivity ---

# Callback for Stock Price and Technical Indicators
@app.callback(
    Output('stock-price-plot', 'figure'),
    Output('rsi-plot', 'figure'),
    Output('macd-plot', 'figure'),
    Input('ticker-dropdown', 'value')
)
def update_stock_plots(selected_ticker):
    df = processed_stock_data.get(selected_ticker)

    if df is None or df.empty:
        return {}, {}, {} # Return empty figures if data not found

    # Stock Price with SMAs
    trace_close = go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price', line=dict(color='#3498db'))
    trace_sma20 = go.Scatter(x=df.index, y=df['SMA_20'], mode='lines', name='SMA 20', line=dict(color='#2ecc71', dash='dot'))
    trace_sma50 = go.Scatter(x=df.index, y=df['SMA_50'], mode='lines', name='SMA 50', line=dict(color='#e67e22', dash='dash'))

    # Bollinger Bands
    trace_upper = go.Scatter(x=df.index, y=df['Upper_Band'], mode='lines', name='Upper Band', line=dict(color='#95a5a6', dash='dot', width=1))
    trace_middle = go.Scatter(x=df.index, y=df['Middle_Band'], mode='lines', name='Middle Band', line=dict(color='#7f8c8d', dash='dash', width=1))
    trace_lower = go.Scatter(x=df.index, y=df['Lower_Band'], mode='lines', name='Lower Band', line=dict(color='#95a5a6', dash='dot', width=1))


    stock_price_figure = {
        'data': [trace_close, trace_sma20, trace_sma50, trace_upper, trace_middle, trace_lower],
        'layout': go.Layout(
            title=f'{selected_ticker} Stock Price with Moving Averages & Bollinger Bands',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Price ($)'},
            hovermode='x unified',
            template='plotly_white',
            legend=dict(x=0, y=1.0, traceorder='normal', orientation='h')
        )
    }

    # RSI Plot
    rsi_figure = {
        'data': [
            go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI', line=dict(color='#8e44ad')),
            go.Scatter(x=df.index, y=[70]*len(df), mode='lines', name='Overbought', line=dict(color='red', dash='dash', width=1)),
            go.Scatter(x=df.index, y=[30]*len(df), mode='lines', name='Oversold', line=dict(color='green', dash='dash', width=1))
        ],
        'layout': go.Layout(
            title=f'{selected_ticker} Relative Strength Index (RSI)',
            xaxis={'title': 'Date'},
            yaxis={'title': 'RSI Value', 'range': [0, 100]},
            hovermode='x unified',
            template='plotly_white',
            legend=dict(x=0, y=1.0, traceorder='normal', orientation='h')
        )
    }

    # MACD Plot
    macd_figure = {
        'data': [
            go.Scatter(x=df.index, y=df['MACD'], mode='lines', name='MACD Line', line=dict(color='#1abc9c')),
            go.Scatter(x=df.index, y=df['MACD_Signal'], mode='lines', name='Signal Line', line=dict(color='#e74c3c')),
            go.Bar(x=df.index, y=df['MACD_Hist'], name='Histogram', marker_color='#95a5a6', opacity=0.7)
        ],
        'layout': go.Layout(
            title=f'{selected_ticker} Moving Average Convergence Divergence (MACD)',
            xaxis={'title': 'Date'},
            yaxis={'title': 'MACD Value'},
            hovermode='x unified',
            template='plotly_white',
            legend=dict(x=0, y=1.0, traceorder='normal', orientation='h')
        )
    }
    return stock_price_figure, rsi_figure, macd_figure


# Callback for Sentiment Plot and Correlation Scatter Plot
@app.callback(
    Output('sentiment-plot', 'figure'),
    Output('sentiment-return-scatter', 'figure'),
    Input('ticker-dropdown', 'value')
)
def update_sentiment_plots(selected_ticker):
    df_merged = merged_correlation_data.get(selected_ticker)

    if df_merged is None or df_merged.empty:
        return {}, {}

    # Sentiment Plot
    sentiment_figure = {
        'data': [
            go.Scatter(x=df_merged.index, y=df_merged['daily_avg_sentiment'], mode='lines', name='Daily Average Sentiment', line=dict(color='#f39c12'))
        ],
        'layout': go.Layout(
            title=f'{selected_ticker} Daily Average News Sentiment',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Sentiment Score', 'range': [-1, 1]},
            hovermode='x unified',
            template='plotly_white',
            legend=dict(x=0, y=1.0, traceorder='normal', orientation='h')
        )
    }

    # Sentiment vs. Daily Return Scatter Plot
    scatter_figure = {
        'data': [
            go.Scatter(
                x=df_merged['daily_avg_sentiment'],
                y=df_merged['Daily_Return'],
                mode='markers',
                marker=dict(
                    size=8,opacity=0.6,
                    color=df_merged['daily_avg_sentiment'], # Color by sentiment score
                    colorscale='RdYlGn', # Red-Yellow-Green for sentiment
                    colorbar=dict(title='Sentiment'),
                    line=dict(width=1, color='DarkSlateGrey')
                ),
                name='Sentiment vs. Return'
            )
        ],
        'layout': go.Layout(
            title=f'{selected_ticker} Daily Sentiment vs. Daily Return (Correlation: {df_merged["daily_avg_sentiment"].corr(df_merged["Daily_Return"]):.4f})',
            xaxis={'title': 'Daily Average Sentiment Score'},
            yaxis={'title': 'Daily Stock Return (%)'},
            hovermode='closest',
            template='plotly_white'
        )
    }
    return sentiment_figure, scatter_figure


# Callback for Overall Correlation Bar Plot (independent of dropdown)
@app.callback(
    Output('correlation-bar-plot', 'figure'),
    Input('ticker-dropdown', 'value') # Using an input to trigger update, but data is static
)
def update_correlation_bar_plot(selected_ticker): # selected_ticker is unused, but required by Input
    if overall_correlation_summary.empty:
        return {
            'data': [],
            'layout': go.Layout(
                title='Overall Correlation: Sentiment vs. Daily Return',
                annotations=[
                    go.layout.Annotation(
                        text='No correlation data available. Please run Correlation_Analysis.ipynb first.',
                        xref="paper", yref="paper",
                        showarrow=False,
                        font=dict(size=16)
                    )
                ]
            )
        }

    bar_figure = {
        'data': [
            go.Bar(
                x=overall_correlation_summary['Ticker'],
                y=overall_correlation_summary['Sentiment_vs_Daily_Return_Correlation'],
                marker_color=overall_correlation_summary['Sentiment_vs_Daily_Return_Correlation'],
                colorscale='RdBu', # Red-Blue for positive/negative correlation
                colorbar=dict(title='Correlation')
            )
        ],
        'layout': go.Layout(
            title='Overall Correlation: Daily News Sentiment vs. Daily Stock Returns',
            xaxis={'title': 'Stock Ticker'},
            yaxis={'title': 'Pearson Correlation Coefficient', 'range': [-1, 1]},
            template='plotly_white'
        )
    }
    return bar_figure


# --- 5. Run the App ---
if __name__ == '__main__':
    app.run_server(debug=True)