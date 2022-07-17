#!/usr/bin/env python3

import platform
import datetime

import psutil



class SystemInfo(object):
    def __init__(self, config):
        self.config = config

    def operating_system(self):
        """ """
        try:
            opersys = platform.platform()
            return opersys

        except Exception as error:
            self.config.log.error(f"Failed operating system lookup. Error: {error}")
            return None

    def users(self):
        """ """

        try:
            active_users = []

            users = psutil.users()
            for user in users:
                active_users.append(
                    {
                        "user_name": user.name,
                        "terminal": user.terminal,
                        "host": user.host,
                        "started": datetime.datetime.fromtimestamp(int(user.started)),
                    }
                )

            return active_users

        except Exception as error:
            self.config.log.error(f"Failed user lookup. Error: {error}")
            return None

    def uptime(self):
        """ """

        try:
            boot = datetime.datetime.fromtimestamp(int(psutil.boot_time()))
            boot_time = datetime.datetime(
                boot.year, boot.month, boot.day, boot.hour, boot.minute
            )
            now = datetime.datetime.now()

            return now - boot_time

        except Exception as error:
            self.config.log.error(f"Failed uptime lookup. Error: {error}")
            return None
