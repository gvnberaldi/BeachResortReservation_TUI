from unittest.mock import patch

import pytest
from valid8 import ValidationError

import beach_resort_reservation
from beach_resort_reservation.domain import NumberOfSeats, ReservedUmbrellaID


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
