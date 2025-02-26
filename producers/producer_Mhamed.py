import time
import json
import random
from kafka import KafkaProducer
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Kafka configuration
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "buzzline-07-Mhamed")
KAFKA_SERVER = os.getenv("KAFKA_BROKER_ADDRESS", "localhost:9092")

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Sample stock tickers
STOCK_TICKERS = ["INTC", "MSFT", "PFE", "COST", "TSLA", "GOOG", "AAPL"]

# Function to generate mock sentiment data
def generate_sentiment_data():
    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ticker": random.choice(STOCK_TICKERS),
        "headline": f"Stock update for {random.choice(STOCK_TICKERS)}",
        "sentiment_score": round(random.uniform(-1, 1), 2)  # Random sentiment score
    }

# Stream messages continuously
print(f"📡 Streaming stock sentiment data to Kafka topic: {KAFKA_TOPIC}")
while True:
    data = generate_sentiment_data()
    producer.send(KAFKA_TOPIC, data)
    print(f"✅ Sent: {data}")
    time.sleep(10)  # Adjusted frequency to 10 seconds