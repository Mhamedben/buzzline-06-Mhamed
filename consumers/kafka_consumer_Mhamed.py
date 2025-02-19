import json
import os
import pathlib
import sys
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

from kafka import KafkaConsumer
import utils.utils_config as config
from utils.utils_consumer import create_kafka_consumer
from utils.utils_logger import logger
from utils.utils_producer import verify_services, is_topic_available

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from consumers.db_sqlite_case import init_db, insert_message

# Store sentiment data for visualizations
author_sentiment_scores = defaultdict(list)  # Store sentiment scores for each author
average_sentiment_by_author = {}
all_sentiment_scores = []  # List to store all sentiment scores for distribution

# CSV file for storing sentiment analysis data
sentiment_data_file = "author_sentiment_data.csv"

# Initialize Matplotlib interactive plot with two subplots (ax1 for avg sentiment, ax2 for distribution)
plt.ion()  # Interactive mode on
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

def update_visualizations():
    """
    Update visualizations dynamically with new data.
    """
    # Clear previous plots
    ax1.clear()
    ax2.clear()

    # Bar Chart for Average Sentiment Score by Author
    if average_sentiment_by_author:
        authors, avg_sentiments = zip(*average_sentiment_by_author.items())
        ax1.bar(authors, avg_sentiments, color='blue')
        ax1.set_title("Average Sentiment Score by Authors -Mhamed-")
        ax1.set_ylabel("Average Sentiment Score")
        ax1.set_xticklabels(authors, rotation=65, ha="left")

    # Histogram for Sentiment Score Distribution
    ax2.hist(all_sentiment_scores, bins=20, color='yellow', edgecolor='black')
    ax2.set_title("Sentiment Score Distribution -Mhamed-")
    ax2.set_xlabel("Sentiment Score")
    ax2.set_ylabel("Frequency")

    # Draw updated plot
    plt.draw()
    plt.pause(0.5)  # Pause to update the plot

def process_message(message: dict) -> None:
    """
    Process a single JSON message and update data for sentiment analysis.
    Store sentiment data in a CSV file.
    """
    try:
        processed_message = {
            "message": message.get("message"),
            "author": message.get("author"),
            "timestamp": message.get("timestamp"),
            "category": message.get("category"),
            "sentiment": float(message.get("sentiment", 0.0)),
            "keyword_mentioned": message.get("keyword_mentioned"),
            "message_length": int(message.get("message_length", 0)),
        }

        # Update author sentiment scores
        author_sentiment_scores[processed_message["author"]].append(processed_message["sentiment"])

        # Update all sentiment scores for distribution
        all_sentiment_scores.append(processed_message["sentiment"])

        # Update the visualizations with the new data
        update_visualizations()

        # Calculate and update average sentiment by author
        for author, sentiments in author_sentiment_scores.items():
            average_sentiment_by_author[author] = sum(sentiments) / len(sentiments)

        # Store sentiment data in CSV
        store_sentiment_data(processed_message)

        return processed_message
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return None

def store_sentiment_data(message: dict) -> None:
    """
    Store sentiment data (author, sentiment score) in the CSV file.
    """
    try:
        # Check if the CSV file exists, if not create it with headers
        if not os.path.exists(sentiment_data_file):
            with open(sentiment_data_file, mode='w', newline='', encoding='utf-8') as file:
                file.write("message,author,timestamp,category,sentiment,keyword_mentioned,message_length\n")

        # Append the sentiment data to the CSV file
        with open(sentiment_data_file, mode='a', newline='', encoding='utf-8') as file:
            file.write(f'"{message["message"]}","{message["author"]}","{message["timestamp"]}","{message["category"]}",{message["sentiment"]},"{message["keyword_mentioned"]}",{message["message_length"]}\n')

        logger.info(f"Stored sentiment data: {message['message']}")

    except Exception as e:
        logger.error(f"Error storing sentiment data in CSV: {e}")

def consume_messages_from_kafka(topic, kafka_url, group, sql_path, interval_secs):
    """
    Consume new messages from Kafka topic and process them.
    """
    try:
        verify_services()
        consumer = create_kafka_consumer(
            topic, group, value_deserializer_provided=lambda x: json.loads(x.decode("utf-8"))
        )
        is_topic_available(topic)
    except Exception as e:
        logger.error(f"ERROR: Kafka initialization failed: {e}")
        sys.exit(11)

    if consumer is None:
        logger.error("ERROR: Consumer is None. Exiting.")
        sys.exit(13)

    try:
        for message in consumer:
            processed_message = process_message(message.value)
            if processed_message:
                insert_message(processed_message, sql_path)

    except Exception as e:
        logger.error(f"ERROR: Could not consume messages from Kafka: {e}")
        raise

def main():
    """
    Main function to run the consumer process.
    """
    try:
        topic = config.get_kafka_topic()
        kafka_url = config.get_kafka_broker_address()
        group_id = config.get_kafka_consumer_group_id()
        interval_secs = config.get_message_interval_seconds_as_int()
        sqlite_path = config.get_sqlite_path()
    except Exception as e:
        logger.error(f"ERROR: Failed to read environment variables: {e}")
        sys.exit(1)

    if sqlite_path.exists():
        try:
            sqlite_path.unlink()
        except Exception as e:
            logger.error(f"ERROR: Failed to delete DB file: {e}")
            sys.exit(2)

    try:
        init_db(sqlite_path)
    except Exception as e:
        logger.error(f"ERROR: Failed to create db table: {e}")
        sys.exit(3)

    try:
        consume_messages_from_kafka(topic, kafka_url, group_id, sqlite_path, interval_secs)
    except KeyboardInterrupt:
        logger.warning("Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("Consumer shutting down.")

if __name__ == "__main__":
    main()