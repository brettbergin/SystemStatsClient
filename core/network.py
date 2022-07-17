#!/usr/bin/env python3

import re
import socket
import psutil
import humanfriendly as bc


class NetworkInfo(object):
    def __init__(self, config):
        self.config = config

    def net_data(self):
        """
        Collects Network Details From All Interfaces
        On System.  Returns A Dictionary Object Of
        The Network Statistics Collected.
        """

        try:
            net_stat = psutil.net_io_counters()
            
            formatted_net_stat = {
                "bytes_sent": bc.format_size(net_stat.bytes_sent),
                "bytes_recvd": bc.format_size(net_stat.bytes_recv),
                "packets_sent": bc.format_size(net_stat.packets_sent),
                "packets_recvd": bc.format_size(net_stat.packets_recv),
                "err_pkt_in": bc.format_size(net_stat.errin),
                "err_pkt_out": bc.format_size(net_stat.errout),
                "dropped_pkt_in": bc.format_size(net_stat.dropin),
                "dropped_pkt_out": bc.format_size(net_stat.dropout),
            }

            return formatted_net_stat

        except Exception as error:
            self.config.log.error(f"Failed network data lookup. Error: {error}")
            return None

    def hostname(self):
        """
        Obtains the system hostname and returns
        as a string object.
        """
        try:
            return socket.gethostname()

        except Exception as error:
            self.config.log.error(f"Failed hostname lookup. Error: {error}")
            return None

    def ip_address(self):
        """
        Gets the IPv4 addresses from all network interfaces.

        Returns a dictionary object with a list of discovered interfaces.
        """
        ipv4_pattern = r"((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))"
        interface_list = []
        try:
            net_addrs = psutil.net_if_addrs()

            for interface_id, interface_data in net_addrs.items():
                for inter in interface_data:

                    if (
                        not len(
                            [
                                match[0]
                                for match in re.findall(ipv4_pattern, inter.address)
                            ]
                        )
                        > 0
                    ):
                        continue

                    interface_list.append({interface_id: inter.address})

            return {"interfaces": interface_list}

        except Exception as error:
            self.config.log.error(f"Failed ip lookup. Error: {error}")
            return None
