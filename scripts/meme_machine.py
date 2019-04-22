"""Create a meme from a given image URL."""

# Import required libraries
from wand.image import Image
from wand.drawing import Drawing
from wand.display import display
import requests
import yaml_data


# Parse YAML data
DATA = yaml_data.get_data()

IMAGE_URL = DATA['IMAGE_URL']
TEXT = DATA['TEXT']
FONT_SIZE = DATA['FONT_SIZE']
HEIGHT = DATA['HEIGHT']
DEEP_FRY = DATA['DEEP_FRY']
COMPRESSION_LEVEL = DATA['COMPRESSION_LEVEL']
CONTRAST_INCREASE_PERCENT = DATA['CONTRAST_INCREASE_PERCENT']

# Create a new image on file system from a given image URL
with Image(blob=requests.get(IMAGE_URL)) as img:
    # Create a new drawing (on top of image)
    with Drawing() as draw:
        # Impact font is important for making meme look proper
        draw.font = 'fonts/impact.ttf'
        draw.font_size = FONT_SIZE
        draw.fill_color = 'white'
        draw.text_alignment = 'center'
        # Put our text in the center of the image and at the specified height (in pixels)
        draw.text(int(img.width / 2), HEIGHT, TEXT)
        draw(img)
        # Apply heavy JPG compression and contrast if the user chooses the DEEP_FRY option
        if DEEP_FRY:
            img.compression = 'jpeg'
            img.compression_quality = COMPRESSION_LEVEL
            img.modulate(100, 100 + CONTRAST_INCREASE_PERCENT, 100)
            img.save(filename='output/meme.jpg')
        else:
            img.save(filename='output/meme.png')
        # You have the option of displaying the image via ImageMagick/Wand
        # display(img)
