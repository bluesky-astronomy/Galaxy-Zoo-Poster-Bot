## Imports 
from atproto import Client

import pandas as pd
import numpy as np
import requests
import time
from io import BytesIO

import os

## Functions 
def pull_galaxy_image(url):
    response = requests.get(url)
    img_data = BytesIO(response.content)
    return img_data 

def create_metadata(row):
    if type(row.redshift.iloc[0]) == str:
        z = row.redshift.iloc[0]
    else:
        z = "%.2f" % ( row.redshift.iloc[0] )
    ra = "%.5f" % row.ra.iloc[0]
    dec = "%.5f" % row.dec.iloc[0]
    clsf = row.galaxy_description.iloc[0]
    survey = row.imaging.iloc[0]
    if "CANDELS-COODS" in survey:
        survey = 'CANDELS-GOODS'
       
    project = row.project.iloc[0]
    if 'Hubble' in project:
        instr = 'Hubble Space Telescope'
    elif 'CANDELS' in project:
        instr = 'Hubble Space Telescope'
    elif 'Galaxy Zoo 2' in project:
        instr = 'Apache Point 2.5m Telescope'

    t_lookback = row.t_lookback.iloc[0]
    if t_lookback < 1:
        tmp = t_lookback * 1000
        t_lookback_string = '%.1f million years' % tmp
    elif t_lookback >= 1:
        t_lookback_string = '%.2f billion years' % t_lookback
    else:
        t_lookback_string = 'unknown'

    vowels = ['a', 'e', 'i', 'o', 'u']
    start = 'A'
    if clsf[0] in vowels:
        start = 'An'
    else:
        start = 'A'
    
    random_no = np.random.random()

    if random_no < (1./20.):

        metadata = (
    """{} {}, observed with the {} in the {} survey.

It is at redshift {} (lookback time {}) with coordinates ({}, {}).

This classification was made in the {} project.
\U0001f52d
    """).format(
                start, clsf, instr, survey, z, t_lookback_string, ra, dec, project
            )
        
    else:
        metadata = (
    """{} {}, observed with the {} in the {} survey.

It is at redshift {} (lookback time {}) with coordinates ({}, {}).

This classification was made in the {} project.
    """).format(
                start, clsf, instr, survey, z, t_lookback_string, ra, dec, project
            )
        
    return metadata

def post(image, metadata, client, clsf, project):

    alt_im_text = 'A {} from the {} project.'.format(clsf, project)

    attempt = 0

    while attempt < 5:
        try:
            response = (
                client.send_image(
                    text = metadata, 
                    image = image, 
                    image_alt = alt_im_text
                )
            )
            attempt = 10
        except:
            time.sleep(10)
            attempt += 1
    
    return response

## Main Function
def main():
    # Initialising connection to the BlueSky Client.
    client = Client()

    # Getting log in details
    usrname = os.environ['USRNAME']
    pwd = os.environ['BLU_CODE']
    cat_path = os.environ['CAT_PATH']

    _ = client.login(usrname, pwd)

    # Selecting a Galaxy to upload.
    gal_data = pd.read_csv(cat_path).sample(1)
    url = gal_data['image_url'].iloc[0]

    # Creating the Post
    image = pull_galaxy_image(url)
    post_string = create_metadata(gal_data)

    # Posting
    response = post(image, post_string, client, gal_data.galaxy_description.iloc[0], gal_data.project.iloc[0])

    print(response)

## Initialisation
if __name__ == '__main__':
    main()