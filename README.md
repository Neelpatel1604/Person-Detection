# Bus Crowd Detection System

A real-time computer vision system that detects people in buses and sends email notifications for crowd monitoring. Built with OpenCV and YOLOv4-tiny for efficient person detection.

## 🚀 Features

- Real-time person detection using YOLOv4-tiny
- Email notifications when people are detected
- SQLite database for storing detection data
- Visual display with bounding boxes and confidence scores
- Configurable notification cooldown period
- Environment variable support for secure credential management

## 📋 Prerequisites

- Python 3.7 or higher
- Webcam or IP camera
- Gmail account with App Password enabled
- Git (for cloning the repository)

## 🛠️ Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/bus-crowd-detection.git
```

2. Install required packages:
```     
cd bus-crowd-detection
pip install -r requirements.txt
```

3. Create `.env` file with your email credentials:
```
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient_email@example.com
```

4. Download YOLOv4-tiny weights:
   - Create a `models` folder
   - Download [yolov4-tiny.weights](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights)
   - Place it in the `models` folder

## 🎮 Usage

1. Run the program:
```
python main.py
```

2. Controls:
   - Press 'q' to quit
   - Detection runs automatically
   - Notifications are sent when people are detected

## 📊 Features in Detail

### Person Detection
- Uses YOLOv4-tiny for efficient detection
- Shows confidence scores for each detection
- Draws bounding boxes around detected people

### Email Notifications
- Sends alerts when people are detected
- Configurable cooldown period
- Uses secure Gmail App Password

### Database Storage
- Stores all detections in SQLite
- Records timestamp, count, and occupancy rate
- Enables historical data analysis

## 🔧 Troubleshooting

### Common Issues:
1. Email not sending:
   - Check Gmail App Password
   - Verify internet connection
   - Confirm .env file setup

2. Detection not working:
   - Verify camera connection
   - Check model files in models/
   - Ensure proper lighting

3. Database errors:
   - Check write permissions
   - Verify SQLite installation

## 📁 Project Structure

- `main.py`: Main program
- `crowd_detection.py`: Crowd detection logic
- `db_handler.py`: Database operations
- `requirements.txt`: Required packages
- `.env`: Environment variables

## 🔒 Security Notes
- Never share your .env file
- Use App Passwords, not account passwords
- Keep model files secure

## 🤝 Contributing
Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request

## 📫 Support
For help:
- Open an issue
- Email: neel_patel2004@outlook.com

## 📜 License
MIT License - feel free to use and modify
