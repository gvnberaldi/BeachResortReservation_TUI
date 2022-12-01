from dataclasses import dataclass

import valid8
from typeguard import check_argument_types, check_return_type, typechecked

from beach_resort_reservation import domain_utils


@typechecked
@dataclass(frozen=True, order=True)
class Reservation:
    pass



@typechecked
@dataclass(frozen=True, order=True)
class NumberOfSeats:
    value: int

    def __post_init__(self):
        valid8.validate('number of seats value',self.value, min_value=domain_utils.MIN_NUMBER_OF_SEATS, max_value=domain_utils.MAX_NUMBER_OF_SEATS)

    def __str__(self):
        return f'number of seats: {self.value}'


@typechecked
@dataclass(frozen=True, order=True)
class ReservedUmbrellaID:
    value: int

    def __post_init__(self):
        valid8.validate('reserved umbrella id',self.value, min_value=domain_utils.MIN_NUMBER_UMBRELLA_ID, max_value=domain_utils.MAX_NUMBER_UMBRELLA_ID)

    def __str__(self):
        return f'umbrella id: {self.value}'


