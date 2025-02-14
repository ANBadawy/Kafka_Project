from confluent_kafka import Consumer
import json
import pandas as pd
import base64
import os

# Kafka Consumer Configurations
consumer_settings = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'custom_img_consumer_group',
    'auto.offset.reset': 'earliest'  # Start from the earliest messages
}

# Initialize Kafka Consumer
custom_consumer = Consumer(consumer_settings)

# Subscribe to Kafka Topic
TOPIC = "custom-image-topic"
custom_consumer.subscribe([TOPIC])

# Output Directories
SAVED_IMAGE_DIR = "processed_images"
os.makedirs(SAVED_IMAGE_DIR, exist_ok=True)

# Message Collector for CSV Output
image_records = []

print("Waiting for messages...")

try:
    while True:
        message = custom_consumer.poll(1.0)  # Poll messages for up to 1 second
        if message is None:
            continue
        if message.error():
            print(f"Consumer error: {message.error()}")
            continue

        # Deserialize the Kafka Message
        msg_value = json.loads(message.value().decode('utf-8'))
        print(f"Message Received: {msg_value}")

        # Extract Data
        img_filename = msg_value.get("image_name")
        img_encoded_data = msg_value.get("image_content")

        # Save Image Locally
        img_file_path = os.path.join(SAVED_IMAGE_DIR, f"custom_{img_filename}")
        with open(img_file_path, "wb") as img_file:
            img_file.write(base64.b64decode(img_encoded_data))

        # Store Data for CSV Output
        image_records.append({
            "file_path": img_file_path,
            "image_label": img_filename,
        })

        # Optional Stop Condition
        if len(image_records) >= 5000:  # Adjust limit as needed
            break

except KeyboardInterrupt:
    print("Consumer process interrupted.")
finally:
    # Close the Consumer
    custom_consumer.close()

# Save Consumed Data to CSV
df = pd.DataFrame(image_records)
OUTPUT_CSV = "processed_image_data.csv"
df.to_csv(OUTPUT_CSV, index=False)
print(f"Data saved to {OUTPUT_CSV}")
