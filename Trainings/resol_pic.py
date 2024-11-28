from PIL import Image
import numpy as np

def reduce_resolution(image_path, output_path, reduction_factor=2):
    """
    Reduces the resolution of an image without losing its form.

    :param image_path: Path to the input image
    :param output_path: Path to save the output image
    :param reduction_factor: Factor by which to reduce resolution (default: 2)
    """
    # Open the image
    img = Image.open(image_path)
    
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Downsample the array
    reduced_array = img_array[::reduction_factor, ::reduction_factor]
    
    # Convert the numpy array back to an image
    reduced_img = Image.fromarray(reduced_array.astype('uint8'))
    
    # Save the resized image
    reduced_img.save(output_path)
    print(f"Reduced resolution image saved to {output_path}")

# Example usage
input_image = "wallpapersden.com_lamborghini_3840x2160.jpg"
output_image = "reduced_image.jpg.jpg"
reduce_resolution(input_image, output_image, reduction_factor=2)
