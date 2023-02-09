#!/usr/bin/env python3
""" Filtered logger module
"""
import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """ filter_datum function """
    for field in fields:
        # pattern = f"{field}=[^;]+"
        # message = re.sub(pattern, f"{field}={redaction}", message)
        message = re.sub(
            field+'=.*?'+separator, field+'='+redaction+separator, message
        )
    return message
