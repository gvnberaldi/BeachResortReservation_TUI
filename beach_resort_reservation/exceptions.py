from beach_resort_reservation import app_utils


class IntegerInputException(Exception):

    def __init__(self, help_msg=app_utils.INT_FIELD_ERROR):
        self.help_msg = help_msg
        super().__init__(self.help_msg)

class DateInputException(Exception):

    def __init__(self, help_msg=app_utils.DATE_CREATION_ERROR):
        self.help_msg = help_msg
        super().__init__(self.help_msg)