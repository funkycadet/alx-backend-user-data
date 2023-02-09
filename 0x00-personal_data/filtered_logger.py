#!/usr/bin/env python3
""" Filtered logger module
"""
import logging
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=List[str]) -> str:
        """ __init__ method
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        redact the message of LogRecord instance
        """
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR
        )
        return redacted
