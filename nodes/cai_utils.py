import requests
from requests.exceptions import HTTPError
import os
import re

def download_file_with_token(url, params=None, save_path='.'):
    try:
        # Send a GET request to the URL
        with requests.get(url, params=params, stream=True) as response:
            response.raise_for_status()  # Raise an error for bad responses
            print(f"Downloading model successfully from {response.url}")

            # Create temporary file path
            temp_path = save_path + '.download'

            # Write response content to temporary file first
            with open(temp_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            # After successful download, rename temp file to target path
            os.replace(temp_path, save_path)
            
            print(f"File downloaded successfully: {save_path}")
            return True

    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'An error occurred: {err}')
        # Clean up temp file if it exists
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
    return False


def download_cai(model_id, token, lora_path):
    """
    Download a LoRA model from CivitAI directly to the specified lora_path.
    
    :param model_id: The ID of the model to download.
    :param token: The authentication token (optional).
    :param lora_path: The full path (including filename) where the file will be saved.
    :param full_url: Full URL for downloading the model (optional).
    """
    # Ensure the directory of lora_path exists
    directory_path = os.path.dirname(lora_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)

    # Determine the URL for the download
    if not model_id:
        print("Either model_id must be provided for model download.")
        return False
    
    url = f'https://civitai.com/api/download/models/{model_id}'
    params = {'token': token} if token else {}

    # Call the download function and specify the exact file path
    download_success = download_file_with_token(url, params, lora_path)
    if download_success:
        print("File downloaded successfully.")
        return True
    else:
        print("Failed to download the file.")
        return False