from Binarize import run_binarization
from split_image import split_image
from extract_text import run_extraction


def receipt_OCR(receipt_path, store_name):
    # img_file = './imgs/TraderJoesReceipt.jpg'
    
    # Binarize the image
    binarized_file = run_binarization(receipt_path)
    
    # Split the image
    left_output, right_output = split_image(binarized_file)
    
    # Extract text
    result = run_extraction(store_name, receipt_path, right_output)
    return result

def main():
    print("Beginning OCR pipeline")
    img_file = './imgs/KeyFoodsReceipt.jpg'
    receipt_OCR(img_file, "Key Food")



if __name__ == '__main__':
    main()