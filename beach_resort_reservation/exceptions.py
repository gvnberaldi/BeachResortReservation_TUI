import typeguard

from beach_resort_reservation import app_utils


@typeguard.typechecked
class IntegerInputException(Exception):
    def __init__(self, help_msg: str = app_utils.INT_FIELD_ERROR):
        self.help_msg = help_msg
        super().__init__(self.help_msg)


@typeguard.typechecked
class DateInputException(Exception):
    def __init__(self, help_msg: str = app_utils.DATE_CREATION_ERROR):
        self.help_msg = help_msg
        super().__init__(self.help_msg)
