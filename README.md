# Granblue Character Frame-data Web-scraper
## Description:

### What the program does:

A CLI program written in Python that uses selenium chromedriver to gather character data from dustloop for the game GBVSR.  

### How to use:

In its current implementation, the user chooses a valid character to fetch the data for. The program gathers the data from dustloop using the chromedriver then converts the results into a csv file. The chromedriver is required to be in a specific folder, but that can be altered (the relevant test will have to be as well).

## Details:

### test_granblue_data_gatherer

Contains all the tests for functionality of the core class of the project as well as its functions.

### granblue_data_gatherer.py

Contains the class implementation of the program and the necessary functions. Different sections of the character page are formatted differently which required similar functions that process non-uniform data since characters can have unique attributes. Creates a csv named after the character in the character_frame_data folder when finished, and will overwrite an existing character csv with updated information (when the game gets patched, for instance).

### main.py

Contains a list of valid characters as well as a break-down for the IDs for different parts of the character pages for reference should the format of the website change. Prompts the user to choose a character from the game to gather data for.