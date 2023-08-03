from PIL import Image

def split_image(image_path):
    # Open the image using PIL
    img = Image.open(image_path)

    # Get the width and height of the original image
    width, height = img.size

    # Calculate the split point based on the left 75% and right 25% division
    split_point = int(width * 0.75)

    # Split the image into two images
    left_image = img.crop((0, 0, split_point, height))
    right_image = img.crop((split_point, 0, width, height))

    left_output = 'imgs/left_image.jpg'
    right_output = 'imgs/right_image.jpg'
    
    left_image.save(left_output)
    right_image.save(right_output)

    return left_output, right_output

# # Replace 'your_image_path.jpg' with the path of the image you want to split
# image_path = 'imgs/BinarizedReceipt.jpg'

# # Call the split_image function to get the two split images
# left_image, right_image = split_image(image_path)

# # Save the split images

