import game_class as game
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from urllib import urlopen as uReq
import pandas as pd
import datetime
import time


#---------------------------------------------#
#------BS4 and Selenium Utility Functions-----#
#---------------------------------------------#
def bs_Read(url):
	working_url = url
	working_client = uReq(working_url)
	working_html = working_client.read()
	working_soup = soup(working_html, "html.parser")
	return working_soup

def modify_url(url):
	now = datetime.datetime.now()
	day = str(now.day)
	month = str(now.month)
	year = str(now.year)
	if(len(day) < 2):
		day = "0" + day
	if(len(month) < 2):
		month = "0" + month
	#form : yyyy/mm/dd  eg) ?date=20190103 
	url_mod = "?date=" + year + month + day

	return url + url_mod

def load(url):
	driver = webdriver.Chrome()
	driver.get(modify_url(url))
	innerHTML = driver.execute_script("return document.body.innerHTML")
	page_soup = soup(innerHTML, "html.parser")
	return page_soup, driver

#---------------------------------------------#
#-----------End of Utility Functions----------#
#---------------------------------------------#



def books_to_dataframe(single_game_books, frame_num):
	"""Function for scraping odds from each book for each game and storing in a pandas dataframe.
	"""

	# Instantiate dataframe to be returned with approrpiate column names.
	temp_dataframe = pd.DataFrame(columns = ["BookID", "Home_ML", "Away_ML"])

	for i in range(2, len(single_game_books) ):
		home_ml = away_ml = ''
		book = 0
		book = int(single_game_books[i]['data-vertical-sbid'])
		try:
			lines = single_game_books[i].findAll('div',{'class':'_3h0tU'})
			home_ml = int(lines[0].text.encode('utf8'))
			away_ml = int(lines[1].text.encode('utf8'))
			print( "{} : {}".format( "printing would-be dataframe row", (i + frame_num*6 - 2) ) )
			odds_row = pd.DataFrame([[book, home_ml, away_ml]],\
				columns = ["BookID", "Home_ML", "Away_ML"])
			temp_dataframe = temp_dataframe.append(odds_row, ignore_index = True)
		except:
			# Invalid sportsbook (possibilities: Not taking bets on this game).
			continue

	return temp_dataframe


def scrape_game(single_game_books, web_driver, index):
	"""Function that scrapes a single beautifulsoup "game" object.
	Arguments: beautifulsoup object, selenium webdriver, and index for which game 
	in the given league on the given day (as provided by the original URL).
	Returns: Game object cointaining teams and dataframe of moneylines and associated sportsbooks.
	"""

	home = away = ''
	teams = single_game_books.findAll('span',{'class':'_3O1Gx'})
	home = teams[0].text
	away = teams[1].text


	right_button = web_driver.find_element_by_class_name('sbr-icon-chevron-right')
	end_of_books = False
	frame = 0 # Track which SBR frame the selenium driver is currently on.

	# Instantiate pandas dataframe that will house all lines for all books for this specific game.
	game_df = pd.DataFrame(columns = ["BookID", "Home_ML", "Away_ML"])

	while(end_of_books == False):
		# Step deeper into HTML.
		unique_books = single_game_books.findAll('section', {'class':'_2NFWr'})

		# Store each book's lines for this game.
		game_df = game_df.append(books_to_dataframe(unique_books, frame), ignore_index = True)
		try:
			right_button.click()

			# NEED to include sleep to allow the time for the page to load before scraping it.
			time.sleep(2)
			frame += 1

			# Scrape new frame.
			page_soup2 = soup(web_driver.execute_script("return document.body.innerHTML"), "html.parser")
			odds_container2 = page_soup2.find('div',{'id':'bettingOddsGridContainer'})
			games = odds_container2.findAll('div',{'class':'_3A-gC'})
			single_game_books = games[index]
		except Exception as e:
			# Reached end of sports books.
			end_of_books = True


	# Now click back as far left as possible for the next game.
	left_button = web_driver.find_element_by_class_name('sbr-icon-chevron-left')
	while(end_of_books == True):
		try:
			left_button.click()
		except Exception as e:
			# Reached end of sports books.
			end_of_books = False

	# "Game" object idenitfying home team, away team, and a dataframe with every book and every line
	newGame = game.Game(home, away, game_df)
	return newGame


def league_scrape(url):
	"""Function for scraping desired league (eg, NBA, NCAAB, NFL...).
	Arguments: league URL. 
	Returns: list of beautifulsoup objects for each game in given league on given date (as provided by URL).
	"""
	browser_soup, driver = load(url)

	odds_container = browser_soup.find('div',{'id':'bettingOddsGridContainer'})
	games = odds_container.findAll('div',{'class':'_3A-gC'})
	
	game_list =[]
	i = 0
	for game in games:
		time.sleep(3)
		game_list.append(scrape_game(game, driver, i))
		i += 1
	driver.quit()

	return game_list


