import logging
import os
import re
import subprocess
import sys

import infection_monkey.config
from infection_monkey.network.HostFinger import HostFinger
from infection_monkey.network.HostScanner import HostScanner

PING_COUNT_FLAG = "-n" if sys.platform == "win32" else "-c"
PING_TIMEOUT_FLAG = "-w" if sys.platform == "win32" else "-W"
TTL_REGEX_STR = r"(?<=TTL\=)[0-9]+"
LINUX_TTL = 64
WINDOWS_TTL = 128

LOG = logging.getLogger(__name__)


class PingScanner(HostScanner, HostFinger):
    _SCANNED_SERVICE = ""

    def __init__(self):
        self._timeout = infection_monkey.config.WormConfiguration.ping_scan_timeout
        if sys.platform != "win32":
            self._timeout /= 1000

        self._devnull = open(os.devnull, "w")
        self._ttl_regex = re.compile(TTL_REGEX_STR, re.IGNORECASE)

    def is_host_alive(self, host):
        ping_cmd = self._build_ping_command(host.ip_addr)
        LOG.debug(f"Running ping command: {' '.join(ping_cmd)}")

        return (
            subprocess.call(
                ping_cmd,
                stdout=self._devnull,
                stderr=self._devnull,
            )
            == 0
        )

    def get_host_fingerprint(self, host):
        ping_cmd = self._build_ping_command(host.ip_addr)
        LOG.debug(f"Running ping command: {' '.join(ping_cmd)}")

        # If stdout is not connected to a terminal (i.e. redirected to a pipe or file), the result
        # of os.device_encoding(1) will be None. Setting errors="backslashreplace" prevents a crash
        # in this case. See #1175 and #1403 for more information.
        encoding = os.device_encoding(1)
        sub_proc = subprocess.Popen(
            ping_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding=encoding,
            errors="backslashreplace",
        )

        LOG.debug(f"Retrieving ping command output using {encoding} encoding")
        output = " ".join(sub_proc.communicate())
        if regex_result := self._ttl_regex.search(output):
            try:
                ttl = int(regex_result.group(0))
                host.os["type"] = "linux" if ttl <= LINUX_TTL else "windows"
                host.icmp = True

                return True
            except Exception as exc:
                LOG.debug("Error parsing ping fingerprint: %s", exc)

        return False

    def _build_ping_command(self, ip_addr):
        return ["ping", PING_COUNT_FLAG, "1", PING_TIMEOUT_FLAG, str(self._timeout), ip_addr]
