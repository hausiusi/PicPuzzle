# Picture Puzzle

## Table of Contents
1. [Reason for Creating This Game](#reason-for-creating-this-game)
2. [Installation](#installation)
3. [How to Play](#how-to-play)

## Reason for Creating This Game
A few days ago, I decided to give the Dear PyGui framework a try and started with some elementary projects. Here is a picture puzzle game designed for little kids.

## Installation
This project has been tested on Python 3.9. To check your Python version, run the following command:

```commandline
python --version
```
It may be helpful to use pyenv to manage specific Python versions. If you're not using pyenv, it is highly recommended to create a virtual environment before installing the required dependencies.

To set up the virtual environment and install the dependencies, follow these steps:
```commandline
python -m venv .venv
./venv/scripts/activate
pip install -r requirements.txt
```
## How to Play
Run the main.py file using the following command in the terminal:
```commandline
python3 main.py
```
Next, choose an image from the list on the right to create the puzzle. A 3x3 grid will be generated on the left. Simply drag and drop the pieces of the image until they are correctly arranged to complete the puzzle.
