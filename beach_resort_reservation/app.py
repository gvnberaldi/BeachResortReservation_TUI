import csv
import sys
from pathlib import Path
from typing import Any, Tuple, Callable

from valid8 import validate, ValidationError

from beach_resort_reservation.menu import Menu, Entry, Description


class App:
	__filename = Path(__file__).parent.parent / 'default.csv'
	__delimiter = '\t'
	
	def __init__(self):
		self.__login = Menu.Builder(Description('Login'))\
			.with_entry(Entry.create('1', 'Login', on_selected=lambda: self.__do_login()))\
			.with_entry(Entry.create('2', 'Register', on_selected=lambda: self.__do_registration()))\
			.with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True))\
			.build()
		
		self.__menu = Menu.Builder(Description('Beach Resort Reservation'))\
			.with_entry(Entry.create('1', 'Make a new reservation', on_selected=lambda: self.__make_new_reservation()))\
			.with_entry(Entry.create('2', 'Delete a reservation', on_selected=lambda: self.__delete_reservation()))\
			.with_entry(Entry.create('3', 'Modify a reservation', on_selected=lambda: self.__modify_reservation()))\
			.with_entry(Entry.create('4', 'Show my reservations', on_selected=lambda: self.__show_reservations()))\
			.with_entry(Entry.create('5', 'Sort by date', on_selected=lambda: self.__sort_by_date()))\
			.with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True))\
			.build()
	
	# The following methos should call the REST API
	def __do_login(self):
		pass
	
	def __do_registration(self):
		pass
	
	def __make_new_reservation(self):
		pass
	
	def __delete_reservation(self):
		pass
	
	def __modify_reservation(self):
		pass
	
	def __show_reservations(self):
		pass
	
	def __sort_by_date(self):
		pass
	
	def run(self) -> None:
		try:
			self.__run()
		except:
			print('Panic error!', file=sys.stderr)
	
	def __run(self) -> None:
		self.__login.run()
		

def main(name: str):
	if name == '__main__':
		App().run()
		

main(__name__)
