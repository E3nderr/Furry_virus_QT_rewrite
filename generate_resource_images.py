import base64
import os

def generate_base64_code():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {script_dir}")
    
    # Define the assets directory where images are stored
    images_dir = os.path.join(script_dir, 'assets')
    print(f"Assets directory: {images_dir}")
    
    # Check if the assets directory exists
    if not os.path.exists(images_dir):
        print(f"Error: 'assets' directory not found at {images_dir}")
        return

    # Dictionary to hold base64-encoded image data
    image_base64_data = {}

    # Loop through all image files in the 'assets' folder
    for image_name in os.listdir(images_dir):
        image_path = os.path.join(images_dir, image_name)
        
        # Check if the current item is a file and has an image extension
        if os.path.isfile(image_path) and image_name.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            try:
                # Open the image file in binary read mode
                with open(image_path, 'rb') as image_file:
                    # Encode the image data to base64
                    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                    image_base64_data[image_name] = encoded_image
                    print(f"Encoded {image_name}")
            except Exception as e:
                print(f"Error encoding {image_name}: {e}")

    # If no images were encoded, return early
    if not image_base64_data:
        print("No valid images found to encode.")
        return

    # Path to the Python file that will store the base64 data
    resource_file_path = os.path.join(script_dir, 'resource_images.py')
    print(f"Writing base64 data to: {resource_file_path}")

    # Try to write the base64 data to resource_images.py
    try:
        with open(resource_file_path, 'w') as resource_file:
            # Write the dictionary containing base64-encoded image data
            resource_file.write("image_base64_data = {\n")
            for image_name, base64_data in image_base64_data.items():
                resource_file.write(f"    '{image_name}': '{base64_data}',\n")
            resource_file.write("}\n")
        print("resource_images.py has been created successfully.")
    except Exception as e:
        print(f"Failed to write to file: {e}")

# Call the function to generate the base64 code
generate_base64_code()
