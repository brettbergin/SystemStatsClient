#!/usr/bin/env python3

import datetime

import psutil


class CPUInfo(object):
    def __init__(self, config):
        self.config = config

    def cpu_data(self):
        """ """

        cpu_data = {}
        try:
            cpu_prct = psutil.cpu_percent(interval=1, percpu=True)

            cnt = 0
            for cpu in cpu_prct:
                cnt += 1
                cpu_data[f"CPU_{cnt}"] = f"{cpu.real}"

            return cpu_data

        except Exception as error:
            self.config.log.error(f"Failed cpu lookup. Error: {error}")
            return None

    def processes(self):
        """ """

        try:
            processes_found = []

            running_processes = [p for p in psutil.process_iter()]
            for proc in running_processes:
                try:
                    processes_found.append(
                        {
                            "name": proc.name(),
                            "pid": proc.pid,
                            "user": proc.username(),
                            "status": proc.status(),
                            "create_time": datetime.datetime.fromtimestamp(
                                proc.create_time()
                            ),
                            "cli": proc.cmdline(),
                            "executable": proc.exe(),
                            "cpu_percent": proc.cpu_percent(),
                            "mem_info": proc.memory_info(),
                            "open_files": [f._asdict() for f in proc.open_files()],
                            "connections": [c._asdict() for c in proc.connections()],
                            "threads": [t._asdict() for t in proc.threads()],
                        }
                    )
                except Exception as error:
                    processes_found.append(
                        {
                            "name": proc.name(),
                            "pid": proc.pid,
                            "user": proc.username(),
                            "status": proc.status(),
                            "create_time": datetime.datetime.fromtimestamp(
                                proc.create_time()
                            ),
                        }
                    )

            return processes_found

        except Exception as error:
            self.config.log.error(f"Failed process lookup. Error: {error}")
            return None
