"""--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 --------------------

COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 --------------------"""
from datetime import date
from sys import argv, exit
import os, re, image_lib, inspect, requests,hashlib, sqlite3

# Global variables
#image_cache_dir = None  # Full path of image cache directory
#image_cache_db = None   # Full path of image cache database

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    

    # Get the path of the directory in which this script resides
    script_dir = get_script_dir()

    # Initialize the image cache
    init_apod_cache(script_dir)

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)
    pass
    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)
    pass
    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['file_path'])

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    # Check whether date has been provided from command line parameter
    num_params = len(argv) - 1
    # If date has been provided validate format
    if num_params >= 1:
        try:
            apod_date = date.fromisoformat(argv[1])
        except ValueError as error:
            print(f'Error: Invalid date format: {error} \n Script Aborted.')
            exit()
    # Validate date falls within accepted range
        START_DATE = date.fromisoformat('1995-06-16')
        if apod_date < START_DATE:
            print(f'Error: No data before {START_DATE} \n Script Aborted.')
            exit()
       
        elif apod_date > date.today():
            print('Error: APOD date cannot be in the future \n Script Aborted.')
            exit()
       
    else:
        apod_date = date.today()
    return apod_date

def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

def init_apod_cache(parent_dir):
    """Initializes the image cache by:
    - Determining the paths of the image cache directory and database,
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    
    The image cache directory is a subdirectory of the specified parent directory.
    The image cache database is a sqlite database located in the image cache directory.

    Args:
        parent_dir (str): Full path of parent directory    
    """
    # Determine the path of the image cache directory
    global image_cache_dir
    image_cache_dir = os.path.join(parent_dir,'images')
    # Create the image cache directory if it does not already exist
    if not os.path.isdir(image_cache_dir):
        os.makedirs(image_cache_dir)
    # Determine the path of image cache DB    
    global image_cache_db
    image_cache_db = os.path.join(image_cache_dir, 'image_cache.db')
    # Open a connection to the database
    con = sqlite3.connect(image_cache_db)
    # Get a cursor object that can be used to run SQL queries on the database.
    cur = con.cursor()
    create_image_table_query = """
    CREATE TABLE IF NOT EXISTS images
        (
        id          INTEGER PRIMARY KEY,
        title       TEXT NOT NULL,   
        explanation TEXT NOT NULL,
        path        TEXT NOT NULL,
        sha_256     TEXT NOT NULL
        );"""
    # Execute SQL database to create the 'images' table
    cur.execute(create_image_table_query)
    # Commit to the database
    con.commit()
   
def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    print("APOD date:", apod_date.isoformat())
    print(f'Getting {apod_date.isoformat()} information from NASA', end=' ')
    # Download the APOD information from the NASA API
    URL = 'https://api.nasa.gov/planetary/apod'
    API_KEY ='9B5p6pJIrJQsag5XemQBqiDzteN66d8sVlqdoZGC'
    # setup query string parameters.
    query_string_params = {'api_key': API_KEY,
                            'date': apod_date,
                            'thumbs': 'True'}
    # Send Get request to APOD api.
    resp_msg = requests.get(URL, params=query_string_params)
    # Check if GET request was successfull.
    #if resp_msg.status_code == requests.codes.ok:
    if resp_msg.ok:
        apod_info_dict = resp_msg.json()
        print('...success')
    elif resp_msg.status_code != requests.codes.ok:
        print(f'failure...\n{resp_msg.status_code} {resp_msg.reason}\nScript Aborted')
        exit()
     # Download Image.  
     # TODO FIx this shit
    if apod_info_dict['media_type'] == 'video':
        print('APOD title:', apod_info_dict['title'])
        print('APOD URL: ', apod_info_dict['url'])
        print('Downloading image from ', apod_info_dict['thumbnail_url'] )
        image_bytes_resp = requests.get(apod_info_dict['thumbnail_url'])
        image_bytes = image_bytes_resp.content
        image_sha256 = hashlib.sha256(image_bytes).hexdigest()
        image_id = get_apod_id_from_db(image_sha256)
        if image_id !=0:
            file_path = determine_apod_file_path(apod_info_dict['title'], apod_info_dict['thumbnail_url'])
        try:
            with open(file_path, 'wb') as file:
                file.write(image_bytes)
        except Exception as error:
            print(error)
            add_apod_to_db(apod_info_dict['title'], apod_info_dict['explanation'], file_path, image_sha256)
        else:
            exit()

    if apod_info_dict['media_type'] == 'image':
        print('APOD title:', apod_info_dict['title'])
        print('APOD URL:', apod_info_dict['hdurl'])
        print('Downloading image from', apod_info_dict['hdurl'] )
        image_bytes_resp = requests.get(apod_info_dict['hdurl'])
        image_bytes = image_bytes_resp.content
        image_sha256 = hashlib.sha256(image_bytes).hexdigest()    
        image_id = get_apod_id_from_db(image_sha256)
        if image_id != 0:
            # TODO Fix this shit
            file_path = determine_apod_file_path(apod_info_dict['title'], apod_info_dict['hdurl'])
            with open(file_path, 'wb') as file:
                file.write(image_bytes)
            add_apod_to_db(apod_info_dict['title'], apod_info_dict['explanation'], file_path, image_sha256)
            return image_id
        else:
            return 0
    
         
        
    # TODO: Check whether the APOD already exists in the image cache
        
    #if image_id !=0:
        #add_apod_to_db(apod_info_dict['title'], image_cache_dir, image_sha256)
        #file_path = determine_apod_file_path(apod_info_dict['title'], apod_info_dict['thumbnail_url' or apod_info_dict['hd_url']])
        #with open(file_path, 'wb') as file:
            #file.write(image_data)
        
        #return image_id
    #else:
        #return 0
    
    
    
    #elif apod_info_dict['media_type'] == 'image':
        #print('APOD title:', apod_info_dict['title'])
        #print('APOD URL:', apod_info_dict['hdurl'])
        #print('Downloading image from', apod_info_dict['hdurl'] )
        #image_data = resp_msg.content
        #image_sha256 = hashlib.sha256(image_data).hexdigest()
    #else:
        #resp_msg.status_code != requests.codes.ok
        #print(f'failure...\n{resp_msg.status_code} {resp_msg.reason}\nScript Aborted')
        #exit()
    

    
    # TODO: Save the APOD file to the image cache directory
    # TODO: Add the APOD information to the DB
    #return 0

def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful.  Zero, if unsuccessful       
    """
    
        # TODO: Complete function body
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()

    add_image_query = """
        INSERT INTO images
                (
                title,
                explanation,
                path,
                sha_256)
                VALUES (?,?,?,?);
                """
    new_image = (
            title,
            explanation,
            file_path,
            sha256)
    cur.execute(add_image_query, new_image)
    con.commit()
    con.close()
    return cur.lastrowid
    

    return 0

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    # TODO: Complete function body
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    # Define query to seach for album in DB
    find_image_query = """
    SELECT ID FROM images
    WHERE sha_256 = ? """
    #image_data = tuple(image_sha256,)
    cur.execute(find_image_query, [image_sha256])

    query_result = cur.fetchone()
    con.close
    if query_result is not None:
        return query_result[0]
    pass
    
    return 0

def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    # TODO: Complete function body
    # Obtain file extension from image_url
    file_type = re.search('.*(\..*)', image_url)
    file_extension = file_type.group(1)
    # Cleanup title - remove non word chars, leading and trailing whitespaces, inner spaces replaced with underscores.
    cleaned_string = re.sub('\W', '', re.sub('\s', '_', image_title.strip()))
    #file_path = image_cache_dir + cleaned_string + file_extension
    file_path = os.path.join(image_cache_dir, cleaned_string + file_extension)   
    return file_path

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    # TODO: Query DB for image info
    # TODO: Put information into a dictionary
    apod_info = {
        #'title': , 
        #'explanation': ,
        'file_path': 'TBD',
    }
    return apod_info

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    # NOTE: This function is only needed to support the APOD viewer GUI
    return

if __name__ == '__main__':
    main()