import cv2
import numpy as np

# Load Haar cascade models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Number of neighbors for smile detection
neighbors = 30

# Open the webcam
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()  # Read frame from the webcam

    if not ret:
        print("Failed to capture video frame. Exiting...")
        break

    # Convert frame to grayscale
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Extract face region
        the_face = frame[y:y + h, x:x + w]

        # Convert the face region to grayscale
        face_grayscale = cv2.cvtColor(the_face, cv2.COLOR_BGR2GRAY)

        # Detect smiles within the face region
        smiles = smile_cascade.detectMultiScale(face_grayscale, scaleFactor=1.7, minNeighbors=neighbors)

        if len(smiles) > 0:
            # Add "smiling" text
            cv2.putText(frame, 'Smiling', (x, y + h + 40), fontScale=2, fontFace=cv2.FONT_HERSHEY_PLAIN, color=(255, 255, 255), thickness=2)

    # Add an "Exit" button to the frame
    cv2.rectangle(frame, (10, 10), (110, 60), (0, 0, 255), -1)  # Button background
    cv2.putText(frame, "Exit", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display the frame
    cv2.imshow("Smile Detector", frame)

    # Check for mouse click on "Exit" button
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if 10 <= x <= 110 and 10 <= y <= 60:
                print("Exit button clicked!")
                video.release()
                cv2.destroyAllWindows()
                exit()

    cv2.setMouseCallback("Smile Detector", mouse_callback)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# Release resources
video.release()
cv2.destroyAllWindows()
