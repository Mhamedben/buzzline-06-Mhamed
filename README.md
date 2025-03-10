# Module 6 Project: Stock Sentiment Streaming Pipeline
This project implements a real-time stock sentiment analysis pipeline that streams data from a producer to a consumer using Kafka. The producer generates mock sentiment data for various stock tickers, and the consumer listens for updates, processes the data, and visualizes the sentiment trends and volatility over time.

## Overview
The pipeline consists of two main components:

### 1. Producer (Producer_Mhamed.py): 
The producer continuously generates mock sentiment data for various stock tickers (e.g., AAPL, TSLA, MSFT, etc.) and sends it to a Kafka topic. Each data point includes: A timestamp, A stock ticker and a sentiment score (between -1 and 1), which represents the overall sentiment around the stock.
### 2. Consumer (Consumer_Mhamed.py):
   The consumer listens to the Kafka topic, stores incoming sentiment data in an SQLite database, and visualizes the data using real-time charts. 
  #### The consumer generates:
   - Bar Chart: Displays the current sentiment score for each stock ticker.
   - Line Chart: Shows the sentiment trend over time, smoothed with a moving average.
   - Volatility Chart: Displays the sentiment volatility (standard deviation) for each ticker.
     
## Installation
### Prerequisites
Ensure you have the following installed:

   - WSL (Windows Subsystem for Linux)
   - Apache Kafka
   - Python 3.x

## Running the Pipeline
### 1. Start the Zookeeper "Terminal 1"
   - WSL
   - cd ~/kafka
   - bin/zookeeper-server-start.sh
   - bin/zookeeper-server-start.sh config/zookeeper.properties
### 2. Start the Kafka "Terminal 2"
   - WSL
   - cd ~/kafka
   - bin/kafka-server-start.sh
   - bin/kafka-server-start.sh config/server.properties
   bin/kafka-server-start.sh config/server.properties
### 3. Run the Producer "Terminal 3"
py -m producers.producer_Mhamed

### 4. Run the Consumer "Terminal 4"
py -m consumers.consumer_Mhamed

Before runnung the producer and the consumer be sure that you have installed matplotlib, dotenv and activate the .venv

   - pip install matplotlib
   - pip install python-dotenv
   - .\.venv\Scripts\Activate

## Visualization

The consumer generates an interactive figure with three subplots:
   1.	Sentiment Distribution: A bar chart showing the breakdown of sentiment (positive, neutral, negative) across the data.
   2.	Sentiment Trends: A line chart tracking sentiment over time with a moving average to smooth out fluctuations.
   3.	Sentiment Volatility: A bar chart highlighting the standard deviation of sentiment, indicating periods of high or low volatility.:

![image](https://github.com/user-attachments/assets/acd7e87f-8ce0-41bd-97f9-0776095b9959)

  

## Conclusion
This pipeline demonstrates how you can combine Kafka for real-time data streaming with SQLite for data storage and Matplotlib for dynamic data visualization. It's a useful setup for streaming and visualizing stock sentiment in real-time, providing insights into market trends and sentiment volatility.


