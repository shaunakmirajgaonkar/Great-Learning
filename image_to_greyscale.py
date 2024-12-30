import cv2

# Load the image
image_path = '/Users/shaunak/Desktop/image.jpg'
image = cv2.imread('/Users/shaunak/Desktop/image.jpg')

# Check if the image is loaded successfully
if image is None:
    print("Error: Unable to load the image.")
    exit()

# Convert the image to grayscale
grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the original and grayscale images
cv2.imshow("Original Image", image)
cv2.imshow("Grayscale Image", grayscale_image)

# Save the grayscale image
output_path = 'grayscale_image.jpg'  # Replace with your desired output path
cv2.imwrite(output_path, grayscale_image)
print(f"Grayscale image saved to {output_path}")

# Wait for a key press and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()
