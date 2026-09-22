from typing import Annotated

from pydantic import StringConstraints

PHONE_REGEX = r"^\+?[1-9]\d{1,14}$"

PhoneNumber = Annotated[
    str, StringConstraints(pattern=PHONE_REGEX, strip_whitespace=True, min_length=10, max_length=20)
]
