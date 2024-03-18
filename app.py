from flask import Flask, request, jsonify, render_template
import io
import base64
import matplotlib
import json
from binance.client import Client
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from chronos import ChronosPipeline

matplotlib.use('Agg')
app = Flask(__name__)

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Binance API keys (replace these with your actual API keys)
api_key = config['api_key']
api_secret = config['api_secret']

# Create a Binance client
client = Client(api_key, api_secret)


# Function to fetch historical prices
def fetch_historical_prices(symbol, start_str, end_str, interval_code):
    # Convert the start and end dates to milliseconds
    start_time = int(datetime.strptime(start_str,
                                       "%Y-%m-%d").timestamp() * 1000)  # Parse date as timestamp and convert to milliseconds
    end_time = int(datetime.strptime(end_str,
                                     "%Y-%m-%d").timestamp() * 1000)  # Parse date as timestamp and convert to milliseconds

    # Use the mapping to get the correct Binance interval constant
    interval = interval_mapping.get(interval_code)
    if not interval:
        raise ValueError(f"Invalid interval code: {interval_code}")

    # Fetch historical klines (OHLCV) from Binance
    klines = client.get_historical_klines(symbol, interval, str(start_time), str(end_time))

    # Fetch historical klines (OHLCV) from Binance
    klines = client.get_historical_klines(symbol, interval, str(start_time), str(end_time))

    # Create a DataFrame
    df = pd.DataFrame(klines, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                                       'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
                                       'Taker Buy Quote Asset Volume', 'Ignore'])

    # Convert timestamps to readable dates
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')

    # Keep only the Open Time and Close columns
    df = df[['Open Time', 'Close']]

    # Rename columns
    df.columns = ['Time', 'Token Price']

    # Convert the 'Close' prices to float
    df['Token Price'] = df['Token Price'].astype(float)

    return df


# Assuming 'ChronosPipeline' is available and correctly imported; adjust as needed
pipeline = ChronosPipeline.from_pretrained(
    "amazon/chronos-t5-small",
    device_map="cpu",  # Adjusted to target CPU explicitly if necessary
    torch_dtype=torch.float32,  # Using float32 for broader compatibility, especially on CPU
)

interval_mapping = {
    "1m": Client.KLINE_INTERVAL_1MINUTE,
    "3m": Client.KLINE_INTERVAL_3MINUTE,
    "5m": Client.KLINE_INTERVAL_5MINUTE,
    "15m": Client.KLINE_INTERVAL_15MINUTE,
    "30m": Client.KLINE_INTERVAL_30MINUTE,
    "1h": Client.KLINE_INTERVAL_1HOUR,
    "2h": Client.KLINE_INTERVAL_2HOUR,
    "4h": Client.KLINE_INTERVAL_4HOUR,
    "6h": Client.KLINE_INTERVAL_6HOUR,
    "8h": Client.KLINE_INTERVAL_8HOUR,
    "12h": Client.KLINE_INTERVAL_12HOUR,
    "1d": Client.KLINE_INTERVAL_1DAY,
    "3d": Client.KLINE_INTERVAL_3DAY,
    "1w": Client.KLINE_INTERVAL_1WEEK,
    "1M": Client.KLINE_INTERVAL_1MONTH,
}


def showPricesPrediction(lenprediction, df):
    # context must be either a 1D tensor, a list of 1D tensors,
    # or a left-padded 2D tensor with batch as the first dimension
    context = torch.tensor(df["Token Price"])
    prediction_length = lenprediction
    forecast = pipeline.predict(context, prediction_length)  # shape [num_series, num_samples, prediction_length]

    # visualize the forecast
    forecast_index = range(len(df), len(df) + prediction_length)
    low, median, high = np.quantile(forecast[0].numpy(), [0.1, 0.5, 0.9], axis=0)

    plt.figure(figsize=(8, 4))
    plt.plot(df["Token Price"], color="royalblue", label="historical data")
    plt.plot(forecast_index, median, color="tomato", label="median forecast")
    plt.fill_between(forecast_index, low, high, color="tomato", alpha=0.3, label="80% prediction interval")
    plt.legend()
    plt.grid()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Encode the image in base64 to send as JSON
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return image_base64


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-plot', methods=['POST'])
def generate_plot():
    # Assuming request JSON has 'symbol', 'start_str', 'end_str', 'interval', 'lenprediction'
    data = request.get_json()
    symbol = data['asset']
    start_str = data['from_period']
    end_str = data['to_period']
    interval = data['interval']
    lenprediction = int(data['lenprediction'])
    # Fetch historical prices and prepare dataframe here...
    # Assuming `fetch_historical_prices` returns a DataFrame compatible with `showPricesPrediction`
    df = fetch_historical_prices(symbol, start_str, end_str, interval)

    # Generate the base64-encoded plot image
    plot_image_base64 = showPricesPrediction(lenprediction, df)

    # Return the base64-encoded image
    return jsonify({'image': plot_image_base64})


if __name__ == '__main__':
    app.run(debug=True)
