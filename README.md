# New Consumer: Kafka_consumer_Mhamed.py

The newly added consumer focuses on sentiment analysis messages. It consumes JSON messages that are produced by a Kafka producer.

## Specifically, this consumer:

 - Extracts the sentiment score of each message (a value between -1 and 1).
 - Calculates the average sentiment score for each author over time.
 - Stores sentiment data in a CSV file for each incoming message.
 - Visualizes sentiment data using real-time plotting:
   - 1-Average sentiment score by author: A bar chart displaying the average sentiment for each author.
   - 2-Sentiment score distribution: A histogram showing the overall sentiment score distribution.
     
This consumer processes each message individually, stores its sentiment, and updates the visualizations dynamically.

## Instructions

### 1. Clone the Repository

Clone this repository to your local machine: git clone https://github.com/drodmay1/buzzline-05-Mhamed

### 2. Create a Virtual Environment:
source .venv/bin/activate
### 3. Install Dependencies:
pip install -r requirements.txt`
### 4. Start Kafka and Zookeeper:
  - Start Zookeeper (Terminal 1)
      - WSL
      - ./bin/zookeeper-server-start.sh
      - ./bin/zookeeper-server-start.sh config/zookeeper.properties
   - Start Kafka (Terminal 2)
      - WSL
      - ./bin/kafka-server-start.sh
      - ./bin/kafka-server-start.sh config/server.properties

### Run Producer (Terminal 3) 
Start the producer to generate the messages. 
```shell
.venv\Scripts\activate
py -m producers.producer_case
```

### Run the Consumer (Terminal 4) 

```shell
.venv\Scripts\activate
py -m consumers.kafka_consumer_Mhamed
```

### Custom Kafka Consumer
For each incoming message, the consumer:
 1. Extracts sentiment data (sentiment score) and stores it for the author of the message.
 2. Tracks the sentiment of messages over time, visualizing the average sentiment per author and the overall sentiment distribution.

### Visualization
The consumer updates two types of visualizations dynamically:
1. **Average Sentiment Score by Author**: A bar chart displaying the average sentiment score for each author.
2. **Sentiment Score Distribution**: A histogram displaying the distribution of sentiment scores across all messages.

These visualizations are updated in real-time as new messages are consumed.

