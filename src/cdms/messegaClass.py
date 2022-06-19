import io
import json
import re
import sqlite3


class Messages:

    @staticmethod
    def falseNumber():
        return "Input is not a number, try again.\n"

    @staticmethod
    def wrongNumber():
        return "Option is not in the listed options or not a number, try again.\n"

    @staticmethod
    def badError():
        return "Bad input. Incident logged."

    