import csv
import sys
from pathlib import Path
from typing import Any, Tuple, Callable
import getpass

from valid8 import validate, ValidationError

from beach_resort_reservation import app_utils
from beach_resort_reservation.menu import Menu, Entry, Description


class App:
    __filename = Path(__file__).parent.parent / 'default.csv'
    __delimiter = '\t'

    __logged: bool = False
    __api_key: str = None

    def __init__(self):
        self.__login_menu = Menu.Builder(Description(app_utils.APP_NAME_LOGIN)) \
            .with_entry(Entry.create('1', 'Login', on_selected=lambda: self.__do_login())) \
            .with_entry(Entry.create('2', 'Register', on_selected=lambda: self.__do_registration())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print(app_utils.APP_EXIT_MESSAGE), is_exit=True)) \
            .build()

        self.__menu = Menu.Builder(Description('Beach Resort Reservation')) \
            .with_entry(Entry.create('1', 'Make a new reservation', on_selected=lambda: self.__make_new_reservation())) \
            .with_entry(Entry.create('2', 'Delete a reservation', on_selected=lambda: self.__delete_reservation())) \
            .with_entry(Entry.create('3', 'Show my reservations', on_selected=lambda: self.__show_reservations())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print(app_utils.APP_EXIT_MESSAGE), is_exit=True)) \
            .build()

    # The following methos should call the REST API
    def __do_login(self):
        username: str = input('username: ')
        password = str = getpass.getpass('password: ')
        login_done: bool = False
        # TODO api call to do the login, if the user gives correct data and django replies
        #  ok we can use the menu else we notice the user with an error

        if (login_done):
            pass
        else:
            print(app_utils.LOGIN_FAILED)

    def __do_registration(self):
        username: str = input('username: ')
        email: str = input('email (optional): ')

        password_not_equals: bool = True
        first_attempt_passwords: bool = True
        while password_not_equals:
            if not first_attempt_passwords:
                print('Passwords are different, please write them another time: ')
            password: str = getpass.getpass('password: ')
            repeated_password: str = getpass.getpass('repeat password: ')

            first_attempt_passwords = False
            if password == repeated_password:
                password_not_equals = False

    # TODO registration on django and return status checking

    def __make_new_reservation(self):
        pass

    def __delete_reservation(self):
        reservation_to_delete_id: str = input('Insert the id of the reservation you want to delete')

    # TODO delete on django

    def __show_reservations(self):
        # TODO get the list of reservation from  django
        pass

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)

    def __run(self) -> None:
        self.__login_menu.run()


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
