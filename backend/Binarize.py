from PIL import Image
import numpy as np

def binarize_image(image_array, threshold):
    # Convert the image array to grayscale if it's a color image
    if len(image_array.shape) == 3:
        image_array = np.mean(image_array, axis=2).astype(np.uint8)

    # Binarize the image based on the threshold
    binarized_image = np.where(image_array > threshold, 255, 0).astype(np.uint8)
    return binarized_image

def run_binarization(filename):

    # Read the image into memory
    img = np.array(Image.open(filename))

    # Define the threshold value (0 to 255)
    threshold_value = 150

    # Binarize the image with the given threshold
    binarized_image = binarize_image(img, threshold_value)

    # Save the binarized image
    binarized_img = Image.fromarray(binarized_image)
    output_file = './imgs/Binarized.jpg'
    binarized_img.save(output_file)

    return output_file

# Optionally, you can display the original and binarized images using matplotlib
# import matplotlib.pyplot as plt

# plt.subplot(1, 2, 1)
# plt.imshow(pricesImg, cmap='gray')
# plt.title('Original Image')

# plt.subplot(1, 2, 2)
# plt.imshow(binarized_image, cmap='gray')
# plt.title('Binarized Image')

# plt.savefig("Binarised" + prices_img_file)
