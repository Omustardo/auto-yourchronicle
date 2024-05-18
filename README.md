Automation for the incremental idle game Your Chronicle.
https://store.steampowered.com/app/1546320/Your_Chronicle/

This code isn't really meant to be run as-is. It's meant as an example or
starting point for anyone else who's interested in automation for YourChronicle
or automation in general.

## Usage

```shell
git clone https://github.com/omustardo/auto-yourchronicle.git
cd auto-yourchronicle
chmod +x run.sh
./run.sh
```

The first time it runs, it will download all of the python dependencies 
documented in `src/requirements.txt`.

## Development

Start by making sure you can `run.sh` as documented above in the Usage section.
This will ensure your python virtual environment is set up.

Modifying the Python code needs no explanation, and you can continue to use 
`run.sh` to run it. If you need to add new python dependencies, you'll need to:
 
1. Enter the virtual environment : `source ./src/venv/bin/activate`
2. Install new deps : `pip3 install foo`
3. Update the list of dependencies : `pip3 freeze > .
   /src/requirements.txt`

## Architecture

Your Chronicle is very consistent about where its UI elements go, so I always
start the program by moving the game to a fixed location and give it a fixed
size. I then have a bunch of pre-set regions (x,y,w,h) that I can search for
text in. This code is all in `navigator.py`.

In order to navigate between menus, I keep a url-like string
(`navigator.menu_state`). Whenever I change to a different view, I update this.
This allows different methods to know if they need to change to a different menu
or not.

Many methods return a boolean to indicate if they worked or not. 
Generally if something fails it isn't recoverable and the program just exits, 
but in a few cases it is recoverable.

## History

I began automation using Sikuli (http://sikulix.com/). Sikuli is an IDE that
lets you write Python to automate detection of images and clicking places on the
screen. Its IDE is nice because it shows images inline, so if you have code
that tries to detect a certain image, it's easy to read the code. I ended
up looking for alternatives because Sikuli felt limiting in a few ways:
* documentation was initially hard to find
* I wanted to run a standard python program, but instead I had to run Sikuli 
  as a java binary and then run python code from the Sikuli IDE.
* It doesn't have OCR built in, doing anything required taking screenshots and 
  matching against those. This meant that I couldn't resize the image, and it
  even seemed to have trouble with Redshift (changing the color of my 
  monitor at night).
* It felt flaky. The program would sometimes fail to match images that it 
  had matched before and I never figured out why.

I ended up switching to pytesseract + pyautogui and was pleased with making 
that change. [pytesseract](https://pypi.org/project/pytesseract/) is an OCR
tool. [pyautogui](https://pypi.org/project/pyautogui/) moves the mouse and does
other GUI interactions.

Unfortunately I started using version control well after I switched away from
Sikuli, so that isn't saved in this repo.
