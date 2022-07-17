#!/usr/bin/env python3

import psutil
import humanfriendly as bc


class DiskInfo(object):
    def __init__(self, config):
        self.config = config

    def partitions(self):
        """
        Collects All Mounted Partitions On System.
        Iterates Through Each Partition, Ignoring Devices
        Which Cannot Be Written To. Returns a List Object
        With The Mount Point As Its Key, And Disk Attributes
        As Its Value.
        """

        try:
            disks = []
            partitions = psutil.disk_partitions()
            for p in partitions:
                if p.mountpoint in ("/", "C:"):
                    stats = psutil.disk_usage(p.mountpoint)
                    disks.append(
                        {
                            "mount_point": p.mountpoint,
                            "total": bc.format_size(stats.total),
                            "used": bc.format_size(stats.used),
                            "free": bc.format_size(stats.free),
                            "percent": stats.percent,
                        }
                    )

            return disks

        except Exception as error:
            self.config.log.error(
                f"Unable to fetch disk partition info. Error: {error}"
            )
            return None
