import cv2

"""
random functions I use that don't belong in any department
"""

def find_image_dimensions(image_path):
    try:
        im = cv2.imread(image_path)
        return im.shape[:-1]
    except Exception as e:
        print(f"Error in find_image_dimensions: {e}")