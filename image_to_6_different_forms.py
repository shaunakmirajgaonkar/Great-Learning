import cv2

# Load the original image
image_path = '/Users/shaunak/Desktop/image.jpg'
image = cv2.imread('/Users/shaunak/Desktop/image.jpg')

# Check if the image is loaded successfully
if image is None:
    print("Error: Unable to load the image.")
    exit()

# Transformations (as before)
grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(image, (15, 15), 0)
edges_image = cv2.Canny(image, 100, 200)
_, binary_image = cv2.threshold(grayscale_image, 128, 255, cv2.THRESH_BINARY)
resized_image = cv2.resize(image, (200, 200))
height, width = image.shape[:2]
center = (width // 2, height // 2)
rotation_matrix = cv2.getRotationMatrix2D(center, 90, 1.0)
rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

# List of all the images
images = [
    ("Original Image", image),
    ("Grayscale Image", grayscale_image),
    ("Blurred Image", blurred_image),
    ("Edges Image", edges_image),
    ("Binary Image", binary_image),
    ("Resized Image", resized_image),
    ("Rotated Image", rotated_image)
]

# Initialize index for images
index = 0

# Function to display image with a title
def display_image(index):
    title, img = images[index]
    cv2.imshow(title, img)

# Display the first image
display_image(index)

# Wait for user to press an arrow key
while True:
    key = cv2.waitKey(0)  # Get the key press

    # If the right arrow key is pressed (macOS key code 83), move to the next image
    if key == 83:  # Right arrow key
        index = (index + 1) % len(images)  # Move to next image, loop back if at the end
        display_image(index)

    # If the left arrow key is pressed (macOS key code 81), move to the previous image
    elif key == 81:  # Left arrow key
        index = (index - 1) % len(images)  # Move to previous image, loop back if at the start
        display_image(index)

    # If 'q' is pressed, exit the loop and close windows
    elif key == ord('q'):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
