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

# Sentiment tracking
sentiment_data = {ticker: deque(maxlen=10) for ticker in ["INTC", "MSFT", "PFE", "COST", "TSLA", "GOOG", "AAPL"]}

# Initialize Matplotlib figures
fig1, ax1 = plt.subplots()  # Figure 1: Bar Chart
fig2, ax2 = plt.subplots()  # Figure 2: Line Chart

# Function to calculate moving average
def moving_average(values, window=5):
    if len(values) < window:
        return values
    return np.convolve(values, np.ones(window)/window, mode='valid')

# Function to update line chart (Sentiment Trends with Moving Average)
def update_chart(frame):
    ax2.clear()
    for ticker, scores in sentiment_data.items():
        smoothed_scores = moving_average(list(scores))
        ax2.plot(range(len(smoothed_scores)), smoothed_scores, label=f"{ticker} (MA)")
    
    ax2.legend()
    ax2.set_xlabel("Last Updates")
    ax2.set_ylabel("Sentiment Score (Moving Average)")
    ax2.set_title("Stock Sentiment Trends - Mhamed-")
    ax2.set_ylim(-1, 1)
    ax2.grid()

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
    ax1.set_title("Real-Time Sentiment Distribution -Mhamed-")

# Listen for Kafka messages
print(f"📥 Listening to Kafka topic: {KAFKA_TOPIC}")
for message in consumer:
    data = message.value
    print(f"📊 Received: {data}")

    # Store in database
    cursor.execute("INSERT INTO stock_sentiment (timestamp, ticker, sentiment_score) VALUES (?, ?, ?)",
                   (data["timestamp"], data["ticker"], data["sentiment_score"]))
    conn.commit()

    # Update sentiment tracking
    sentiment_data[data["ticker"]].append(data["sentiment_score"])

    # Start visualizations
    ani1 = animation.FuncAnimation(fig1, update_bar_chart, interval=1000)
    ani2 = animation.FuncAnimation(fig2, update_chart, interval=1000)

    plt.show(block=False)
    plt.pause(0.1)

