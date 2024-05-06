# Galaxy Zoo Poster Bot
This repository contains the code to post an image of a galaxy from the Galaxy Zoo archives every hour on BlueSky. The code to pull the image from the archive, write the post text and publish on BlueSky is written as a single Python script. To post every hour, a GitHub Actions workflow has been created with a scheduled trigger of every 0th minute of every hour. 

The process of creating the bot and running it with GitHub actions is surprisingly easy. Therefore, please use this repository as an example to create your own bots for different things. I really think that these hourly bot posters were a brilliant thing that Twitter killed off. So, let's see some more of them on BlueSky!

This repository is laid out as follows.

<ins>posting-to-bluesky-example.ipynb</ins> - A Jupyter Notebook breaking down the process of using Python to write a post, add image data and publish it on BlueSky. If you are just beginning to write the code for your bot, I'd recommend you start here.

<ins>creating-a-github-workflow.ipynb</ins> - A Jupyter Notebook breaking down the process of creating a GitHub Actions workflow to schedule your bot. This will introduce GitHub actions, how to use Secret Access Tokens and how to create a cron schedular.

<ins>gz-bot.py</ins> - The python script which is run within the GitHub Actions workflow every hour. May be used as a working example.

<ins>requirements.txt</ins> - The Python packages that must be installed to run the Python script. See creating-a-github-workflow.ipynb for how this is used.