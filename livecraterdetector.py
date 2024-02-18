from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
import numpy as np
import io
from PIL import Image

def detect_shapes(image, min_radius=10, max_radius=100):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detect circles using Hough Circle Transform
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                               param1=100, param2=30, minRadius=min_radius, maxRadius=max_radius)
    
    # Find contours in the image
    contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            x, y, radius = circle[0], circle[1], circle[2]
            # Draw circles only if they are reasonably sized
            if radius > min_radius and radius < max_radius:
                cv2.circle(image, (x, y), radius, (0, 255, 0), 2)
                cv2.rectangle(image, (x - radius, y - radius), (x + radius, y + radius), (0, 255, 0), 2)
    
    # Draw detected ellipses
    for contour in contours:
        if len(contour) >= 5:
            ellipse = cv2.fitEllipse(contour)
            (x, y), (MA, ma), angle = ellipse
            # Draw ellipses only if their major and minor axes are reasonably sized
            if MA > min_radius and MA < max_radius and ma > min_radius and ma < max_radius:
                cv2.ellipse(image, (x, y), (MA, ma), angle, 0, 360, (0, 255, 0), 2)
    
    return image

# Initialize Selenium WebDriver (assuming you have the appropriate browser driver installed)
driver = webdriver.Chrome()

# Open the webpage with the Twitch embed
driver.get("http://127.0.0.1:5500/index.html")

# Use explicit wait to wait for the iframe to be present
wait = WebDriverWait(driver, 20)  # Adjust the timeout as needed
iframe_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#twitch-embed iframe")))

# Switch to the iframe context
driver.switch_to.frame(iframe_element)

# Wait for the video element to be present
video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))

# Main loop to capture frames
while True:
    try:
        # Get the screenshot of the video element
        video_screenshot = video_element.screenshot_as_png
        
        # Convert the screenshot to OpenCV format
        pil_image = Image.open(io.BytesIO(video_screenshot))
        frame = np.array(pil_image)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Apply shape detection to the frame
        frame_with_shapes = detect_shapes(frame)
        
        # Display the resulting frame with shapes and bounding boxes
        cv2.imshow("Frame with Shapes", frame_with_shapes)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print("Error occurred:", e)
        # Add additional logging or error handling here

# Clean up
cv2.destroyAllWindows()
driver.quit()
