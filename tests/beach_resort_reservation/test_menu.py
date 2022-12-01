import builtins
from unittest.mock import patch, Mock, call

import pytest
from valid8 import ValidationError

from beach_resort_reservation.menu import Entry, Key, Description, Menu


class TestEntry:

    @patch('builtins.print')
    def test_entry_on_selected_function_have_to_call_exactly_what_we_pass(self, mocked_print:Mock):
        entry_key = Entry(Key('0'), Description('test entry'), on_selected= lambda: print('test print'))
        entry_key.on_selected()
        assert mocked_print.mock_calls==[call('test print')]

    @patch('builtins.print')
    def test_entry_on_selected_function_have_to_call_it_only_one_time(self, mocked_print: Mock):
        entry_key = Entry(Key('0'), Description('test entry'), on_selected=lambda: print('test print'))
        entry_key.on_selected()
        assert mocked_print.call_count == 1


class TestKey:

    def test_key_with_wrong_value_raises_a_validation_error(self):
        with pytest.raises(ValidationError):
            Key('***')
    def test_key_with_correct_value_has_to_create_a_key(self):
        assert Key('1').value =='1'

class TestDescription:

    def test_description_with_wrong_value_raises_a_validation_error(self):
        with pytest.raises(ValidationError):
            Description('a' * 901)
        with pytest.raises(ValidationError):
            Description('')
        with pytest.raises(ValidationError):
            Description('****')
    def test_key_with_correct_value_has_to_create_a_key(self):
        assert Description('a'*900).value == 'a'*900




class TestMenu:
    def test_menu_with_no_exit_must_raise_an_exception(self):
        with pytest.raises(ValidationError):
            Menu.Builder(Description('menu')).with_entry(Entry.create('1', 'entry with not exit', on_selected=lambda: print('test'), is_exit=False)).build()

    def test_menu_with_correct_entries_must_create_a_menu(self):
            menu=Menu.Builder(Description('menu'))\
                .with_entry(Entry.create('1', 'entry with not exit', on_selected=lambda: print('test'), is_exit=False))\
                .with_entry(Entry.create('0', 'entry with not exit', on_selected=lambda: print('test'), is_exit=True))\
                .build()

            assert menu.description.value=='menu'


    @patch('builtins.input', side_effect=['1','0'])
    @patch('builtins.print')
    def test_menu_call_the_method_on_selected_entry(self, mocked_print:Mock, mocked_input:Mock):
        menu = Menu.Builder(Description('menu')) \
            .with_entry(Entry.create('1', 'entry with not exit', on_selected=lambda: print('test1'), is_exit=False)) \
            .with_entry(Entry.create('0', 'entry with not exit', on_selected=lambda: print('exit'), is_exit=True)) \
            .build()

        menu.run()

        mocked_print.assert_any_call('exit')
        mocked_input.assert_called()



