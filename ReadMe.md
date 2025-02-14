# **Kafka-Based Image Processing Pipeline**

## **Overview**

This project demonstrates a Kafka-based pipeline for processing image files. It includes a Kafka Producer that reads images from a directory, encodes them in Base64, and sends them to a Kafka topic. The Kafka Consumer retrieves the images, decodes them, saves them locally, and logs metadata in a CSV file.

## **Project Structure**

├── `producer.py`        # Kafka Producer: Reads images, encodes them, and sends them to Kafka  
├── `consumer.py`        # Kafka Consumer: Receives images, decodes, and saves them  
├── `docker-compose.yml` # Docker Compose setup for Kafka services  
├── `processed_image_data.csv` # CSV log of processed images

## **Dependencies**

Ensure you have the following installed:

* Python 3.8+  
* `confluent_kafka` for Kafka communication  
* `pandas` for data handling

Install dependencies using:
```bash
pip install confluent_kafka pandas
```
## **Kafka Setup Using Docker Compose**

The project uses a single-node Kafka cluster set up via Docker Compose.

### **Start Kafka**

Run the following command to start the Kafka broker and control center:
```bash
docker compose up -d
```
This will launch:

* Kafka broker (listening on `localhost:9092`)  
* Confluent Control Center (accessible at `http://localhost:9021`)

### **Stop Kafka**

To stop the services, run:
```bash
docker compose down
```
## **Running the Producer**

The producer reads image files from a specified directory and publishes them to Kafka.

1. Update the `IMAGES_DIR` variable in `producer.py` to point to your images directory.  
2. Run the producer:

python producer.py

## **Running the Consumer**

The consumer retrieves images from Kafka, decodes them, and stores them locally.

1. Run the consumer:

python consumer.py

2. Processed images will be saved in the `processed_images/` directory.  
3. A CSV log will be created at `processed_image_data.csv`.

## **Configuration Details**

### **Kafka Producer (`producer.py`)**

* Reads images from the specified directory.  
* Encodes images in Base64 and sends them to Kafka.  
* Uses batching (`batch.num.messages`) and compression (`snappy`) for efficiency.

### **Kafka Consumer (`consumer.py`)**

* Subscribes to the Kafka topic and listens for messages.  
* Decodes Base64-encoded images and saves them to a local directory.  
* Logs metadata (file paths and labels) in a CSV file.

### **Kafka Docker Compose Configuration**

* Broker (`broker` service) listens on `localhost:9092`.  
* Confluent Control Center (`http://localhost:9021`) provides a web UI to monitor Kafka.

## **Monitoring Kafka Messages**

You can inspect the Kafka topic with the following commands:

### **List Topics**
```bash
docker exec -it broker kafka-topics --list --bootstrap-server broker:29092
```
### **Read Messages from Topic**
```bash
docker exec -it broker kafka-console-consumer --bootstrap-server broker:29092 --topic custom-image-topic --from-beginning
```
## **Troubleshooting**

* If the producer fails to connect, ensure the Kafka broker is running.  
* If the consumer does not receive messages, verify the topic name in both scripts.  
* Check `docker logs broker` for any Kafka-related issues.


