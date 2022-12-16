import datetime
import re
from dataclasses import dataclass, InitVar, field
from typing import Any

import valid8
from dateutil.relativedelta import relativedelta
from typeguard import typechecked

from beach_resort_reservation import domain_utils
from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class NumberOfSeats:
    value: int

    def __post_init__(self):
        valid8.validate('number of seats value', self.value, min_value=domain_utils.MIN_NUMBER_OF_SEATS,
                        max_value=domain_utils.MAX_NUMBER_OF_SEATS, help_msg=domain_utils.NUMBER_OF_SEATS_HELP_MESSAGE)

    def __str__(self):
        return f'{self.value}'


@typechecked
@dataclass(frozen=True, order=True)
class ReservedUmbrellaID:
    value: int

    def __post_init__(self):
        valid8.validate('reserved umbrella id', self.value, min_value=domain_utils.MIN_NUMBER_UMBRELLA_ID,
                        max_value=domain_utils.MAX_NUMBER_UMBRELLA_ID, help_msg=domain_utils.UMBRELLA_ID_HELP_MESSAGE)

    def __str__(self):
        return f'{self.value}'


@typechecked
@dataclass(frozen=True, order=True)
class Price:
    __parse_pattern = re.compile(r'(?P<euro>\d{0,11})(?:\.(?P<cents>\d{1,2}))?')
    value_in_cents: int
    private_key: InitVar[Any] = field(default='')

    __max_value = 10_000_000_000 - 1
    __private_key = object()

    def __post_init__(self, private_key):
        valid8.validate('private_key', private_key, equals=self.__private_key)
        valid8.validate('value_in_cents', self.value_in_cents, min_value=0, max_value=self.__max_value)

    @staticmethod
    def create_price(euros: int, cents: int) -> 'Price':
        valid8.validate('euros', euros, min_value=0, max_value=Price.__max_value // 100)
        valid8.validate('cents', cents, min_value=0, max_value=99)
        value_in_cents = euros * 100 + cents
        return Price(value_in_cents, Price.__private_key)

    @property
    def euros(self) -> int:
        return self.value_in_cents // 100

    @property
    def cents(self) -> int:
        return self.value_in_cents % 100

    def __str__(self):
        return f'{self.euros}.{self.cents:02}'

    @staticmethod
    def parse(value: str) -> 'Price':
        m = Price.__parse_pattern.fullmatch(value)
        valid8.validate('value', m)
        euro = m.group('euro')
        cents = m.group('cents') if m.group('cents') else 0
        return Price.create_price(int(euro), int(cents))


@typechecked
@dataclass(frozen=True, order=True)
class ReservationID:
    value: int

    def __post_init__(self):
        valid8.validate('reservation id', self.value, min_value=0)

    def __str__(self):
        return f'{self.value}'


@typechecked
@dataclass(frozen=True, order=True)
class ReservationFromServer:
    number_of_seats: NumberOfSeats
    umbrella_id: ReservedUmbrellaID
    start_date: datetime.date
    end_date: datetime.date
    price: Price
    id: ReservationID

    def __post_init__(self):
        valid8.validate('end date validation', self.end_date, min_value=self.start_date,
                        max_value=self.start_date + relativedelta(
                            months=domain_utils.MAX_DATE_DELTA_MONTHS_END_DATE),
                        help_msg=domain_utils.END_DATE_RESERVATION_ERROR)


@typechecked
@dataclass(frozen=True, order=True)
class NewReservation:
    number_of_seats: NumberOfSeats
    umbrella_id: ReservedUmbrellaID
    start_date: datetime.date
    end_date: datetime.date

    def __post_init__(self):
        valid8.validate('end date validation', self.end_date, min_value=self.start_date,
                        max_value=self.start_date + relativedelta(
                            months=domain_utils.MAX_DATE_DELTA_MONTHS_END_DATE),
                        help_msg=domain_utils.END_DATE_RESERVATION_ERROR)


@typechecked
@dataclass(frozen=True, order=True)
class Username:
    value: str

    def __post_init__(self):
        valid8.validate('username', self.value, min_len=1, max_len=150, custom=pattern(domain_utils.USERNAME_REGEX),
                        help_msg=domain_utils.USERNAME_HELP_MESSAGE_ON_CREATION)

    def __str__(self):
        return f'username: {self.value}'


@typechecked
@dataclass(frozen=True, order=True)
class Password:
    value: str

    def __post_init__(self):
        valid8.validate('password', self.value, min_len=8, max_len=150, custom=pattern(domain_utils.PASSWORD_REGEX),
                        help_msg=domain_utils.PASSWORD_HELP_MESSAGE_ON_CREATION)


@typechecked
@dataclass(frozen=True, order=True)
class Email:
    value: str

    def __post_init__(self):
        valid8.validate('email', self.value, max_len=200,
                        custom=pattern(domain_utils.EMAIL_REGEX),
                        help_msg=domain_utils.EMAIL_HELP_MESSAGE_ON_CREATION)

    def __str__(self):
        return f'email: {self.value}'
