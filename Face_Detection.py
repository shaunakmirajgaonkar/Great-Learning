import cv2

# Load the pre-trained Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the webcam
video = cv2.VideoCapture(0)  # Use 0 for default webcam

if not video.isOpened():
    print("Error: Could not access the webcam.")
    exit()

print("Press 'q' to quit the program.")

while True:
    # Read frame from the webcam
    ret, frame = video.read()
    if not ret:
        print("Error: Unable to capture frame from the webcam.")
        break

    # Convert the frame to grayscale
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue rectangle with thickness 2

    # Display the output frame
    cv2.imshow("Face Detection", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close OpenCV windows
video.release()
cv2.destroyAllWindows()
