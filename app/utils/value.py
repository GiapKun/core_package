from enum import Enum
import datetime
import uuid
import time
import random
import string

class UserRoles(Enum):
    USER = "user"
    ADMIN = "admin"
    
class OrderBy(Enum):
    DECREASE = "desc"
    ASCENDING = "asc"
    
class DataFormat(Enum):
    DATE = r"%Y-%m-%d"
    DATE_TIME = r"%Y-%m-%d %H:%M:%S"
    EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,10}\b"
    PHONE_REGEX = r"^\d{10}$"

class Values:
    @staticmethod
    def get_uuid():
        return str(uuid.uuid4())

    @staticmethod
    def get_current_datetime_string():
        timezone_offset = datetime.timedelta(hours=7)
        timezone = datetime.timezone(timezone_offset)

        current_datetime = datetime.datetime.now(timezone)
        dt_string = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
        return dt_string

    @staticmethod
    def get_current_timestamp():
        return time.time()

    @staticmethod
    def random_password(number: int = 20):
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        result_str = "".join(random.choice(letters) for _ in range(number))
        return result_str

    @staticmethod
    def generate_otp(number: int = 6):
        result_str = "".join(random.choice(string.digits) for i in range(number))
        return result_str

    @staticmethod
    def random_choice_with_weights(options, option_weights):
        """
        Randomly selects an element from the given options based on the provided weights.
        *Ensure that the weights add up to 1.
        Examples:
            >>> options = ['apple', 'banana', 'cherry']
            >>> option_weights = [0.1, 0.2, 0.7]
            >>> random_choice_with_weights(options, option_weights)
            'cherry'
        """

        # Randomly select a server based on the given weights
        return random.choices(options, weights=option_weights, k=1)[0]

    @staticmethod
    def random_password_with_special_chars(password_length=14, special_chars_count=2, digits_count=3):
        total_special_chars = special_chars_count + digits_count
        if password_length <= total_special_chars:
            raise ValueError(f"Password must be at least {total_special_chars} characters long")

        digits = "".join(random.choice(string.digits) for _ in range(digits_count))
        special_chars = "".join(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?") for _ in range(special_chars_count))
        remaining_length = password_length - total_special_chars
        letters = "".join(random.choice(string.ascii_letters) for _ in range(remaining_length))

        password = list(digits + special_chars + letters)
        random.shuffle(password)
        return "".join(password)

    @staticmethod
    def random_password_with_custom_chars(password_length=12, custom_chars_count=2, digits_count=3):
        total_custom_chars = custom_chars_count + digits_count
        if password_length <= total_custom_chars:
            raise ValueError(f"Password must be at least {total_custom_chars} characters long")

        digits = "".join(random.choice(string.digits) for _ in range(digits_count))
        custom_chars = "".join(random.choice(string.ascii_uppercase) for _ in range(custom_chars_count))
        remaining_length = password_length - total_custom_chars
        letters = "".join(random.choice(string.ascii_letters) for _ in range(remaining_length))

        password = list(digits + custom_chars + letters)
        random.shuffle(password)
        return "".join(password)

    @staticmethod
    def generate_random_promotion_code(number: int = 7):
        letters = string.ascii_uppercase
        result_str = "".join(random.choice(letters) for _ in range(number))
        return result_str