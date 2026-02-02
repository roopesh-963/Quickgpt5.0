# app/services/imagekit_service.py
import os
from imagekitio import ImageKit

# Initialize ImageKit with the new SDK structure
imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
    
    
)

def upload_image(file_path: str, file_name: str, folder: str = "/") -> dict:
    with open(file_path, "rb") as file_data:
        response = imagekit.upload_file(
            file=file_data,
            file_name=file_name,
            options={"folder": folder}
        )
    return response
