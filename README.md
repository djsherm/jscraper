# JScraper
A program to compile a dataframe of Jeopardy questions and display them in a webpage for personal testing. A heartfealt thank you to the wonderful people at [J! Archive](https://j-archive.com/) for enabling this project through the data collection that they do.

## Required Software

I made this repository using Python3 and regular HTML/CSS/JavaScript so it is best to match that the best you can.

The only external Python libraries I used were [Selenium](https://pypi.org/project/selenium/) and [Pandas](https://pypi.org/project/pandas/), both of which can be installed easily using pip:

`pip install selenium`

`pip install pandas`

You will also need to download the proper Chrome Driver and supply the appropriate file location for the variable `PATH` in `jeopardy_selenium.py`.

I tried my best to not rely on any external programs for running the HTML document but was unable to. In order to successfully run the HTML file, you will need to host it on a local server. I did this using [XAMPP](https://www.apachefriends.org/) with an Apache server. You can choose another method, but results may vary.

## Installation

JScraper can be downloaded and installed by cloning this repository:

`git clone https://github.com/djsherm/jscraper.git`

Once downloaded, `jeopardy_selenium.py` is fully ready to download and format Jeopardy clues from [J! Archive](https://j-archive.com/). To get the webapp running, you'll need to do some other file manipulations. Mentioned above, download and install XAMPP. Navigate to where you have installed "xampp" folder on your computer and navigate to the "htdocs" subfolder. You can create a new subfolder here or just drag and drop the entire repository folder here. Make note of the folder's name that contains the repository files.

## Usage

To compile a database of Jeopardy questions, you can simply run `jeopardy_selenium.py`. By default, it uses the default location for the Google Chrome driver once downloaded and installed. You can use a different browser or driver location, but results may vary.

By default, `jeopardy_selenium.py` extracts the clues from 3 games (counting backwards) starting at the game airing March 3, 2020. To change either of those parameters you'll need to tweak some variables. To change the starting game simply modify the `game_index` variable. This can simply be done by opening your game of choice on J! Archive and taking the `game_id` variable from the link.

For example, the game aired on July 18, 2014 can be found with this link [https://j-archive.com/showgame.php?game_id=4569](https://j-archive.com/showgame.php?game_id=4569). To start scraping games from here, in the code set `game_index=4569`.

By default, the number of games scraped is 3. This was mainly done to not wait too long while testing the code. To change this variable, set the default parameter `num_pages_to_extract` in the function `get_games()` to whatever you want. Note that JScraper scrapes games going backwards in time.

Once ran, `jeopardy_selenium.py` should save a .csv file in the same directory as itself. The .csv file is pipe character (| or SHIFT+\) delimited.

After you have the games you want scraped, we can run the testing webpage. Open up the XAMPP Control Panel app and click Start beside the Apache module. From there, open up a new tab on your web browser (I used FireFox, results may vary if you choose another browser). This is where you will need to know the folder that `jscrape_game.html` is in. For this example, the subfolder that my HTML file is in is called "jscrape_local_server" within the "htdocs" folder.

In your new browser tab, nagivate to the address "localhost/jscrape_local_server.jscrape_game.html" (obviously changing the name of the subfolder if you used a different name. From there, the game should load.

To get a new random clue, simply hit the "k" key. To reveal the answer to the clue, hit the "j" key.

# Authors

- Daniel Sherman - [GitHub](https://github.com/djsherm), [LinkedIn](https://www.linkedin.com/in/d-sherman18/)
