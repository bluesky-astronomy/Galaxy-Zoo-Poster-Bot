## Imports 
from atproto import Client

import pandas as pd
import requests
import sys
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
        t_lookback_string = '%.3f million years' % tmp
    else:
        t_lookback_string = '%.2f billion years' % t_lookback
    

    metadata = (
"""A {}, observed with the {} in the {} survey.

It is at redshift {} (lookback time {}) with coordinates ({}, {}).

This classification was made in the {} project.
""").format(
            clsf, instr, survey, z, t_lookback_string, ra, dec, project
        )

    return metadata

def post(image, metadata, client, clsf, project):

    alt_im_text = 'A {} from the {} project.' % (clsf, project)

    response = (
        client.send_image(
            text = metadata, 
            image = image, 
            image_alt = alt_im_text
        )
    )
    
    return response

## Main Function
def main():
    # Initialising connection to the BlueSky Client.
    client = Client()

    # Getting log in details
    usrname = os.environ['USRNAME']
    pwd = os.environ['PWD']
    cat_path = os.environ['CAT_PATH']

    print(len(pwd))
    print(pwd)

    _ = client.login(usrname, pwd)

    # Selecting a Galaxy to upload.
    gal_data = pd.read_csv(cat_path).sample(1)
    url = gal_data['image_url']

    # Creating the Post
    image = pull_galaxy_image(url)
    post_string = create_metadata(gal_data)

    # Posting
    response = post(image, post_string, client, gal_data.galaxy_description.iloc[0], gal_data.project.iloc[0])

## Initialisation
if __name__ == '__main__':
    main()