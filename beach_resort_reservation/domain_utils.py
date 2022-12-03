MIN_NUMBER_OF_SEATS = 2
MAX_NUMBER_OF_SEATS = 4

MIN_NUMBER_UMBRELLA_ID = 0
MAX_NUMBER_UMBRELLA_ID = 50

MAX_DATE_DELTA_MONTHS_END_DATE = 1

PASSWORD_REGEX = r'[A-Za-z\d@$!%*?&]+'
EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
USERNAME_REGEX = r'[a-zA-Z\d!@#$%^&_-]+'

PASSWORD_HELP_MESSAGE_ON_CREATION = 'Password cannot be empty, it must be at least 8 characters, and can contain ' \
                                    'numbers, letters and these special chars: @$!%*?&'


EMAIL_HELP_MESSAGE_ON_CREATION = 'Email must be in the right format, for example: example@domain.com'


USERNAME_HELP_MESSAGE_ON_CREATION = 'Username cannot be empty, it can contain only letters, numbers and ' \
                                    'these special chars !@#$%^&_-'
