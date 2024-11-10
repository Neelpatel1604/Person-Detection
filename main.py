import cv2
from crowd_detection import BusCrowdDetector
import time
from db_handler import CrowdingDatabase

def main():
    # Initialize camera (0 for default camera, or IP camera URL)
    cap = cv2.VideoCapture(0)
    
    # Initialize detector and database
    detector = BusCrowdDetector(bus_id="BT123")
    db = CrowdingDatabase()
    
    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
                
            # Detect people in frame
            people_count, annotated_frame = detector.detect_people(frame)
            
            # Check if crowding threshold is exceeded
            try:
                detector.check_crowding(people_count)
            except Exception as e:
                print(f"Notification error: {e}")
            
            # Log to database
            try:
                db.log_crowding(detector.bus_id, people_count, people_count/50)
            except Exception as e:
                print(f"Database error: {e}")
            
            # Add overlay to frame showing count
            cv2.putText(annotated_frame, f"People: {people_count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow('Bus Crowd Detection', annotated_frame)
            
            # Break loop with 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Reduced sleep time for more responsive detection
            time.sleep(0.1)  # Changed from 1 second to 0.1 seconds
            
        except KeyboardInterrupt:
            print("\nStopping the program...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            continue
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 