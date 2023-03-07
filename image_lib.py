from apod_api import get_apod_image_url, get_apod_info
import requests
import re, os, ctypes, random

'''
Library of useful functions for working with images.
'''
def main():
    # TODO: Add code to test the functions in this module
    #apod_date = "2021-08-25" # Video File.
    apod_date = '2021-05-04'
    apod_info_dict = get_apod_info(apod_date)
    image_url = get_apod_image_url(apod_info_dict)
    pass
    image_data = download_image(image_url)
    image_path = save_image_file(image_data, r"C:\temp\images")
    set_desktop_background_image(image_path)



    return

def download_image(image_url):
    """Downloads an image from a specified URL.

    DOES NOT SAVE THE IMAGE FILE TO DISK.

    Args:
        image_url (str): URL of image

    Returns:
        bytes: Binary image data, if succcessful. None, if unsuccessful.
    """
    # TODO: Complete function body
    # Send get request to download file
    resp_msg = requests.get(image_url)
    # Check whether the download was successfull
    if resp_msg.status_code == requests.codes.ok:
        # Extract Binary file content from response message body.
        image_data = resp_msg.content
        return image_data
    else:
        print(f'Failed to download file \n {resp_msg.status_code} {resp_msg.reason}')

def save_image_file(image_data, image_path,):
    """Saves image data as a file on disk.
    
    DOES NOT DOWNLOAD THE IMAGE.

    Args:
        image_data (bytes): Binary image data
        image_path (str): Path to save image file

    Returns:
        bytes: True, if succcessful. False, if unsuccessful
    """
    # TODO: Complete function body
    # Set Directory and file path
    file_path ='newpic.jpg'
    installer_path = os.path.join(image_path, file_path)
    if not os.path.isdir(image_path):
        os.makedirs(image_path)
    with open(installer_path, 'wb') as file:
        file.write(image_data)
        return installer_path


def set_desktop_background_image(image_path):
    """Sets the desktop background image to a specific image.

    Args:
        image_path (str): Path of image file

    Returns:
        bytes: True, if succcessful. False, if unsuccessful        
    """
    # TODO: Complete function body
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    return

def scale_image(image_size, max_size=(800, 600)):
    """Calculates the dimensions of an image scaled to a maximum width
    and/or height while maintaining the aspect ratio  

    Args:
        image_size (tuple[int, int]): Original image size in pixels (width, height) 
        max_size (tuple[int, int], optional): Maximum image size in pixels (width, height). Defaults to (800, 600).

    Returns:
        tuple[int, int]: Scaled image size in pixels (width, height)
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    # NOTE: This function is only needed to support the APOD viewer GUI
    resize_ratio = min(max_size[0] / image_size[0], max_size[1] / image_size[1])
    new_size = (int(image_size[0] * resize_ratio), int(image_size[1] * resize_ratio))
    return new_size

if __name__ == '__main__':
    main()