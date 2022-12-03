import getpass
import json
from unittest.mock import patch, Mock, call

from requests import Response, get

import beach_resort_reservation
from beach_resort_reservation import app_utils, domain_utils
from beach_resort_reservation.app import main


class TestApp:
    @patch('builtins.input', side_effect=['0'])
    @patch('builtins.print')
    def test_app_run_must_show_login_menu(self, mocked_print: Mock, mocked_input: Mock):
        main('__main__')
        mocked_print.assert_any_call('*** ' + app_utils.APP_NAME_LOGIN + ' ***')
        mocked_print.assert_any_call('0:\tExit')
        mocked_print.assert_any_call(app_utils.APP_EXIT_MESSAGE)
        mocked_input.assert_called()

    @patch('builtins.input', side_effect=['1', 'cris', '0'])
    @patch('builtins.print')
    @patch.object(getpass, 'getpass', return_value='pass')
    def test_app_do_login_must_print_error_message_if_credentials_are_invalids(self, mocked_input, mocked_print,
                                                                               mocked_getpass):
        getpass.return_value = 'pass'

        response_mock = Response()
        response_mock.status_code = 400

        with patch.object(beach_resort_reservation.app.App, 'do_login_request', return_value=response_mock):
            main('__main__')

            mocked_print.assert_any_call(app_utils.LOGIN_FAILED)

    @patch('builtins.input', side_effect=['1', 'cris', '0'])
    @patch('builtins.print')
    @patch.object(getpass, 'getpass', return_value='password')
    def test_app_do_login_must_print_welcome_if_input_data_is_valid(self, mocked_input, mocked_print, mocked_getpass):
        response_mock = Response()
        response_mock.status_code = 200
        response_mock._content = b'{ "key" : "key value" }'
        with patch.object(beach_resort_reservation.app.App, 'do_login_request', return_value=response_mock):
            main('__main__')

            mocked_print.assert_any_call(app_utils.LOGIN_OK_WELCOME)

    @patch('builtins.input', side_effect=['2', 'cris', 'email@lib.it', '0'])
    @patch('builtins.print')
    @patch.object(getpass, 'getpass', side_effect=['password', 'password1', 'password', 'password'])
    def test_app_do_registration_must_ask_another_time_for_password_if_the_two_passwords_are_not_equals(self,
                                                                                                        mocked_input,
                                                                                                        mocked_print,
                                                                                                        mocked_getpass):
        main('__main__')
        mocked_print.assert_any_call(app_utils.PASSWORDS_DIFFERENT_ON_REGISTRATION_ERROR_MESSAGE)

    @patch('builtins.input', side_effect=['2', 'cris', 'email@lib.it', '0'])
    @patch('builtins.print')
    @patch.object(getpass, 'getpass', side_effect=['passw', 'password', 'password'])
    def test_app_do_registration_must_ask_another_time_for_password_the_password_is_not_well_formed(self, mocked_input,
                                                                                                    mocked_print,
                                                                                                    mocked_getpass):
        main('__main__')
        mocked_print.assert_any_call(domain_utils.PASSWORD_HELP_MESSAGE_ON_CREATION)

    @patch('builtins.input', side_effect=['2', 'cris', 'email@', 'email@email.com', '0'])
    @patch('builtins.print')
    @patch.object(getpass, 'getpass', side_effect=['password', 'password'])
    def test_app_do_registration_must_ask_another_time_for_email_if_the_email_is_not_well_formed(self, mocked_input,
                                                                                                 mocked_print,
                                                                                                 mocked_getpass):
        main('__main__')
        mocked_print.assert_any_call(domain_utils.EMAIL_HELP_MESSAGE_ON_CREATION)

    @patch('builtins.input', side_effect=['2', '', 'username', 'email@email.com', '0'])
    @patch('builtins.print')
    @patch.object(getpass, 'getpass', side_effect=['password', 'password'])
    def test_app_do_registration_must_ask_another_time_for_username_if_the_username_is_not_well_formed(self,
                                                                                                       mocked_input,
                                                                                                       mocked_print,
                                                                                                       mocked_getpass):
        main('__main__')
        mocked_print.assert_any_call(domain_utils.USERNAME_HELP_MESSAGE_ON_CREATION)

    @patch('builtins.input', side_effect=['2', 'cris', 'email@lib.it', '0'])
    @patch('builtins.print')
    @patch.object(getpass, 'getpass', side_effect=['password', 'password'])
    def test_app_do_registration_must_print_error_messages_if_data_is_invalid(self, mocked_input, mocked_print,
                                                                              mocked_getpass):
        response_mock = Response()
        response_mock.status_code = 400
        response_mock._content = b'{ "non_field_errors" : ["non field error"], "username": ["username error"],' \
                                 b'"password1": ["password1 error"], "password2": ["password2 error"],' \
                                 b'"email": ["email error"] }'

        with patch.object(beach_resort_reservation.app.App, 'do_registration_request', return_value=response_mock):
            main('__main__')

            mocked_print.assert_any_call(app_utils.REGISTRATION_FAILED)
            mocked_print.assert_any_call('\tnon field error')
            mocked_print.assert_any_call('\tusername error')
            mocked_print.assert_any_call('\tpassword1 error')
            mocked_print.assert_any_call('\tpassword2 error')
            mocked_print.assert_any_call('\temail error')

    @patch('builtins.input', side_effect=['2', 'cris', 'email@lib.it', '0'])
    @patch('builtins.print')
    @patch.object(getpass, 'getpass', side_effect=['password', 'password'])
    def test_app_do_registration_must_print_welcome_if_input_data_is_valid(self, mocked_input, mocked_print,
                                                                           mocked_getpass):
        response_mock = Response()
        response_mock.status_code = 201
        response_mock._content = b'{ "key" : "key value" }'
        with patch.object(beach_resort_reservation.app.App, 'do_registration_request', return_value=response_mock):
            main('__main__')
            mocked_print.assert_any_call(app_utils.REGISTRATION_OK_WELCOME)

    @patch('builtins.input', side_effect=['1', 'cris', '0'])
    @patch('builtins.print')
    @patch.object(getpass, 'getpass', return_value='password')
    def test_app_do_login_must_change_menu_if_credential_are_valid(self, mocked_input, mocked_print, mocked_getpass):
        response_mock = Response()
        response_mock.status_code = 200
        response_mock._content = b'{ "key" : "key value" }'
        with patch.object(beach_resort_reservation.app.App, 'do_login_request', return_value=response_mock):
            main('__main__')

            mocked_print.assert_any_call(app_utils.LOGIN_OK_WELCOME)
            mocked_print.assert_any_call('1:\tMake a new reservation')
            mocked_print.assert_any_call('2:\tDelete a reservation')
            mocked_print.assert_any_call('4:\tLogout')

    @patch('builtins.input', side_effect=['1', 'cris', '4', '0'])
    @patch('builtins.print')
    @patch.object(getpass, 'getpass', return_value='password')
    def test_app_do_logout_must_print_a_confirm_message_if_all_is_correct(self, mocked_input, mocked_print,
                                                                          mocked_getpass):
        response_mock = Response()
        response_mock.status_code = 200
        response_mock._content = b'{ "key" : "key value" }'
        with patch.object(beach_resort_reservation.app.App, 'do_login_request', return_value=response_mock):
            with patch.object(beach_resort_reservation.app.App, 'do_logout_request',
                              return_value=response_mock):
                main('__main__')
                mocked_print.assert_any_call(app_utils.LOGGED_OUT_MESSAGE)

    @patch('builtins.input', side_effect=['1', 'cris', '4', '0'])
    @patch('builtins.print')
    @patch.object(getpass, 'getpass', return_value='password')
    def test_app_do_logout_must_print_an_error_message_if_all_is_correct(self, mocked_input, mocked_print, getpass):
        getpass.return_value = 'pass'

        response_mock_login = Response()
        response_mock_login.status_code = 200
        response_mock_login._content = b'{ "key" : "key value" }'

        response_mock_logout = Response()
        response_mock_logout.status_code = 400
        with patch.object(beach_resort_reservation.app.App, 'do_login_request', return_value=response_mock_login):
            with patch.object(beach_resort_reservation.app.App, 'do_logout_request',
                              return_value=response_mock_logout):
                main('__main__')
                mocked_print.assert_any_call(app_utils.LOGOUT_FAILED)
