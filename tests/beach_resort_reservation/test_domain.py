from datetime import datetime
from unittest.mock import patch

import pytest
from valid8 import ValidationError
from dateutil.relativedelta import *

import beach_resort_reservation
from beach_resort_reservation import domain_utils
from beach_resort_reservation.domain import NumberOfSeats, ReservedUmbrellaID, Reservation


class TestNumberOfSeats:
    @pytest.mark.parametrize("test_input", [5,6,1000])
    def test_number_of_seats_more_than_maximum_number_must_raise_a_validation_error(self, test_input):

        with pytest.raises(ValidationError):
            NumberOfSeats(test_input)

    @pytest.mark.parametrize("test_input", [-1, 0, 1])
    def test_number_of_seats_less_than_minimum_number_must_raise_a_validation_error(self, test_input):
        with pytest.raises(ValidationError):
            NumberOfSeats(test_input)

    @pytest.mark.parametrize("test_input", [2, 3, 4])
    def test_number_of_seats_between_min_and_max_must_be_accepted(self, test_input):
        seats=NumberOfSeats(test_input)
        assert seats.value == test_input




class TestReservationUmbrellaID:
    @pytest.mark.parametrize("test_input", [51,52,1000,100])
    def test_umbrella_id_more_than_maximum_number_must_raise_a_validation_error(self, test_input):
        with pytest.raises(ValidationError):
            ReservedUmbrellaID(test_input)

    @pytest.mark.parametrize("test_input", [-1, -2, -100])
    def test_umbrella_id_less_than_minimum_number_must_raise_a_validation_error(self, test_input):
        with pytest.raises(ValidationError):
            ReservedUmbrellaID(test_input)

    @pytest.mark.parametrize("test_input", [2, 3, 4, 1, 49,50,0])
    def test_umbrella_id_between_min_and_max_must_be_accepted(self, test_input):
        umbrella_id=ReservedUmbrellaID(test_input)
        assert umbrella_id.value == test_input



class TestReservation:
    @pytest.mark.parametrize("reservation_input",
                             [ Reservation(number_of_seats=NumberOfSeats(2), umbrella_id=ReservedUmbrellaID(1), \
                                           reservation_start_date=(datetime.today()).date(), \
                                          reservation_end_date=(datetime.today()+relativedelta(days=+1)).date()),
                               Reservation(number_of_seats=NumberOfSeats(2), umbrella_id=ReservedUmbrellaID(1), \
                                           reservation_start_date=datetime.today().date(), \
                                           reservation_end_date=(datetime.today() + relativedelta(months=domain_utils.MAX_DATE_DELTA_MONTHS_END_DATE)).date()),
                              ])
    def test_reservation_with_correct_data_must_raise_validation_error(self, reservation_input):
        assert reservation_input.number_of_seats.value == 2

    @pytest.mark.parametrize("reservation_input",[
        (2, 1, datetime.today().date(), (datetime.today() + relativedelta(days=-1)).date()),
        (2, 1, datetime.today().date(), (datetime.today() + relativedelta(months=domain_utils.MAX_DATE_DELTA_MONTHS_END_DATE,days=1)).date()),
        (2, 1, datetime.today().date(), (datetime.today() + relativedelta(years=1)).date()),
        (2, 1, datetime.today().date(), (datetime.today() + relativedelta(months=-domain_utils.MAX_DATE_DELTA_MONTHS_END_DATE)).date())

    ])
    def test_reservation_with_wrong_end_date_must_raise_validation_error(self,reservation_input):
        with pytest.raises(ValidationError):

            Reservation(number_of_seats=NumberOfSeats(reservation_input[0]), umbrella_id=ReservedUmbrellaID(reservation_input[1]), \
                        reservation_start_date=reservation_input[2], \
                        reservation_end_date=reservation_input[3])

