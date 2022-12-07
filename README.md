**Team Members**: Keya Sengupta, Fanni Varhelyi, Cecil John, Zhongxian Liu

**Topic**: Environmental Health/Air Quality

This repository will hold work for the PPOL564 Final Project.

[All csv datasets used can be found at this link.](https://drive.google.com/drive/folders/1ve6YTp5sn9QkpjGCJBIgosvKKT3Ypwd7?usp=share_link)

## Data Sources
1. CDC Places Data
1. Toxic Release Inventory
1. Census data / American Community Survey data

## Directory Structure
1. input: information about data
1. output: generated dataframes and other pieces of information
1. scratch: notebooks for preliminary data exploration
1. src: final code

## How to run
1. This repository uses a single notebook called [0_driver](src/0_Driver.ipynb).
1. It requires a Census API key which it reads from a saved credentials file.
    1. In order to retrieve this, create a file called either config.json or a creds.yml in the root of the directory, with the below key names.
	
		```
		{
			"CENSUS": {
			"API_KEY" : ""
		}
		
		```
		
1. Running this file alone will import our other files, which are written as Python classes, and use the functions within them to process data and generate maps.
1. It requires an input from the keyboard - when prompted, enter the state abbreviations you wish to examine through maps.
    ![How to enter values](https://github.com/skeyas/PPOL564_Group2/blob/master/assets/user_input_example.PNG)
    1. Upon entering the state abbreviations, allow the program to continue executing. When it finishes, it will store all output images in the output directory.
