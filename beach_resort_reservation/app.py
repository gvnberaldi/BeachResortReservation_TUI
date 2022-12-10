import dataclasses
import getpass
import sys
from datetime import datetime
from typing import Any, Callable, List, Optional

import requests
from dateutil.parser import parse
from termcolor import colored
from valid8 import ValidationError

from beach_resort_reservation import app_utils, domain_utils
from beach_resort_reservation.domain import Username, Email, Password, NewReservation, ReservationID, NumberOfSeats, \
    ReservedUmbrellaID, Price, ReservationFromServer
from beach_resort_reservation.exceptions import IntegerInputException, DateInputException
from beach_resort_reservation.menu import Menu, Entry, Description


class App:
    __delimiter = '\t'

    __logged: bool = False
    __api_key: Optional[str] = None
    __user_reservation: List[NewReservation] = dataclasses.field(default_factory=list)

    def __init__(self):
        self.__login_menu = Menu.Builder(Description(app_utils.APP_NAME_LOGIN)) \
            .with_entry(Entry.create('1', 'Login', on_selected=lambda: self.__do_login())) \
            .with_entry(Entry.create('2', 'Register', on_selected=lambda: self.__do_registration())) \
            .with_entry(
            Entry.create('0', 'Exit', on_selected=lambda: print(colored(app_utils.APP_EXIT_MESSAGE,
                                                                        app_utils.SUCCESS_ACTION_COLOR)),
                         is_exit=True)) \
            .build()

        self.__menu = Menu.Builder(description=Description(app_utils.APP_NAME_MENU),
                                   auto_select=lambda: self.__show_reservations()) \
            .with_entry(Entry.create('1', 'Make a new reservation', on_selected=lambda: self.__make_new_reservation())) \
            .with_entry(Entry.create('2', 'Delete a reservation', on_selected=lambda: self.__delete_reservation())) \
            .with_entry(Entry.create('4', 'Logout', on_selected=lambda: self.__do_logout())) \
            .with_entry(
            Entry.create('0', 'Exit',
                         on_selected=lambda: print(colored(app_utils.APP_EXIT_MESSAGE, app_utils.SUCCESS_ACTION_COLOR)),
                         is_exit=True)) \
            .build()

    def __do_login(self):

        username: str = input('Username: ')
        password: str = getpass.getpass('Password: ')

        login_response = self.do_login_request(username=username, password=password)

        if login_response.status_code != 200 or login_response.json()['key'] is None:
            print(app_utils.LOGIN_FAILED)
        else:
            print(colored(app_utils.LOGIN_OK_WELCOME, app_utils.SUCCESS_ACTION_COLOR))
            self.__api_key = login_response.json()['key']
            self.__login_menu.stop()
            self.__menu.run()


    def do_login_request(self, username: str, password: str):
        login_response = requests.post(url=f'{app_utils.API_SERVER}{app_utils.LOGIN_END_POINT}',
                                       data={'username': username, 'password': password})
        return login_response

    def __do_registration(self):
        email, password, repeated_password, username = self.__read_registration_fields_from_user_input()
        if password is not None and repeated_password is not None:
            registration_response = self.do_registration_request(username, password, repeated_password, email)
            self.__validate_registration_response(registration_response)

    def __validate_registration_response(self, registration_response):

        response_json = registration_response.json()
        if registration_response.status_code != 201 or registration_response.json()['key'] is None:
            print(colored(app_utils.REGISTRATION_FAILED, app_utils.FAIL_ACTION_COLOR))

            if registration_response.status_code == 400:
                self.__show_registration_tips_to_fix_errors_to_user(response_json)

        else:
            print(colored(app_utils.REGISTRATION_OK_WELCOME, app_utils.SUCCESS_ACTION_COLOR))
            self.__api_key = response_json['key']
            self.__login_menu.stop()
            self.__menu.run()

    def __show_registration_tips_to_fix_errors_to_user(self, response_json):
        print(colored('This could help you:', app_utils.FAIL_ACTION_COLOR))
        if 'non_field_errors' in response_json:
            for elem in response_json['non_field_errors']:
                print('\t' + colored(elem, app_utils.FAIL_ACTION_COLOR))
        if 'username' in response_json:
            for elem in response_json['username']:
                print('\t' + colored(elem, app_utils.FAIL_ACTION_COLOR))
        if 'email' in response_json:
            for elem in response_json['email']:
                print('\t' + colored(elem, app_utils.FAIL_ACTION_COLOR))
        if 'password1' in response_json:
            for elem in response_json['password1']:
                print('\t' + colored(elem, app_utils.FAIL_ACTION_COLOR))
        if 'password2' in response_json:
            for elem in response_json['password2']:
                print('\t' + colored(elem, app_utils.FAIL_ACTION_COLOR))

    def __read_registration_fields_from_user_input(self):

        username: Username = self.__ask_until_provided_field(Username, 'username: ', 'username')
        email: Email = self.__ask_until_provided_field(Email, 'email: ', 'email')
        password_not_equals: bool = True
        first_attempt_passwords: bool = True
        password: Optional[Password] = None
        repeated_password: Optional[Password] = None
        while password_not_equals:

            if not first_attempt_passwords:
                print(app_utils.PASSWORDS_DIFFERENT_ON_REGISTRATION_ERROR_MESSAGE)
            password: Password = self.__ask_until_provided_field(Password, 'password: ', 'password')
            repeated_password: Password = self.__ask_until_provided_field(Password, 'repeat password: ', 'password')

            first_attempt_passwords = False
            if password.value == repeated_password.value:
                password_not_equals = False

        return email, password, repeated_password, username

    def do_registration_request(self, username: Username, password: Password, repeated_password: Password,
                                email: Email):
        registration_response = requests.post(url=f'{app_utils.API_SERVER}{app_utils.REGISTRATION_END_POINT}',
                                              data={'username': username.value, 'password1': password.value,
                                                    'password2': repeated_password.value, 'email': email.value})
        return registration_response

    def __ask_until_provided_field(self, constructor: Callable[[str], Any], prompt: str, type_: str):
        is_invalid_input = True
        while is_invalid_input:
            try:
                object_to_create = self.__ask_field(constructor, prompt, type_)
                is_invalid_input = False
                return object_to_create
            except ValidationError as validation_error:
                is_invalid_input = True
                print(colored(validation_error.help_msg, app_utils.FAIL_ACTION_COLOR))
            except IntegerInputException as integer_exception:
                print(colored(integer_exception.help_msg, app_utils.FAIL_ACTION_COLOR))
            except DateInputException as date_exception:
                print(colored(date_exception.help_msg, app_utils.FAIL_ACTION_COLOR))

    def __ask_field(self, constructor: Callable[[str], Any], prompt: str, type_: str):
        read_value: Any
        if type_ == 'password':
            read_value = getpass.getpass(prompt).strip()
        elif type_ == 'reservation_id' or type_ == 'umbrella_id' or type_ == 'number_of_seats':

            read_value_str = input(prompt)
            if read_value_str.isnumeric():
                read_value = int(read_value_str)
            else:
                raise IntegerInputException()

        elif type_ == 'date':
            date_str: str = input(prompt).strip()
            if constructor(date_str) is not None:
                return constructor(date_str)
            else:
                raise DateInputException()

        else:
            read_value = input(prompt)
            read_value = read_value.strip()

        object_to_create = constructor(read_value)
        return object_to_create

    def __make_new_reservation(self):
        new_reservation: NewReservation = self.__read_new_reservation_from_user_input()
        if new_reservation is not None:
            new_reservation_response = self.do_new_reservation_request(new_reservation)
            self.__validate_new_reservation_response(new_reservation_response)

    def __read_date_from_user(self, date: str):
        try:
            return datetime.strptime(date, app_utils.DATE_PATTERN)
        except ValueError:
            return None

    def do_new_reservation_request(self, new_reservation: NewReservation):
        new_reservation_response = requests.post(
            url=f'{app_utils.API_SERVER}{app_utils.RESERVATIONS_END_POINT}',
            headers={'Authorization': f'Token {self.__api_key}'},
            data={'number_of_seats': new_reservation.number_of_seats.value,
                  'reservation_start_date': new_reservation.start_date,
                  'reservation_end_date': new_reservation.end_date,
                  'reserved_umbrella_id': new_reservation.umbrella_id.value}, )
        return new_reservation_response

    def __validate_new_reservation_response(self, new_reservation_response):
        if new_reservation_response.status_code != 201:
            print(colored(app_utils.NEW_RESERVATION_FAILED, app_utils.FAIL_ACTION_COLOR))
            new_reservation_response_json = new_reservation_response.json()
            self.__show_new_reservation_tips_to_fix_errors_to_user(new_reservation_response_json)
        else:
            print(colored(app_utils.NEW_RESERVATION_CORRECTLY_ADDED, app_utils.SUCCESS_ACTION_COLOR))

    def __read_new_reservation_from_user_input(self) -> NewReservation:
        reserved_umbrella_id: ReservedUmbrellaID = self.__ask_until_provided_field(ReservedUmbrellaID,
                                                                                   'Choose the umbrella id: ',
                                                                                   'umbrella_id')
        number_of_seats: NumberOfSeats = \
            self.__ask_until_provided_field(NumberOfSeats, f'How many seats you want to have in your umbrella? '
                                                           f'Take in mind that the minimum is '
                                                           f'{domain_utils.MIN_NUMBER_OF_SEATS} and the maximum is '
                                                           f'{domain_utils.MAX_NUMBER_OF_SEATS}: ', 'number_of_seats')
        reservation_start_date: datetime.date = \
            self.__ask_until_provided_field(self.__read_date_from_user, f'Insert the start date of the reservation '
                                                                        f'(in the format yyyy-mm-dd ): ',
                                            'date').date()
        reservation_end_date: datetime.date = \
            self.__ask_until_provided_field(self.__read_date_from_user,
                                            f'Insert the end date of the reservation (in the format yyyy-mm-dd  ): ',
                                            'date').date()
        try:
            reservation: NewReservation = NewReservation(number_of_seats=number_of_seats,
                                                         umbrella_id=reserved_umbrella_id,
                                                         start_date=reservation_start_date,
                                                         end_date=reservation_end_date)
            return reservation
        except ValidationError as e:
            print(colored(e.help_msg, app_utils.FAIL_ACTION_COLOR))

    def __show_new_reservation_tips_to_fix_errors_to_user(self, response_json):
        print(colored('This could help you:', app_utils.FAIL_ACTION_COLOR))
        if 'number_of_seats' in response_json:
            print(colored('\tThere is a problem with the number of seats:', app_utils.FAIL_ACTION_COLOR))
            for elem in response_json['number_of_seats']:
                print('\t\t' + colored(elem, app_utils.FAIL_ACTION_COLOR))
        if 'reservation_start_date' in response_json:
            print(colored('\tThere is a problem with the reservation start date:', app_utils.FAIL_ACTION_COLOR))
            for elem in response_json['reservation_start_date']:
                print('\t\t' + colored(elem, app_utils.FAIL_ACTION_COLOR))
        if 'reservation_end_date' in response_json:
            print(colored('\tThere is a problem with the reservation end date:', app_utils.FAIL_ACTION_COLOR))
            for elem in response_json['reservation_end_date']:
                print('\t\t' + colored(elem, app_utils.FAIL_ACTION_COLOR))
        if 'reserved_umbrella_id' in response_json:
            print(colored('\tThere is a problem with the umbrella you choose:', app_utils.FAIL_ACTION_COLOR))
            for elem in response_json['reserved_umbrella_id']:
                print('\t\t' + colored(elem, app_utils.FAIL_ACTION_COLOR))

    def __delete_reservation(self):
        reservation_id = self.__ask_until_provided_field(ReservationID,
                                                         'Insert the id of the reservation you want to delete: ',
                                                         'reservation_id')

        reservation_delete_response = self.do_reservation_delete_request(reservation_id)
        self.__validate_delete_response(reservation_delete_response=reservation_delete_response,
                                        reservation_id=reservation_id)

    def __validate_delete_response(self, reservation_delete_response, reservation_id: ReservationID):
        if reservation_delete_response.status_code != 200 and reservation_delete_response.status_code != 204 and \
                reservation_delete_response.status_code != 202:
            if reservation_delete_response.status_code == 404:
                print(colored(app_utils.DELETE_FAILED_ID_NOT_FOUND, app_utils.FAIL_ACTION_COLOR))
            else:
                print(colored(app_utils.DELETE_FAILED, app_utils.FAIL_ACTION_COLOR))
        else:
            print(colored(f'Reservation with id: {reservation_id.value}{app_utils.DELETE_OK}',
                          app_utils.SUCCESS_ACTION_COLOR))

    def do_reservation_delete_request(self, reservation_id_to_delete: ReservationID):
        reservation_delete_response = requests.delete(
            url=f'{app_utils.API_SERVER}{app_utils.RESERVATIONS_END_POINT}{reservation_id_to_delete.value}/',
            headers={'Authorization': f'Token {self.__api_key}'})
        return reservation_delete_response

    def __show_reservations(self):
        reservation_list_response = self.do_retrieve_reservation_list_request()
        self.__validate_reservation_list_response(reservation_list_response)


    def do_retrieve_reservation_list_request(self):

        reservation_response = requests.get(url=f'{app_utils.API_SERVER}{app_utils.RESERVATIONS_END_POINT}',
                                            headers={'Authorization': f'Token {self.__api_key}'})
        return reservation_response

    def __validate_reservation_list_response(self, reservation_list_response):
        # print(reservation_list_response.content)

        if reservation_list_response.status_code != 200:
            print(colored(app_utils.RESERVATION_LIST_RETRIEVE_FAILED, app_utils.FAIL_ACTION_COLOR))
        else:
            response_json = reservation_list_response.json()
            self.__print_reservation_list(response_json)

    def __print_reservation_list(self, response_json):
        if len(response_json) > 0:
            print_separator: () = lambda: print('-' * 150)
            print_separator()

            print(app_utils.RESERVATION_FORMATTER % (
                'Reservation ID', 'Reserved umbrella ID', 'Number of seats', 'From', 'To', 'Reservation price'))
            print_separator()
            for elem in response_json:
                reservation: ReservationFromServer = self.__create_reservation_from_json_object(elem)
                print(app_utils.RESERVATION_FORMATTER % (
                    reservation.id.value, reservation.umbrella_id.value,
                    reservation.number_of_seats.value,
                    reservation.start_date, reservation.end_date,
                    reservation.price))
            print_separator()
        else:
            print()
            print(app_utils.NO_RESERVATION_FOUND_FOR_USER)
            print()

    def __do_logout(self):
        logout_response = self.do_logout_request()
        self.__validate_logout_response(logout_response)

    def __validate_logout_response(self, logout_response):
        if logout_response.status_code != 200:
            print(colored(app_utils.LOGOUT_FAILED, app_utils.FAIL_ACTION_COLOR))
        else:
            print(colored(app_utils.LOGGED_OUT_MESSAGE, app_utils.SUCCESS_ACTION_COLOR))
            self.__menu.stop()
            self.__login_menu.run()
            # optional
            self.__api_key = None

    def do_logout_request(self):
        logout_response = requests.post(url=f'{app_utils.API_SERVER}/auth/logout/',
                                        headers={'Authorization': f'Token {self.__api_key}'})
        return logout_response

    def run(self) -> None:
        try:
            self.__run()
        except Exception as e:
            print('Panic error!', file=sys.stderr)
            print(e)

    def __run(self) -> None:
        self.__login_menu.run()

    def __create_reservation_from_json_object(self, elem):
        reservation_id: ReservationID = ReservationID(elem['id'])
        number_of_seats: NumberOfSeats = NumberOfSeats(elem['number_of_seats'])
        reservation_start_date: datetime.date = parse(elem['reservation_start_date']).date()
        reservation_end_date: datetime.date = parse(elem['reservation_end_date']).date()
        reserved_umbrella_id: ReservedUmbrellaID = ReservedUmbrellaID(elem['reserved_umbrella_id'])
        reservation_price: Price = Price.parse("{0:.2f}".format(elem['reservation_price']))
        reservation: ReservationFromServer = ReservationFromServer(id=reservation_id,
                                                                   number_of_seats=number_of_seats,
                                                                   price=reservation_price,
                                                                   umbrella_id=reserved_umbrella_id,
                                                                   start_date=reservation_start_date,
                                                                   end_date=reservation_end_date)

        return reservation


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
