# Binance time series forecasting
![Cryptocurrency Price Prediction Platform](assets/main.png)

Welcome to our Binance Price Prediction demo, a humble showcase leveraging `amazon-science/chronos-forecasting` for time series forecasting. This demo provides a glimpse into the Chronos model's capabilities by fetching and forecasting cryptocurrency prices from Binance.

## Features

This demo allows users to interact with the platform to customize their predictions based on various parameters:

- **Asset Name**: Choose different cryptocurrency pairs like APTUSDT, BTCUSDT, etc.
- **From Period**: Select the starting date for the price data.
- **To Period**: Choose the ending date for the price data.
- **Predictions Length**: Determine the number of future data points you wish to forecast.
- **Time Window**: Set the time interval for each data point (e.g., 30 minutes, 1 hour).

## Configuration

For this demo, you need to specify your Binance API keys in the `config.json` file to fetch the price data.

Here's a sample of what your `config.json` should look like:

```json
{
  "binance_api_key": "YOUR_BINANCE_API_KEY",
  "binance_secret_key": "YOUR_BINANCE_SECRET_KEY"
}
```

## About Chronos Forecasting

Chronos stands as an innovative approach to time series forecasting, utilizing language model architectures. It transforms a time series into a sequence of tokens through scaling and quantization.

A language model is then trained on these tokens with a cross-entropy loss function, enabling Chronos to offer probabilistic forecasts. These models are trained on a broad array of both public time series data and synthetic data created through Gaussian processes.

## Probabilistic Forecasts

This demo generates probabilistic forecasts by simulating multiple future trajectories with the historical data provided, offering a useful tool for understanding the uncertainty in predictions.

## Disclaimer

This is a demo and for demonstration purposes only. It utilizes historical data to make predictions and does not guarantee future performance.

## License

This project is under the MIT License - see the LICENSE file for more information.

## Acknowledgments

- Our thanks go to the `amazon-science/chronos-forecasting` team for their pioneering efforts in time series forecasting.
- Gratitude to Binance for providing the API for fetching real-time cryptocurrency data.
