#!/usr/bin/env python3

import json
import datetime
from datetime import timedelta


import requests 

from core.config import Config
from core.cpu import CPUInfo
from core.disk import DiskInfo
from core.memory import MemoryInfo
from core.network import NetworkInfo
from core.system import SystemInfo


class SystemProfiler(object):

    def __init__(self) -> None:
        self.config = Config()

        self.access_token, self.refresh_token = self._authenticate()
        if not self.access_token or not self.refresh_token:
            raise AttributeError("Missing Auth Tokens.")

        self.report_id = None

        self.cpu = CPUInfo(self.config)
        self.disk = DiskInfo(self.config)
        self.memory = MemoryInfo(self.config)
        self.network = NetworkInfo(self.config)
        self.system = SystemInfo(self.config)

    def _authenticate(self):
        r = requests.post(f"{self.config.api_base_url}/authenticate",
            json={
                "email":f"{self.config.api_username}",
                "password":f"{self.config.api_password}"
            },
            headers={"Content-Type": "application/json"}
        )
        if not r.status_code == 200:
            return None, None

        resp = r.json()
        return resp["access_token"], resp["refresh_token"]

    def _datetime_convertor(self, o):
        if isinstance(o, (datetime.datetime, timedelta)):
            return o.__str__()

    def register_new_report(self, target):
        r = requests.post(f"{self.config.api_base_url}/api/report/new", 
            headers={
                "Authorization": f"Bearer {self.access_token}", 
                "Content-Type": "application/json"
            },
            data=json.dumps({"target": f"{target}"})
        )

        if not r.status_code == 200:
            print(f"Unable to generate new report. API response status code: {r.status_code}")
            return None
        
        resp = r.json()
        self.report_id = resp["report_id"]
        return self.report_id

    def fetch_cpu_stats(self, target):
        cpu_data = self.cpu.cpu_data()
        # processes = self.cpu.processes()

        r = requests.post(f"{self.config.api_base_url}/api/cpu/info", 
            headers={
                "Authorization": f"Bearer {self.access_token}", 
                "Content-Type": "application/json"
            },
            data=json.dumps(
                {"cpu_data": cpu_data, "target": target, "report_id": self.report_id}, 
                    default=self._datetime_convertor)
        )
        return True

    def fetch_disk_stats(self, target):
        disk_data = self.disk.partitions()
        
        r = requests.post(f"{self.config.api_base_url}/api/disk/info", 
            headers={
                "Authorization": f"Bearer {self.access_token}", 
                "Content-Type": "application/json"
            },
            data=json.dumps({"disk_data": disk_data, 
                "target": target, "report_id": self.report_id})
        )
        return True


    def fetch_memory_stats(self, target):
        mem_data = self.memory.mem_data()
        r = requests.post(f"{self.config.api_base_url}/api/memory/info", 
            headers={
                "Authorization": f"Bearer {self.access_token}", 
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "mem_data":  mem_data,
                "target": target, "report_id": self.report_id},
                    default=self._datetime_convertor)
        )
        return True

    def fetch_network_stats(self, target):
        netwk_data = self.network.net_data()
        ips = self.network.ip_address()

        r = requests.post(f"{self.config.api_base_url}/api/network/info", 
            headers={
                "Authorization": f"Bearer {self.access_token}", 
                "Content-Type": "application/json"
            },
            data=json.dumps({"network_data": netwk_data, "target": target, "report_id": self.report_id}, 
                default=self._datetime_convertor)
        )
        r = requests.post(f"{self.config.api_base_url}/api/network/ip", 
            headers={
                "Authorization": f"Bearer {self.access_token}", 
                "Content-Type": "application/json"
            },
            data=json.dumps({"ips": ips, "target": target, "report_id": self.report_id}, 
                default=self._datetime_convertor)
        )
        return True        

    def fetch_system_stats(self, target):
        opersys = self.system.operating_system()
        users = self.system.users()
        uptime = self.system.uptime()
        
        r = requests.post(f"{self.config.api_base_url}/api/system/os", 
            headers={
                "Authorization": f"Bearer {self.access_token}", 
                "Content-Type": "application/json"
            },
            data=json.dumps({"os": opersys, "target": target, "report_id": self.report_id}, 
                default=self._datetime_convertor)
        )

        r = requests.post(f"{self.config.api_base_url}/api/system/uptime", 
            headers={
                "Authorization": f"Bearer {self.access_token}", 
                "Content-Type": "application/json"
            },
            data=json.dumps({"uptime": uptime, "target": target, "report_id": self.report_id}, 
                default=self._datetime_convertor)
        )

        r = requests.post(f"{self.config.api_base_url}/api/system/users", 
            headers={
                "Authorization": f"Bearer {self.access_token}", 
                "Content-Type": "application/json"
            },
            data=json.dumps({"users": users, "target": target, "report_id": self.report_id},
                default=self._datetime_convertor)
        )
        return True


def main():
    sys_profiler = SystemProfiler()
    target_hostname = sys_profiler.network.hostname()
    sys_profiler.register_new_report(target=target_hostname)
    print(f"Running System Profiler Report on {target_hostname}. Using Report ID: {sys_profiler.report_id}.")
    
    sys_profiler.fetch_cpu_stats(target=target_hostname)
    sys_profiler.fetch_disk_stats(target=target_hostname)
    sys_profiler.fetch_memory_stats(target=target_hostname)
    sys_profiler.fetch_network_stats(target=target_hostname)
    sys_profiler.fetch_system_stats(target=target_hostname)

if __name__ == "__main__":
    main()
