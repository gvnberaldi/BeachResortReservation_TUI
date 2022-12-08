from datetime import datetime
from unittest.mock import patch

import pytest
from valid8 import ValidationError
from dateutil.relativedelta import *

import beach_resort_reservation
from beach_resort_reservation import domain_utils
from beach_resort_reservation.domain import NumberOfSeats, ReservedUmbrellaID, Reservation, Password, Username, Email, \
    ReservationID, Price


class TestNumberOfSeats:
    @pytest.mark.parametrize("test_input", [5, 6, 1000])
    def test_number_of_seats_more_than_maximum_number_must_raise_a_validation_error(self, test_input):
        with pytest.raises(ValidationError):
            NumberOfSeats(test_input)

    @pytest.mark.parametrize("test_input", [-1, 0, 1])
    def test_number_of_seats_less_than_minimum_number_must_raise_a_validation_error(self, test_input):
        with pytest.raises(ValidationError):
            NumberOfSeats(test_input)

    @pytest.mark.parametrize("test_input", [2, 3, 4])
    def test_number_of_seats_between_min_and_max_must_be_accepted(self, test_input):
        seats = NumberOfSeats(test_input)
        assert seats.value == test_input


class TestReservationUmbrellaID:
    @pytest.mark.parametrize("test_input", [51, 52, 1000, 100])
    def test_umbrella_id_more_than_maximum_number_must_raise_a_validation_error(self, test_input):
        with pytest.raises(ValidationError):
            ReservedUmbrellaID(test_input)

    @pytest.mark.parametrize("test_input", [-1, -2, -100])
    def test_umbrella_id_less_than_minimum_number_must_raise_a_validation_error(self, test_input):
        with pytest.raises(ValidationError):
            ReservedUmbrellaID(test_input)

    @pytest.mark.parametrize("test_input", [2, 3, 4, 1, 49, 50, 0])
    def test_umbrella_id_between_min_and_max_must_be_accepted(self, test_input):
        umbrella_id = ReservedUmbrellaID(test_input)
        assert umbrella_id.value == test_input


class TestReservationID:
    @pytest.mark.parametrize("test_input", [-1, -100, -1000])
    def test_reservation_id_more_than_maximum_number_must_raise_a_validation_error(self, test_input):
        with pytest.raises(ValidationError):
            ReservationID(test_input)

    @pytest.mark.parametrize("test_input", [2, 3, 4, 1, 49, 50, 0])
    def test_reservation_id_more_than_min_value_must_be_accepted(self, test_input):
        reservation_id = ReservationID(test_input)
        assert reservation_id.value == test_input


class TestPrice:
    def test_negative_price_must_raise_a_validation_error(self):
        with pytest.raises(ValidationError):
            euros: int = -100
            cents: int = 99
            Price.create_price(euros, cents)
        with pytest.raises(ValidationError):
            euros: int = 100
            cents: int = -99
            Price.create_price(euros, cents)

    def test_price__with_cents_more_than_99_must_raise_a_validation_error(self):
        with pytest.raises(ValidationError):
            euros: int = 100
            cents: int = 100
            Price.create_price(euros, cents)

    def test_price_with_euros_more_than_max_must_raise_a_validation_error(self):
        with pytest.raises(ValidationError):
            euros: int = 10_000_000_000 // 100
            cents: int = 100
            Price.create_price(euros, cents)

    def test_price_must_create_a_Price_if_cents_and_euros_are_correct(self):
        values = [(1, 99), (100, 10), (1000, 89), (27, 30)]
        for value in values:
            p = Price.create_price(value[0], value[1])
            assert p.euros == value[0] and p.cents == value[1]

    def test_price_must_create_a_Price_if_cents_and_euros_are_correct_in_parsing(self):
        values = ['1.99', '1.60', '1.88']
        for value in values:
            p = Price.parse(value)
            assert str(p) == value
class TestReservation:
    @pytest.mark.parametrize("reservation_input",
                             [Reservation(number_of_seats=NumberOfSeats(2), umbrella_id=ReservedUmbrellaID(1), \
                                          reservation_start_date=(datetime.today()).date(), \
                                          reservation_end_date=(datetime.today() + relativedelta(days=+1)).date()),
                              Reservation(number_of_seats=NumberOfSeats(2), umbrella_id=ReservedUmbrellaID(1), \
                                          reservation_start_date=datetime.today().date(), \
                                          reservation_end_date=(datetime.today() + relativedelta(
                                              months=domain_utils.MAX_DATE_DELTA_MONTHS_END_DATE)).date()),
                              ])
    def test_reservation_with_correct_data_must_raise_validation_error(self, reservation_input):
        assert reservation_input.number_of_seats.value == 2

    @pytest.mark.parametrize("reservation_input", [
        (2, 1, datetime.today().date(), (datetime.today() + relativedelta(days=-1)).date()),
        (2, 1, datetime.today().date(),
         (datetime.today() + relativedelta(months=domain_utils.MAX_DATE_DELTA_MONTHS_END_DATE, days=1)).date()),
        (2, 1, datetime.today().date(), (datetime.today() + relativedelta(years=1)).date()),
        (2, 1, datetime.today().date(),
         (datetime.today() + relativedelta(months=-domain_utils.MAX_DATE_DELTA_MONTHS_END_DATE)).date())

    ])
    def test_reservation_with_wrong_end_date_must_raise_validation_error(self, reservation_input):
        with pytest.raises(ValidationError):
            Reservation(number_of_seats=NumberOfSeats(reservation_input[0]),
                        umbrella_id=ReservedUmbrellaID(reservation_input[1]), \
                        reservation_start_date=reservation_input[2], \
                        reservation_end_date=reservation_input[3])


class TestPassword:
    @pytest.mark.parametrize("password_input", [
        'a',
        'a' * 7,
        'b' * 151,
        'c' * 200,
        '+' * 4
    ])
    def test_password_must_raise_a_validation_error_if_the_length_is_not_well_formed(self, password_input):
        with pytest.raises(ValidationError):
            Password(password_input)

    @pytest.mark.parametrize("password_input", [
        'a' * 8,
        'abcjaslja*josj',
        'hellothisisapass',
        '1233456778',
        'b' * 150
    ])
    def test_password_must_raise_a_validation_error_if_the_length_is_well_formed(self, password_input):
        password = Password(password_input)
        assert password.value == password_input


class TestUsername:
    @pytest.mark.parametrize("username_input", [
        'a ',
        'a/',
        '',
        'c' * 200,
        '+' * 4
    ])
    def test_username_must_raise_a_validation_error_if_username_is_not_well_formed(self, username_input):
        with pytest.raises(ValidationError):
            Username(username_input)

    @pytest.mark.parametrize("username_input", [
        'a!@#$%^&_-',
        'jesunccl',
        'aaaaa87',
        'john_22'
    ])
    def test_username_must_raise_a_validation_error_if_username_is_well_formed(self, username_input):
        user = Username(username_input)
        assert user.value == username_input


class TestEmail:
    @pytest.mark.parametrize("email_input", [
        'a@...',
        'axss@ssss.i',
        'aaassa.it',
        'ccs.it@lib',
        ''
    ])
    def test_username_must_raise_a_validation_error_if_email_is_not_well_formed(self, email_input):
        with pytest.raises(ValidationError):
            Email(email_input)

    @pytest.mark.parametrize("email_input", [
        'cr@lib.it',
        'matt@bbb.com',
        'pip@chz.ch',
        '1809@email.org'
    ])
    def test_username_must_raise_a_validation_error_if_email_is_well_formed(self, email_input):
        email = Email(email_input)
        assert email.value == email_input
