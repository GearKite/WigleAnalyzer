from datetime import datetime, timedelta
from dateutil import parser
import re


def parse_datetime(input_str: str | None) -> datetime:
    # Check for relative time formats (e.g., "12h", "2d", "30m")
    relative_time_pattern = re.compile(r"^\d+\s*[smhdwMy]$", re.IGNORECASE)

    if input_str is None:
        return None

    # Check if the input matches a relative time format
    if relative_time_pattern.match(input_str):
        # Extract the amount and unit
        amount = int(input_str[:-1])
        unit = input_str[-1]

        now = datetime.now()

        if unit == "s":
            return now - timedelta(seconds=amount)
        elif unit == "m":
            return now - timedelta(minutes=amount)
        elif unit == "h":
            return now - timedelta(hours=amount)
        elif unit == "d":
            return now - timedelta(days=amount)
        elif unit == "w":
            return now - timedelta(weeks=amount)
        elif unit == "M":
            return now - timedelta(days=30 * amount)  # Approximation for months
        elif unit == "y":
            return now - timedelta(days=365 * amount)  # Approximation for years

    # Try to parse the input string as a date/time
    try:
        parsed_date = parser.parse(input_str)
        return parsed_date
    except ValueError:
        raise ValueError(
            "Input format not recognized. Please use formats like YYYY-MM-DD, HH:MM, or relative time (e.g., 12h, 2d)."
        )
