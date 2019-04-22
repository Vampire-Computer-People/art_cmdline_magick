"""Custom CLI script to create sprite sheets from a folder of PNG files."""

# Import required libraries
import argparse
import subprocess
import yaml_data

# Set up our COMMANDS - a list of commands to send to the command line
if yaml_data.get_data()['MAGICK_VERSION'] >= 7:
    COMMANDS = ['magick', 'montage']
else:
    COMMANDS = ['montage']

# Create our argument parser and define/add arguments and defaults
p = argparse.ArgumentParser()
p.add_argument('-d', '--directory', help='directory of png images', required=True)
p.add_argument('-o', '--output', help='output image or pattern', required=True)
p.add_argument('-t', '--tile', help='tile dimensions for sprite sheet, e.g. 6x3', default='3x2')
p.add_argument('-s', '--size', help='size of each tile, e.g. 200x200', default='200x200')

# Parse user arguments
args = p.parse_args()

# Add to our list of commands from user arguments
image_paths = '{}/*.png'.format(args.directory)
COMMANDS.extend([image_paths, '-tile', args.tile, '-geometry', args.size, '-background', 'transparent', args.output])

# Show user the native command to be executed
commands_to_print = ' '.join(COMMANDS)
print('Executing the following command:')
print(commands_to_print)

# Run the command
subprocess.call(COMMANDS)
