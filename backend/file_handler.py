from PIL import Image
from PIL.ExifTags import TAGS
import os

def load_photos_from_directory(directory):
    """Load image files from a directory and return their data."""
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    images = []  # Store image data as a list of dictionaries

    for file_name in os.listdir(directory):
        if file_name.lower().endswith(supported_formats):
            #creates the proper path using .path.join
            file_path = os.path.join(directory, file_name)
            
            try:
                # Open the image
                image = Image.open(file_path)
                # Generate a thumbnail
                thumbnail = image.copy()
                thumbnail.thumbnail((150, 150))  # Resize to a max of 150x150
                
                # Store image data
                images.append({
                    "file_path": file_path,
                    "image": image,  # Original image
                    "thumbnail": thumbnail  # Smaller version
                })
            except Exception as e:
                print(f"Error loading {file_name}: {e}")

    return images

def get_metadata(image_path):
    """ Extracts EXIF metadata from an image and formats it into a string. """
    image = Image.open(image_path)
    exif_data = image._getexif()
    
    if exif_data is not None:
        metadata = ""
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            metadata += f"{tag_name}: {value}\n"
        return metadata
    else:
        return "No EXIF metadata found."