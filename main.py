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

    def _datetime_convertor(self, date_obj):
        if isinstance(date_obj, (datetime.datetime, timedelta)):
            return date_obj.__str__()

    def _stringify_req_body(self, req_body):
        if not isinstance(req_body, dict):
            self.config.log.debug(f"[!] Request body is not a dict() object. Cannot stringify.")
            return None
        
        return json.dumps(req_body, default=self._datetime_convertor)
    
    def _send_api_request(self, uri_path=None, data_payload=None):
    
        if uri_path == None or data_payload == None:
            return False

        self.config.log.debug(f"[!] Using URI PATH: {uri_path}")
        req_url = f"{self.config.api_base_url}{uri_path}"
        self.config.log.debug(f"[!] Using URL: {req_url}")

        if self.access_token == None:
            self.config.log.debug(f"[!] No API access token available to make API requests.")
            return

        r = requests.post(
            url=req_url, 
            headers={
                "Authorization": f"Bearer {self.access_token}", 
                "Content-Type": "application/json"
            },
            data=data_payload
        )

        self.config.log.debug(f"[!] Received Response Code: {r.status_code}")
        if r.status_code not in (200, 201, 202, 204):
            return False

        resp_json = r.json()
        return resp_json

    def register_new_report(self, target, api_path):
        request_data = self._stringify_req_body(req_body={"target": f"{target}"})
        api_response = self._send_api_request(uri_path=api_path, data_payload=request_data)

        self.report_id = api_response["report_id"]
        return self.report_id

    def fetch_cpu_stats(self, target, api_path):
        cpu_data = self.cpu.cpu_data()
        
        request_data = self._stringify_req_body(req_body={
            "cpu_data": cpu_data, "target": target,
            "report_id": self.report_id})

        self._send_api_request(uri_path=api_path, data_payload=request_data)

    def fetch_process_stats(self, target, api_path):
        processes = self.cpu.processes()
        
        request_data = self._stringify_req_body(req_body={
            "process_data": processes, "target": target, 
            "report_id": self.report_id})

        self._send_api_request(uri_path=api_path, data_payload=request_data)

    def fetch_disk_stats(self, target, api_path):
        disk_data = self.disk.partitions()
        
        request_data = self._stringify_req_body(req_body={
            "disk_data": disk_data, "target": target, 
            "report_id": self.report_id})

        self._send_api_request(uri_path=api_path, data_payload=request_data)

    def fetch_memory_stats(self, target, api_path):
        mem_data = self.memory.mem_data()

        request_data = self._stringify_req_body(req_body={
            "mem_data":  mem_data, "target": target, 
            "report_id": self.report_id})

        self._send_api_request(uri_path=api_path, data_payload=request_data)

    def fetch_network_stats(self, target, network_info_api_path, network_ip_api_path):
        netwk_data = self.network.net_data()
        ips = self.network.ip_address()

        network_data = self._stringify_req_body(req_body={
            "network_data": netwk_data, "target": target,
            "report_id": self.report_id})
    
        ip_data = self._stringify_req_body(req_body={
            "ips": ips, "target": target, "report_id": self.report_id})

        self._send_api_request(uri_path=network_info_api_path, data_payload=network_data)
        self._send_api_request(uri_path=network_ip_api_path, data_payload=ip_data)      

    def fetch_system_stats(self, target, os_api_path, uptime_api_path, users_api_path):
        opersys = self.system.operating_system()
        users = self.system.users()
        uptime = self.system.uptime()

        os_req_data = self._stringify_req_body(req_body={
            "os": opersys, "target": target, "report_id": self.report_id})

        uptime_req_data = self._stringify_req_body(req_body={
            "uptime": uptime, "target": target, "report_id": self.report_id})

        users_req_data = self._stringify_req_body(req_body={
            "users": users, "target": target, "report_id": self.report_id})

        self._send_api_request(uri_path=os_api_path, data_payload=os_req_data)
        self._send_api_request(uri_path=uptime_api_path, data_payload=uptime_req_data)
        self._send_api_request(uri_path=users_api_path, data_payload=users_req_data)


def main():
    sys_profiler = SystemProfiler()
    target_hostname = sys_profiler.network.hostname()
    sys_profiler.register_new_report(target=target_hostname, 
        api_path="/api/report/new")

    print(f"Running System Profiler Report on {target_hostname}. Using Report ID: {sys_profiler.report_id}.")

    sys_profiler.fetch_cpu_stats(target=target_hostname, 
        api_path="/api/cpu/info")

    sys_profiler.fetch_disk_stats(target=target_hostname, 
        api_path="/api/disk/info")
    
    sys_profiler.fetch_memory_stats(target=target_hostname, 
        api_path="/api/memory/info")
    
    sys_profiler.fetch_network_stats(target=target_hostname, 
        network_info_api_path="/api/network/info", network_ip_api_path="/api/network/ip")
    
    sys_profiler.fetch_system_stats(
        target=target_hostname, os_api_path="/api/system/os", 
        users_api_path="/api/system/users", uptime_api_path="/api/system/uptime")

    sys_profiler.fetch_process_stats(target=target_hostname, 
        api_path="/api/cpu/processes")


if __name__ == "__main__":
    main()
