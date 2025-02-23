# Module 6 Project: Stock Sentiment Streaming Pipeline
This project implements a real-time stock sentiment analysis pipeline that streams data from a producer to a consumer using Kafka. The producer generates mock sentiment data for various stock tickers, and the consumer listens for updates, processes the data, and visualizes the sentiment trends and volatility over time.

## Overview
The pipeline consists of two main components:

    ### Producer (Producer_Mhamed.py): The producer continuously generates mock sentiment data for various stock tickers (e.g., AAPL, TSLA, MSFT, etc.) and sends it to a Kafka topic. Each data point includes: A timestamp, A stock ticker and a sentiment score (between -1 and 1), which represents the overall sentiment around the stock.
    ### Consumer (Consumer_Mhamed.py): The consumer listens to the Kafka topic, stores incoming sentiment data in an SQLite database, and visualizes the data using real-time charts. The consumer generates:

Bar Chart: Displays the current sentiment score for each stock ticker.
Line Chart: Shows the sentiment trend over time, smoothed with a moving average.
Volatility Chart: Displays the sentiment volatility (standard deviation) for each ticker.
Insight Focus
The core insights provided by this system are:

Real-Time Sentiment: The sentiment score for each stock ticker, updated every 10 seconds, gives insights into market sentiment towards specific stocks.
Sentiment Trends: A smoothed moving average of sentiment scores over time helps to identify the overall trend for a specific stock.
Volatility Analysis: A bar chart showing the volatility (standard deviation) of sentiment scores for each ticker. This helps to understand which stocks have more fluctuations in sentiment.
Each time a message arrives:

Producer: Generates random data for a stock ticker, including a sentiment score.
Consumer: Processes the data by storing it in an SQLite database and updating the visualizations:
Adds the sentiment score to the appropriate stock ticker's list.
Updates the bar chart showing the latest sentiment for each ticker.
Updates the line chart showing sentiment trends and moving averages.
Updates the volatility chart, which measures the sentiment score's fluctuations.
Running the Pipeline
1. Start the Kafka Broker
Before running the producer or consumer, make sure you have a running Kafka broker on localhost:9092.

2. Run the Producer
To run the producer, which will generate mock sentiment data for the stock tickers, use the following command:

bash
Copy
python Producer_Mhamed.py
This will continuously stream sentiment data for random stock tickers to the Kafka topic.

3. Run the Consumer
To start the consumer, which listens to the Kafka topic, processes the data, and visualizes the results, use:

bash
Copy
python Consumer_Mhamed.py
This will create real-time charts for sentiment trends, volatility, and real-time sentiment scores.

Visualization
The consumer generates three dynamic visualizations:

Real-Time Sentiment Distribution (Bar Chart): This chart updates every second, showing the latest sentiment score for each stock ticker, color-coded for positive (green) and negative (red) sentiment.


Sentiment Trends (Line Chart): This chart shows the moving average of sentiment scores for each stock over time.


Volatility (Bar Chart): This chart displays the volatility (standard deviation) of sentiment scores for each stock ticker.


Directory Structure
bash
Copy
.
├── Producer_Mhamed.py
├── Consumer_Mhamed.py
├── buzzline-06-Mhamed.sqlite  # SQLite database where sentiment data is stored
├── .env                      # Environment file to store Kafka settings
└── images/
    ├── sentiment_bar_chart.png
    ├── sentiment_trend_chart.png
    └── volatility_chart.png
Conclusion
This pipeline demonstrates how you can combine Kafka for real-time data streaming with SQLite for data storage and Matplotlib for dynamic data visualization. It's a useful setup for streaming and visualizing stock sentiment in real-time, providing insights into market trends and sentiment volatility.
