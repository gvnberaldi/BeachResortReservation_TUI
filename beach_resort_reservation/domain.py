import datetime
from dataclasses import dataclass

import valid8
from typeguard import check_argument_types, check_return_type, typechecked
from dateutil.relativedelta import relativedelta


from beach_resort_reservation import domain_utils
from validation.regex import pattern


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


@typechecked
@dataclass(frozen=True, order=True)
class Reservation:
    number_of_seats: NumberOfSeats
    umbrella_id: ReservedUmbrellaID
    reservation_start_date: datetime.date
    reservation_end_date: datetime.date

    def __post_init__(self):
        valid8.validate('end date validation', self.reservation_end_date, min_value=self.reservation_start_date,
                        max_value=self.reservation_start_date + relativedelta(months=domain_utils.MAX_DATE_DELTA_MONTHS_END_DATE))





@typechecked
@dataclass(frozen=True, order=True)
class Username:
    value: str

    def __post_init__(self):
        valid8.validate('username', self.value, min_len=1, max_len=150, help_msg='Username cannot be empty')

    def __str__(self):
        return f'username: {self.value}'



@typechecked
@dataclass(frozen=True, order=True)
class Password:
    value: str

    def __post_init__(self):
        valid8.validate('password', self.value, min_len=1, max_len=150, help_msg ='Password cannot be empty')


@typechecked
@dataclass(frozen=True, order=True)
class Email:
    value: str

    def __post_init__(self):
        valid8.validate('email', self.value,max_len=200, custom=pattern(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), help_msg='Email must be in the right format, for example: example@domain.com')

    def __str__(self):
        return f'username: {self.value}'


