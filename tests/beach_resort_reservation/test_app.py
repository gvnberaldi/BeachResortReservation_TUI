import getpass
import json
from unittest.mock import patch, Mock, call

from requests import Response, get

import beach_resort_reservation
from beach_resort_reservation import app_utils
from beach_resort_reservation.app import main


class TestApp:
    @patch('builtins.input', side_effect=['0'])
    @patch('builtins.print')
    def test_app_run_must_show_login_menu(self, mocked_print:Mock, mocked_input:Mock):
        main('__main__')
        mocked_print.assert_any_call('*** ' + app_utils.APP_NAME_LOGIN +' ***')
        mocked_print.assert_any_call('0:\tExit')
        mocked_print.assert_any_call(app_utils.APP_EXIT_MESSAGE)
        mocked_input.assert_called()


    def test_app_do_login_must_print_error_message_if_credentials_are_invalids(self):
        getpass.return_value='pass'

        response_mock = Response()
        response_mock.status_code=400


        with patch('builtins.input', side_effect=['1','cris', '0']):
            with patch('builtins.print') as mocked_print:
                with patch.object(getpass, 'getpass', return_value='pass'):
                    with patch.object(beach_resort_reservation.app.App, 'do_login_request', return_value= response_mock):
                        main('__main__')

                        mocked_print.assert_any_call(app_utils.LOGIN_FAILED)


    def test_app_do_login_must_print_welcome_if_input_data_is_valid(self):
        getpass.return_value='pass'

        response_mock = Response()
        response_mock.status_code = 200
        response_mock._content = b'{ "key" : "key value" }'

        with patch('builtins.input', side_effect=['1','cris', '0']):
            with patch('builtins.print') as mocked_print:
                with patch.object(getpass, 'getpass', return_value='pass'):
                    with patch.object(beach_resort_reservation.app.App, 'do_login_request', return_value= response_mock):
                        main('__main__')

                        mocked_print.assert_any_call(app_utils.LOGIN_OK_WELCOME)

    def test_app_do_registration_must_another_time_for_password_if_the_two_passwords_are_not_equals(self):

        with patch('builtins.input', side_effect=['2', 'cris', 'email', '0']):
            with patch('builtins.print') as mocked_print:
                with patch.object(getpass, 'getpass', side_effect=['pass', 'pass1', 'pass', 'pass']):
                        main('__main__')
                        mocked_print.assert_any_call('Passwords are different, please write them another time: ')

