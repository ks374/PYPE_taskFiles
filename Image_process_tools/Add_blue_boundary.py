import os
from PIL import Image, ImageOps

def add_blue_border_to_images(input_folder, output_folder, border_thickness=10):
    """
    Reads all images from an input folder, adds a blue border,
    and saves them to an output folder.

    Args:
        input_folder (str): Path to the folder containing source images.
        output_folder (str): Path to the folder where processed images will be saved.
        border_thickness (int): The thickness of the border in pixels. Default is 10.
    """
    
    # --- 1. Create Output Directory ---
    # Ensure the output directory exists, create it if it doesn't
    os.makedirs(output_folder, exist_ok=True)
    print(f"Output will be saved to: {output_folder}")

    # --- 2. Check Input Directory ---
    if not os.path.isdir(input_folder):
        print(f"Error: Input folder not found at {input_folder}")
        print("Please create it and add some images.")
        return

    # Define common image file extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')

    # --- 3. Process Each Image ---
    processed_count = 0
    for filename in os.listdir(input_folder):
        # Check if the file is an image by its extension
        if filename.lower().endswith(image_extensions):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                # Open the image
                with Image.open(input_path) as img:
                    # Add the border using ImageOps.expand
                    # 'fill' can be a color name (like 'blue') or an (R, G, B) tuple
                    img_with_border = ImageOps.expand(
                        img, 
                        border=border_thickness, 
                        fill='blue'
                    )
                    
                    # Save the new image to the output folder
                    img_with_border.save(output_path)
                    print(f"Processed: {filename}")
                    processed_count += 1

            except Exception as e:
                print(f"Failed to process {filename}: {e}")

    if processed_count == 0:
        print(f"No images found in {input_folder}. Please add some images to process.")
    else:
        print(f"\nSuccessfully processed {processed_count} images.")
        print(f"Check the results in: {output_folder}")


# --- Main execution ---
if __name__ == "__main__":
    
    # --- Configuration ---
    BORDER_SIZE = 10  # You can change this value
    
    # 1. Set up a test folder and a sample image
    INPUT_DIR = "E:\\File\\Work\\2025\\PYPE_taskFiles\\Image_process_tools\\Image_test\\"
    OUTPUT_DIR = "E:\\File\\Work\\2025\\PYPE_taskFiles\\Image_process_tools\\Image_test_output\\"

    # 2. Run the main function
    print("\nStarting image processing...")
    add_blue_border_to_images(INPUT_DIR, OUTPUT_DIR, border_thickness=BORDER_SIZE)
    
    # --- Example with a different thickness ---
    # You can uncomment this to run another pass with a thicker border
    
    # print("\nStarting second pass with 25px border...")
    # OUTPUT_DIR_THICK = "output_images_thick_border"
    # add_blue_border_to_images(INPUT_DIR, OUTPUT_DIR_THICK, border_thickness=25)