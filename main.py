#!/usr/bin/env python3

from core.config import Config
from core.cpu import CPUInfo
from core.disk import DiskInfo
from core.memory import MemoryInfo
from core.network import NetworkInfo
from core.system import SystemInfo


class SystemProfiler(object):
    def __init__(self) -> None:
        self.config = Config()
        self.cpu = CPUInfo(self.config)
        self.disk = DiskInfo(self.config)
        self.memory = MemoryInfo(self.config)
        self.network = NetworkInfo(self.config)
        self.system = SystemInfo(self.config)       

    def fetch_cpu_stats(self, target):
        cpu_data = self.cpu.cpu_data()
        process_data = self.cpu.processes()
        results = {"cpu_data": cpu_data, "process_data": process_data, "target": target}

    def fetch_disk_stats(self, target):
        disk_data = self.disk.partitions() 
        results = {"disk_data": disk_data, "target": target}

    def fetch_memory_stats(self, target):
        mem_data = self.memory.mem_data()
        results = {"mem_data": mem_data, "target": target}

    def fetch_network_stats(self, target):
        netwk_data = self.network.net_data()
        hostname = self.network.hostname()
        ip = self.network.ip_address()
        results = {"network_data": netwk_data, "hostname": hostname, "ip_address": ip, "target": target}

    def fetch_system_stats(self, target):
        opersys = self.system.operating_system()
        users = self.system.users()
        uptime = self.system.uptime()
        results = {"operating_system": opersys, "users": users, "uptime": uptime, "target": target}


def main():
    sys_profiler = SystemProfiler()
    target_hostname = sys_profiler.network.hostname()

    sys_profiler.fetch_cpu_stats(target=target_hostname)
    sys_profiler.fetch_disk_stats(target=target_hostname)
    sys_profiler.fetch_memory_stats(target=target_hostname)
    sys_profiler.fetch_network_stats(target=target_hostname)
    sys_profiler.fetch_system_stats(target=target_hostname)

if __name__ == "__main__":
    main()
