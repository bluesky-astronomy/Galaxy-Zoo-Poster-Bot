## Imports 
from atproto import Client

import pandas as pd
from PIL import Image
import requests
from io import BytesIO

import os

## Functions 
def pull_galaxy_image(url):
    response = requests.get(url)
    img_data = BytesIO(response.content)
    return img_data 

def create_metadata(gal_info):
    z = 
    ra =
    dec = 
    clsf = 
    instr =
    survey =
    projects =
    metadata = (
        ''
    )

def post(image, metadata, client):

    response = client.send_image(text = metadata, image = image, image_alt = 'A Galaxy')

    if len(response.errors) > 0:
        print("error posting to BlueSky -- errors:")
        print(response.errors)
    else:
        print("successfully posted animation")
    
    return response

## Main Function
def main():
    # Initialising connection to the BlueSky Client.
    client = Client()

    # Getting log in details
    usrname = os.getenv.get('USERNAME')
    pwd = os.getenv.get('PWD')
    cat_path = os.getenv.get('CAT_PATH')
    _ = client.login(usrname, pwd)

    # Selecting a Galaxy to upload.
    gal_data = pd.read_csv(cat_path).sample(1)
    url = gal_data['url']
    gal_info = gal_data['some_meta_data']

    # Creating the Post
    image = pull_galaxy_image(url)
    post_string = create_metadata(gal_info)

    # Posting
    response = post(image, post_string, client)

## Initialisation
if __name__ == '__main__':
    main()