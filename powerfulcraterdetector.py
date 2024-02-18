import numpy as np
import cv2
import threading
import time
import pyrebase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard

# Firebase configuration
firebase_config = {
  "apiKey": "AIzaSyBDVDfTYx9_M5XWGPcCttRToGrIX9sAkXI",
  "authDomain": "pragyanrover-a1c17.firebaseapp.com",
  "projectId": "pragyanrover-a1c17",
  "storageBucket": "pragyanrover-a1c17.appspot.com",
  "messagingSenderId": "420377741422",
  "appId": "1:420377741422:web:6be67b3a89469381ffbe7f",
  "databaseURL": "",
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
storage = firebase.storage()

# Function to detect craters in an image and draw bounding boxes around them
def detect_craters(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detect edges using Canny edge detector
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours based on their area in descending order
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]  # Limit to the two largest contours
    
    # Initialize an empty list to store bounding boxes
    bounding_boxes = []
    
    # Iterate over the largest contours and draw bounding boxes around them
    for contour in contours:
        # Calculate the bounding box for the contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Draw bounding box on the original image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Store the bounding box coordinates
        bounding_boxes.append((x, y, w, h))
    
    return image, bounding_boxes

# Function to upload image to Firebase Storage
def upload_to_firebase(filename):
    storage.child("images/" + filename).put(filename)
    print(f"Image uploaded to Firebase Storage: {filename}")

# Function to capture keypresses
def key_capture_thread():
    global frame_counter
    while True:
        if keyboard.is_pressed('esc'):
            # Save the current frame
            frame_counter += 1
            filename = f"frame_{frame_counter}.png"
            cv2.imwrite(filename, frame_with_craters)
            print(f"Frame saved as {filename}")
            upload_to_firebase(filename)  # Upload image to Firebase Storage
            time.sleep(1)  # Delay to prevent multiple saves for a single press
        time.sleep(0.1)

# Initialize Selenium WebDriver (assuming you have the appropriate browser driver installed)
driver = webdriver.Chrome()

# Open the webpage with the Twitch embed
driver.get("http://127.0.0.1:5501/realtimevideo/index.html")

# Use explicit wait to wait for the iframe to be present
wait = WebDriverWait(driver, 20)  # Adjust the timeout as needed
iframe_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#twitch-embed iframe")))

# Switch to the iframe context
driver.switch_to.frame(iframe_element)

# Wait for the video element to be present
video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))

frame_counter = 0

# Start a separate thread to capture key presses
threading.Thread(target=key_capture_thread, daemon=True).start()

while True:
    try:
        # Get the screenshot of the video element
        video_screenshot = video_element.screenshot_as_png

        # Convert the screenshot to OpenCV format
        nparr = np.frombuffer(video_screenshot, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Apply crater detection to the frame
        frame_with_craters, bounding_boxes = detect_craters(frame)

        # Display the resulting frame with craters and bounding boxes
        cv2.imshow("Frame with Craters", frame_with_craters)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    except Exception as e:
        print("Error occurred:", e)
        # Add additional logging or error handling here

# Clean up
cv2.destroyAllWindows()
driver.quit()