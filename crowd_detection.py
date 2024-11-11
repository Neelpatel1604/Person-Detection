import cv2
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BusCrowdDetector:
    def __init__(self, bus_id, capacity_threshold=0.8):
        self.bus_id = bus_id
        self.capacity_threshold = capacity_threshold
        
        # Get email configuration from environment variables
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        
        if not all([self.recipient_email, self.sender_email, self.sender_password]):
            raise ValueError("Email configuration missing in .env file")
            
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
        # Rest of the initialization code remains the same...