"""--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 --------------------

Library for interacting with NASA's Astronomy Picture of the Day API.

--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 --------------------"""
import requests
def main():
    apod_date = '2021-05-03'
    apod_info_dict = get_apod_info(apod_date)
    get_apod_image_url(apod_info_dict)

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    URL = 'https://api.nasa.gov/planetary/apod'
    API_KEY ='9B5p6pJIrJQsag5XemQBqiDzteN66d8sVlqdoZGC'
    # setup query string parameters.
    query_string_params = {'api_key': API_KEY,
                           'date': apod_date,
                           'thumbs': 'True'}
    # send Get request to APOD api.
    print("APOD date:", apod_date)
    print(f'Getting {apod_date} APOD information from NASA', end=' ')
    resp_msg = requests.get(URL, params=query_string_params)
    # Check if GET request was successfull.

    if resp_msg.ok:
        apod_info_dict = resp_msg.json()
        print('...success!')
        print('APOD title:', apod_info_dict['title'])
        return apod_info_dict
    else:
        print(f'failure... {resp_msg.status_code} {resp_msg.reason}.')

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    # Get Image URL from APOD dict.
    if apod_info_dict['media_type'] == 'video':
        image_url = apod_info_dict['thumbnail_url']
        return image_url
    else:
        image_url = apod_info_dict['hdurl']
        return image_url

if __name__ == '__main__':
    main()