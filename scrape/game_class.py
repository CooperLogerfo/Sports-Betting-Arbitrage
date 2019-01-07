from utilityDict import sportsbookID
import pandas as pd

class Game:
	"""Game class 
	Member variables - home team, away team, dataframe of odds and associated sportsbooks.
	Odds_df - pandas dataframe with these fields: "BookID", "Home_ML", "Away_ML".

	Will be expanded with more data for future use cases
	i.e. larger "odds_df", triangular arbitrage, frequency of line changes, halftime lines
	"""
	def __init__(self, homet, awayt, odds_dataframe):
		self.home_team = homet
		self.away_team = awayt
		self.odds_df = odds_dataframe

	def match_id_to_book(self, bookID):
		"""Utility function for matching bookID to book name (string).
		"""
		for book in sportsbookID:
			if sportsbookID[book] == bookID:
				return book

	def toDecimal(self, moneyline):
		"""Function that returns converts US moneyline odds to decimal odds.
		This allows for a cleaner arbitrage calculation.
		"""
		if moneyline > 0:
			return ((float(abs(moneyline))/100.0)+1.0)
		else:
			return ((100.0/float(abs(moneyline)))+1.0)

	def is_arbitrage(self, home, away):
		"""Function that returns True if arbitrage opportunity exists between two books.
		Used to avoid calculating arbitrage for every single combination of sportsbooks.
		"""
		is_arb = False
		if(1/home + 1/away < 1):
			is_arb = True
		return is_arb	

	def calc_arbitrage(self, home_odds, away_odds, stake_home):
		"""Function that returns which bets to place to take advantage of arbitrage.
		"""
		return_1 = stake_home*home_odds
		stake_away = stake_home*(home_odds/away_odds)
		return_2 = stake_away*away_odds # Should equal return_1.
		risk = stake_home + stake_away
		reward = return_1 - risk
		return stake_home, stake_away, reward

	def record_books():
		"""Function that stores books subject to arbitrage.
		"""

	def export_dataframe():
		"""Function that exports pandas dataframes to csv.
		"""

	def identify_arbitrage(self):
		"""Function for iterating through sportsbooks and finding arbitrage opportunities.
		Currently set for simply printing results. 
		TODO: Tweet/Email/Text updates
		TODO: Automatically place bets using API's where available.
		"""
		arb_count = 0
		for i, row_i in self.odds_df.iterrows():
			for j, row_j in self.odds_df.iterrows():
				books = [row_i['BookID'], row_j['BookID']]
				home_ml = [ self.toDecimal(row_i['Home_ML']), self.toDecimal(row_j['Home_ML'])]
				away_ml = [self.toDecimal(row_i['Away_ML']), self.toDecimal(row_j['Away_ML'])]
				if self.is_arbitrage(home_ml[0], away_ml[1]) == True:
					arb_count += 1
					home_bet, away_bet, profit = self.calc_arbitrage(home_ml[0], away_ml[1], 100)
					print("{} : {} : {} : {}".format("printing h bet a bet profit", home_bet, away_bet, profit))
					print("{} : {}".format("sportsbook for home back", sportsbookID[books[0]]))
					print("{} : {}".format("sportsbook for away back", sportsbookID[books[1]]))
				elif self.is_arbitrage(home_ml[1], away_ml[0]) == True:
					arb_count += 1
					home_bet, away_bet, profit = self.calc_arbitrage(home_ml[1], away_ml[0], 100)
					print("{} : {} : {} : {}".format("printing h bet a bet profit", home_bet, away_bet, profit))
					print("{} : {}".format("sportsbook for home back", sportsbookID[books[1]]))
					print("{} : {}".format("sportsbook for away back", sportsbookID[books[0]]))
		print("{} - {}".format("Num arb opportunities", arb_count/2))
