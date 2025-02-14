from confluent_kafka import Producer
import os
import base64
import json

# Kafka Configurations
BROKER_ADDRESS = "localhost:9092"
TOPIC_NAME = "custom-image-topic"

# Kafka Producer Configurations
custom_producer = Producer({
    'bootstrap.servers': BROKER_ADDRESS,
    'linger.ms': 10,                    # Longer batching delay
    'batch.num.messages': 3000,         # Messages per batch
    'queue.buffering.max.messages': 15000,  # Increase buffer size
    'compression.type': 'snappy',      
    'acks': 'all'                       
})

# Encode images into Base64
def encode_image(image_file_path):
    with open(image_file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Delivery Callback
def delivery_status(err, msg):
    if err:
        print(f"Delivery failed for {msg.key()}: {err}")
    else:
        print(f"Message successfully delivered to {msg.topic()} [Partition {msg.partition()}]")

# Read Images and Send to Kafka
def send_images_from_directory(directory_path):
    for image_file in os.listdir(directory_path):
        if image_file.lower().endswith((".png", ".jpg", ".jpeg")):
            file_path = os.path.join(directory_path, image_file)
            encoded_image_data = encode_image(file_path)

            kafka_message = json.dumps({
                "image_name": image_file,
                "image_content": encoded_image_data,
            })

            custom_producer.produce(
                TOPIC_NAME, key=image_file, value=kafka_message, callback=delivery_status
            )
            print(f"Sent {image_file} to Kafka.")

    custom_producer.flush()
    print("Finished sending all images.")

if __name__ == "__main__":
    IMAGES_DIR = "/mnt/d/Users/ali.badawy/custom_images"
    send_images_from_directory(IMAGES_DIR)
