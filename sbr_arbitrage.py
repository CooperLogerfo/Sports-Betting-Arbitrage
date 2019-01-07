from selenium import webdriver
from bs4 import BeautifulSoup as soup
from urllib import urlopen as uReq
import pandas as pd
import datetime as dt
import sys
import re
import time
import game_class
import sbr_game_scrape as scrape
from utilityDict import sportsDict

#url_a = "https://www.sportsbookreview.com/betting-odds/nba-basketball/money-line/"
url_a = "https://www.sportsbookreview.com/betting-odds/ncaa-basketball/money-line/"
games = scrape.league_scrape(url_a)


print( "{} : {}".format("printing length of games list", len(games)))


for game in games:
	game.identify_arbitrage()


games[0].odds_df.to_csv("game0.csv")
games[3].odds_df.to_csv("game3.csv")
games[4].odds_df.to_csv("game4.csv")
games[6].odds_df.to_csv("game6.csv")



#------------_different league options------------#
#-- "MLB", "NBA", "NFL", "NHL", "NCAAF", "NCAAB"--#
#-------------------------------------------------#

#def main(urls):
#	for url in urls:
#		all_games = scrape.league_scrape(url)
#		for game in games:
#			game.identify_arbitrage()#
#

#while __name__ == "__main__":
#	if len(sys.argv) > 1 and len(sys.argv) <= (len(sport_dict) + 2):
#		#first arg is script itself
#		urls = sys.argv[1:len(sys.argv)]
#		for arg in args:
#			for sport in sportsDict:
#				if arg == sport
#					urls.append(sport_dict[sport])#

#		main(urls)
#	else:
#		print("invalid command line args")