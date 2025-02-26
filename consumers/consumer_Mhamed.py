import json
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from kafka import KafkaConsumer
from dotenv import load_dotenv
import os
import numpy as np

# Load environment variables
load_dotenv()

# Kafka configuration
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "buzzline-06-Mhamed")
KAFKA_SERVER = os.getenv("KAFKA_BROKER_ADDRESS", "localhost:9092")

# SQLite database setup
DB_FILE = "buzzline-06-Mhamed.sqlite"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_sentiment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    ticker TEXT,
    sentiment_score REAL
)
""")
conn.commit()

# Initialize Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

# Sentiment tracking with timestamps
sentiment_data = {ticker: deque(maxlen=10) for ticker in ["INTC", "MSFT", "PFE", "COST", "TSLA", "GOOG", "AAPL"]}
timestamps_data = {ticker: deque(maxlen=10) for ticker in ["INTC", "MSFT", "PFE", "COST", "TSLA", "GOOG", "AAPL"]}

# Initialize Matplotlib figures
fig1, ax1 = plt.subplots()  # Figure 1: Bar Chart
fig2, ax2 = plt.subplots()  # Figure 2: Line Chart for Sentiment Over Time
fig3, ax3 = plt.subplots()  # Figure 3: Volatility Chart

# Function to calculate moving average
def moving_average(values, window=5):
    if len(values) < window:
        return values
    return np.convolve(values, np.ones(window)/window, mode='valid')

# Function to update line chart (Sentiment Trends with Moving Average)
def update_sentiment_trend(frame):
    ax2.clear()
    for ticker, scores in sentiment_data.items():
        smoothed_scores = moving_average(list(scores))
        ax2.plot(range(len(smoothed_scores)), smoothed_scores, label=f"{ticker} (MA)")

    ax2.legend()
    ax2.set_xlabel("Time (Updates)")
    ax2.set_ylabel("Sentiment Score (Moving Average)")
    ax2.set_title("Sentiment Trends Over Time")
    ax2.set_ylim(-1, 1)
    ax2.grid()

# Function to update volatility chart
def update_volatility_chart(frame):
    ax3.clear()
    for ticker, scores in sentiment_data.items():
        if len(scores) > 1:
            volatility = np.std(scores)  # Standard deviation as volatility measure
            ax3.bar(ticker, volatility, color='purple')

    ax3.set_xlabel("Stock Ticker")
    ax3.set_ylabel("Volatility (Standard Deviation)")
    ax3.set_title("Sentiment Volatility Over Time")
    ax3.set_ylim(0, 1)
    ax3.grid()

# Function to update sentiment bar chart
def update_bar_chart(frame):
    ax1.clear()
    tickers = list(sentiment_data.keys())
    scores = [sentiment_data[t][-1] if sentiment_data[t] else 0 for t in tickers]

    colors = ["green" if s > 0 else "red" for s in scores]
    ax1.bar(tickers, scores, color=colors)
    ax1.set_ylim(-1, 1)
    ax1.set_xlabel("Stock Ticker")
    ax1.set_ylabel("Sentiment Score")
    ax1.set_title("Real-Time Sentiment Distribution")

# Initialize animation
ani1 = animation.FuncAnimation(fig1, update_bar_chart, interval=500)
ani2 = animation.FuncAnimation(fig2, update_sentiment_trend, interval=500)
ani3 = animation.FuncAnimation(fig3, update_volatility_chart, interval=500)

# Start visualizations
plt.show(block=False)

# Listen for Kafka messages
print(f"📥 Listening to Kafka topic: {KAFKA_TOPIC}")

for message in consumer:
    data = message.value
    print(f"📊 Received: {data}")

    # Store in database
    try:
        cursor.execute("INSERT INTO stock_sentiment (timestamp, ticker, sentiment_score) VALUES (?, ?, ?)",
                       (data["timestamp"], data["ticker"], data["sentiment_score"]))
        conn.commit()
    except Exception as e:
        print(f"Error storing data: {e}")

    # Update sentiment tracking and timestamps
    sentiment_data[data["ticker"]].append(data["sentiment_score"])
    timestamps_data[data["ticker"]].append(data["timestamp"])

    plt.pause(0.1)  # This allows real-time updates without blocking