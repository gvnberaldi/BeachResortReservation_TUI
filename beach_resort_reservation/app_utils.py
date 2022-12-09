import datetime

APP_NAME_LOGIN = 'Umbrella Reservation Login'
APP_NAME_MENU = 'Umbrella Reservation'
APP_EXIT_MESSAGE = 'Thank you for using our app, see you soon'

LOGIN_END_POINT = '/auth/login/'
REGISTRATION_END_POINT = '/auth/registration/'
RESERVATIONS_END_POINT = '/beachreservation/'

LOGIN_FAILED = 'Login failed, please provide correct credential to continue...'
LOGIN_OK_WELCOME = 'You are logged in now, welcome to our application :)'
LOGGED_OUT_MESSAGE = 'You are logged out now :)'
LOGOUT_FAILED = 'There is a problem with the logout, please try later. If it does not work, ' \
                'you can close directly the application'

REGISTRATION_FAILED = 'Registration failed, please check the data you insert'
REGISTRATION_OK_WELCOME = 'Registration done, now you can start use our application :) '

RESERVATION_LIST_RETRIEVE_FAILED = 'Is not possible retrieve your reservation list'
NO_RESERVATION_FOUND_FOR_USER = 'You have not reservations yet, but you can create one if you want'
RESERVATION_FORMATTER = '%-20s %-30s %-20s %-20s %-20s %-20s'

DELETE_FAILED = 'Is not possible to delete this reservation'
NEW_RESERVATION_FAILED = 'Is not possible to add this reservation'

DATE_CREATION_ERROR = f'Please remember that the correct date format is: yyyy-mm-dd, in addition remember to put the ' \
                      f'right values for years (max = {datetime.MAXYEAR}), month (min = 1, ' \
                      f'max = 12), and days in according to the month'

DELETE_OK = ' correctly deleted '
DELETE_FAILED_ID_NOT_FOUND = 'There is not a reservation with the id chosen, please check it and try another time '

INT_FIELD_ERROR = 'The value you insert is not in the right format, remember that it has to be a number'

NEW_RESERVATION_CORRECTLY_ADDED = 'The reservation is added correctly, you can see it with other ones on the screen :)'

PASSWORDS_DIFFERENT_ON_REGISTRATION_ERROR_MESSAGE = 'Passwords are different, please write them another time: '
DATE_PATTERN = '%Y-%m-%d'
SUCCESS_ACTION_COLOR = 'green'
FAIL_ACTION_COLOR = 'red'
API_SERVER = 'http://127.0.0.1:8000/api/v1'
