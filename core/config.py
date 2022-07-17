#!/usr/bin/env python3


import os
from .logger import Logger


class Config(object):
    def __init__(self):
        self.log_level = "DEBUG"
        self.log = Logger(self.log_level).setup_logging()
