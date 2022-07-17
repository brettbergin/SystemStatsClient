#!/usr/bin/env python3


import os
from .logger import Logger


class Config(object):
    def __init__(self):
        self.log_level = "DEBUG"
        self.log = Logger(self.log_level).setup_logging()
        self.api_username = os.environ["SS_API_USER"]
        self.api_password = os.environ["SS_API_PASSWORD"]
        self.api_base_url = "http://127.0.0.1:5000"
