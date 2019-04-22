"""Create a colorful Rorschach-like pattern from an image."""

# Import required libraries
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
from wand.display import display
import requests
import yaml_data

# Parse YAML data
DATA = yaml_data.get_data()

SOURCE_IMG_URL = DATA['SOURCE_IMG_URL']
COLOR_TO_REPLACE = DATA['COLOR_TO_REPLACE']
FUZZ = DATA['FUZZ']
ALPHA = DATA['ALPHA']
IMAGE_1_COLOR = DATA['IMAGE_1_COLOR']
IMAGE_2_COLOR = DATA['IMAGE_2_COLOR']
BACKGROUND_COLOR = DATA['BACKGROUND_COLOR']

OUTPUT_FILE_1 = 'output/ocean1.png'
OUTPUT_FILE_2 = 'output/ocean2.png'


def rorschach(new_color, output_name, flip=False):
    """Remove a given color from an image (URL) and re-color all remaining pixels - then save the output."""
    # Create a new image from a given image URL
    with Image(blob=requests.get(SOURCE_IMG_URL)) as img:
        # Clone it
        with img.clone() as i:
            # Make the given color transparent
            i.transparent_color(color=Color(COLOR_TO_REPLACE), alpha=ALPHA, fuzz=FUZZ, invert=True)
            # Make a new drawing on the image
            with Drawing() as draw:
                # Fill the image with our new color (a hack - may not work if first pixel in image is transparent)
                draw.fill_color = new_color
                draw.color(0, 0, paint_method='replace')
                draw(i)
                # Flip the image if specified
                if flip:
                    i.flip()
                # Save the file
                i.save(filename=output_name)
                # Return the width and height
                return i.width, i.height


def draw_background(dimensions):
    """Create a solid rectangle for layering on our pattern and save the output."""
    # Create a new image from given dimensions
    with Image(width=dimensions[0], height=dimensions[1]) as background:
        # Create a new drawing
        with Drawing() as draw:
            # Fill the drawing with the specified color
            draw.fill_color = BACKGROUND_COLOR
            draw.rectangle(left=0, top=0, width=dimensions[0], height=dimensions[1])
            draw(background)
            # Save the file
            background.save(filename='output/background.png')


def meld(image_1, image_2):
    """Combines two images with the previously created background and save the output."""
    # Create a new image from background
    with Image(filename='output/background.png') as img_final:
        # Combine images
        img_final.composite(Image(filename=image_1), 0, 0)
        img_final.composite(Image(filename=image_2), 0, 0)
        # Save the file
        img_final.save(filename='output/modded_ocean.png')
        # You have the option of displaying the image via ImageMagick/Wand
        # display(img_final)


# Script execution begins here

# Rorschach our first image and store the dimensions in variable
image_dimensions = rorschach(IMAGE_1_COLOR, OUTPUT_FILE_1)
# Rorschach the second image
rorschach(IMAGE_2_COLOR, OUTPUT_FILE_2, flip=True)
# Draw the background rectangle
draw_background(image_dimensions)
# Combine all the images
meld(OUTPUT_FILE_1, OUTPUT_FILE_2)
