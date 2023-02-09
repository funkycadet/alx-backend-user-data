#!/usr/bin/env python3
""" Filtered logger module
"""
import logging
import mysql.connector
import os
import re
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


def get_logger() -> logging.Logger:
    """
    Return a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()

    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    get_db function
    Retrieve data from db
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(
        user=user, password = password, host=host, database=db_name
    )
    return conn
