#!/usr/bin/env python3

import psutil
import humanfriendly as bc


class MemoryInfo(object):
    def __init__(self, config):
        self.config = config

    def mem_data(self):
        """ """

        try:
            mem = psutil.virtual_memory()
            formatted_mem = {
                "total_memory": bc.format_size(mem.total),
                "available_memory": bc.format_size(mem.available),
                "percent": mem.percent,
                "used": bc.format_size(mem.used),
                "free": bc.format_size(mem.free),
                "active": bc.format_size(mem.active),
                "inactive": bc.format_size(mem.inactive),
                "wired": bc.format_size(mem.wired),
            }

            return formatted_mem

        except Exception as error:
            self.config.log.error(f"Failed memory lookup. Error: {error}")
            return None
