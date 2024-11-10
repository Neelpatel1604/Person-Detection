import cv2
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import time

class BusCrowdDetector:
    def __init__(self, bus_id, capacity_threshold=0.8):
        self.bus_id = bus_id
        self.capacity_threshold = capacity_threshold
        self.recipient_email = "Email that you want to send notification"
        
        # Updated Email configuration 
        self.sender_email = "your email"  # Changed to your  email
        self.sender_password = "Your gogle password"    # Put your password here
        self.smtp_server = "smtp.gmail.com"        # Changed  SMTP server
        self.smtp_port = 587
        self.max_retries = 3  # Number of times to retry sending email
        self.last_notification_time = 0  # To prevent too frequent notifications
        self.notification_cooldown = 30  # Seconds between notifications
        
        # Model paths
        model_dir = os.path.join(os.path.dirname(__file__), 'models')
        config_path = os.path.join(model_dir, 'yolov4-tiny.cfg')
        weights_path = os.path.join(model_dir, 'yolov4-tiny.weights')
        names_path = os.path.join(model_dir, 'coco.names')
        
        # Check if model files exist
        if not all(os.path.exists(f) for f in [config_path, weights_path, names_path]):
            raise FileNotFoundError(
                "Model files not found. Please ensure yolov4-tiny.cfg, "
                "yolov4-tiny.weights, and coco.names are in the 'models' directory."
            )
        
        # Load YOLOv4-tiny
        self.net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        
        # Load class names
        with open(names_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        
    def detect_people(self, frame):
        height, width = frame.shape[:2]
        
        # Create blob from image
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        
        # Get detections
        outputs = self.net.forward(self.output_layers)
        
        # Initialize lists for detected people
        boxes = []
        confidences = []
        
        # Process detections
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                # Filter for people (class 0 in COCO dataset) with confidence > 0.5
                if class_id == 0 and confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
        
        # Apply non-maximum suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        people_count = len(indices)
        
        # Draw boxes for detected people
        for i in indices:
            box = boxes[i]
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f'Person {confidences[i]:.2f}', (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return people_count, frame
    
    def check_crowding(self, people_count, bus_capacity=50):
        # Modified to send notification if at least 1 person is detected
        if people_count >= 1:  # Changed from checking occupancy_rate
            self.send_notification(people_count, people_count/bus_capacity)
            
    def send_notification(self, count, occupancy_rate):
        # Check if enough time has passed since last notification
        current_time = time.time()
        if current_time - self.last_notification_time < self.notification_cooldown:
            print("Skipping notification - cooldown period")
            return

        subject = f"Person Detected - Bus {self.bus_id}"
        body = f"""
        Person Detection Alert!
        
        Bus ID: {self.bus_id}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Number of People Detected: {count}
        
        This is a test notification from the Bus Crowd Detection System.
        """
        
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        for attempt in range(self.max_retries):
            try:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)  # Added timeout
                server.starttls()
                
                print(f"Attempting to login (attempt {attempt + 1}/{self.max_retries})...")
                server.login(self.sender_email, self.sender_password)
                
                print("Sending email...")
                server.send_message(msg)
                print("Email sent successfully")
                
                server.quit()
                self.last_notification_time = current_time
                print(f"Test notification sent: {count} people detected")
                return  # Success - exit the function
                
            except smtplib.SMTPAuthenticationError as e:
                print(f"Authentication failed: Please check your email and password")
                break  # Don't retry on authentication errors
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    print(f"Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print("Max retries reached. Continuing without sending notification.")