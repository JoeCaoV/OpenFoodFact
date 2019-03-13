#!/usr/bin/env python3
# coding: utf-8

from classes.display import Display
from classes.database import Database

class Main():
	"""docstring for Main"""
	def __init__(self):
		display = Display()
		display.display_home()
		db = Database()
		first_ans = input('What do you want to do, select "1" or "2" : ')
		self.second(display, first_ans)

	def second(self, display, answer):
		if answer == "1":
			display.display_categories()
		elif answer == "2":
			display.display_saved()
		else:
			print("Incorrect choice, please select '1' or '2'.")
		



if __name__ == "__main__":
	MAIN = Main()