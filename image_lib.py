"""--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 --------------------

Library of useful functions for working with images.


--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 -------------------- """
from apod_api import get_apod_image_url, get_apod_info
import requests
import os, ctypes, random, string, struct

def main():
    
    # apod_date = "2021-08-25" # Video File.
    apod_date = '2017-09-03'
    apod_info_dict = get_apod_info(apod_date)
    image_url = get_apod_image_url(apod_info_dict)
    image_data = download_image(image_url)
    file_name = ''.join(random.choice(string.ascii_letters) for i in range(12)) + ".jpg"
    image_path = os.path.join(r'C:\temp\images', file_name)
    save_image_file(image_data, image_path)
    set_desktop_background_image(image_path)

def download_image(image_url):
    """Downloads an image from a specified URL.

    DOES NOT SAVE THE IMAGE FILE TO DISK.

    Args:
        image_url (str): URL of image

    Returns:
        Bytes: Binary image data, if succcessful. None, if unsuccessful.
    """

    print('Downloading image from:', image_url, end='')
    # Send GET request to download file
    resp_msg = requests.get(image_url)
    # Check whether the download was successfull
    if resp_msg.ok:
        print('...success!')
        # Extract Binary file content from response message body.
        image_data = resp_msg.content
        return image_data
    else:
        print(f'...failure.\n{resp_msg.status_code} {resp_msg.reason}')

def save_image_file(image_data, image_path,):
    """Saves image data as a file on disk.
    
    DOES NOT DOWNLOAD THE IMAGE.

    Args:
        image_data (bytes): Binary image data
        image_path (str): Path to save image file

    Returns:
        Bool: True, if succcessful. False, if unsuccessful
    """
    print(f'Saving image file as {image_path}', end='')
    # write binary data to image_path
    try:
        with open(image_path, 'wb') as file:
            file.write(image_data)
            print('...success!')
            return  True
    except Exception as error:
        print(f'...failure {error}')
        return False
    

def set_desktop_background_image(image_path):
    """Sets the desktop background image to a specific image.

    Args:
        image_path (str): Path of image file

    Returns:
        Bool: True, if succcessful. False, if unsuccessful        
    """
    print(f'Setting desktop to {image_path}', end='')
    try:
        if struct.calcsize('P') * 8 == 64:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
            print('...success!')
            return True
        else:
            ctypes.windll.user32.SystemParametersInfoA(20, 0, image_path, 3)
            print('...success!')
            return True
    except Exception as error:
        print(f'...failure \n{error}')
        return False
        

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