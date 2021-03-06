# Art on the command line with ImageMagick

Try out our Glitch app if you want to skip all this! - https://glitch.com/~omnikrll-art-cmdline-magick-glitch

1. Download this project
2. Unzip the archive
3. cd to the project directory, e.g. `cd ~/Downloads/art_cmdline_magick`

There are a few options for setting up this codebase/environment depending on your OS and preferences. You may need to use the `sudo` command as a prefix for some commands depending on your system settings.

# General Install 

You can also set up this codebase/environment directly on your machine without using Docker.

1. Install Python if you don't already have it (Python 2 comes standard with OSX) - Windows users can download here: `https://www.python.org/downloads/windows`
    * Make sure to choose the Add to Path options for Windows installer
2. Install ImageMagick and make sure to select to add it to PATH if using the Windows installer - `https://www.imagemagick.org/script/download.php`
    * For Windows users, make sure you choose the same architecture type (32 or 64 bit) as your Python installation
    * If you are on OSX and not using Docker, try using homebrew (or MacPorts): `brew install imagemagick`
    * To download homebrew, run `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
    * You can also install using OSX binaries as shown below in the "Installing ImageMagick from binaries via OSX" section.
3. Install pip if you don't already have it (OSX pre-installed won't) - instructions here - `https://pip.pypa.io/en/stable/installing/`
    1. Run `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
    2. Run `python get-pip.py`
4. cd to the project directory, e.g. `cd ~/Downloads/art_cmdline_magick`
5. Install the project requirements `python -m pip install -r requirements.txt`
6. Execute scripts as shown below in the "Script exection examples" section.

# Docker

You will need to create a Docker account to get access to the download link.

1. Download and install docker here: `https://www.docker.com/products/docker-desktop`
2. cd to the project directory after making sure Docker Desktop is running, e.g. `cd ~/Downloads/art_cmdline_magick`
3. Run `docker build -t magick_image .`
4. Run `docker run -v "$(pwd):/art_cmdline_magick" -i -t magick_image bin/sh`
5. cd to the project directory now that you are working inside the Docker container `cd art_cmdline_magick`
5. Execute scripts as shown below in the "Script exection examples" section. 

# Installing Imagemagick from binaries via OSX

1. Download the following archive - `https://imagemagick.org/download/binaries/ImageMagick-x86_64-apple-darwin17.7.0.tar.gz`
2. cd to the directory where you downloaded the archive, e.g. `cd ~/Downloads`
3. Unzip the directory to your root directory `sudo tar xvzf ImageMagick-x86_64-apple-darwin17.7.0.tar.gz -C /`
4. Run `export MAGICK_HOME="/ImageMagick-7.0.8"`
5. Run `export PATH="$MAGICK_HOME/bin:$PATH"`
6. Run `export DYLD_LIBRARY_PATH="$MAGICK_HOME/lib/"`
7. Execute scripts as shown below in the "Script exection examples" section.


# Script execution examples

Scripts are set to output files to the /output folder.

## Simple conversion:

`magick sprites/veto_side_step_south_east00.png output/jpeg_convert.jpg`

## Conversion with wildcards:

`magick sprites/veto_side_step_south_east*.png output/jpeg_convert%02d.jpg`

## Scale:

`magick sprites/veto_side_step_south_east00.png -scale 500% output/big.png`

## Scale with distortion:

`magick sprites/veto_side_step_south_east00.png -scale 10% -scale 1000% output/pixelated.png`

## Montage - create a sprite sheet from images

`magick montage sprites/veto_side_step_south_east*.png -tile 3x2 -geometry 200x200 -background transparent output/sprite_sheet.png`

## Split the sheet back into separate images

`magick output/sprite_sheet.png -crop 200x200 output/tile_%02d.png`

## Custom CLI - sprite sheet

`python scripts/sprite_sheet.py -d sprites -o output/sheet.png`

# Scripting with Wand 

## The Meme Machine

`python scripts/meme_machine.py`

## Rorschach

`python scripts/rorschach.py`

## MAX DOUBT

`magick -size 20x20 xc:white +noise random -scale 500x500 -statistic minimum 20 -swirl "%[fx:rand()*240-180]" -virtual-pixel mirror -distort SRT "%[fx:rand()*360]" output/cubic.png`

```
SLICES=13
INPUT=output/cubic.png
OUTPUT=output/mandala.png

magick \
   $INPUT \
   -set option:h0 %[h] \
   -virtual-pixel mirror \
   -set option:distort:viewport %[w]x%[fx:h*1.5] \
   -distort affine "0,0 0,%[fx:h/2]" \
   -set option:distort:viewport "%[fx:ceil(h*tan(pi/$SLICES))]x%[h]" \
   -distort affine "%[fx:w/2],0 0,0" \
   -distort affine "0,%[h] 0,%[h]  %[w],%[h] %[w],%[h]  0,0 %[w],0" \
   -virtual-pixel none \
   -distort affine "%[w],0 %[w],0  1.5,0 0,0  1.5,%[h] %[w],%[h]" \
   -virtual-pixel mirror \
   -set option:distort:viewport %[w]x%[fx:h/2] \
   -distort SRT "0,0 0.5 0 %[w],0" \
   -duplicate $SLICES +delete \
   -virtual-pixel none \
   -set option:distort:viewport %[fx:h*2]x%[fx:h*2] \
   -distort SRT "%[fx:w/2],%[h] 1 %[fx:t*360/n] %[h],%[h]" \
   -layers merge \
   -gravity center \
   -extent %[h0]x%[h0] \
   +repage \
      $OUTPUT
```

in PowerShell:

```
$SLICES=13
$INPUT="output/cubic.png"
$OUTPUT="output/mandala.png"

magick `
   $INPUT `
   -set option:h0 %[h] `
   -virtual-pixel mirror `
   -set option:distort:viewport %[w]x%[fx:h*1.5] `
   -distort affine "0,0 0,%[fx:h/2]" `
   -set option:distort:viewport "%[fx:ceil(h*tan(pi/$SLICES))]x%[h]" `
   -distort affine "%[fx:w/2],0 0,0" `
   -distort affine "0,%[h] 0,%[h]  %[w],%[h] %[w],%[h]  0,0 %[w],0" `
   -virtual-pixel none `
   -distort affine "%[w],0 %[w],0  1.5,0 0,0  1.5,%[h] %[w],%[h]" `
   -virtual-pixel mirror `
   -set option:distort:viewport %[w]x%[fx:h/2] `
   -distort SRT "0,0 0.5 0 %[w],0" `
   -duplicate $SLICES +delete `
   -virtual-pixel none `
   -set option:distort:viewport %[fx:h*2]x%[fx:h*2] `
   -distort SRT "%[fx:w/2],%[h] 1 %[fx:t*360/n] %[h],%[h]" `
   -layers merge `
   -gravity center `
   -extent %[h0]x%[h0] `
   +repage `
      $OUTPUT
```
