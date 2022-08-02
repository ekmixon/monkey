import logging
from typing import Sequence

from infection_monkey.system_info.system_info_collector import SystemInfoCollector
from infection_monkey.telemetry.system_info_telem import SystemInfoTelem

LOG = logging.getLogger(__name__)


class SystemInfoCollectorsHandler(object):
    def __init__(self):
        self.collectors_list = self.config_to_collectors_list()

    def execute_all_configured(self):
        successful_collections = 0
        system_info_telemetry = {}
        for collector in self.collectors_list:
            try:
                LOG.debug(f"Executing system info collector: '{collector.name}'")
                collected_info = collector.collect()
                system_info_telemetry[collector.name] = collected_info
                successful_collections += 1
            except Exception as e:
                # If we failed one collector, no need to stop execution. Log and continue.
                LOG.error(f"Collector {collector.name} failed. Error info: {e}")
        LOG.info(
            f"All system info collectors executed. Total {len(self.collectors_list)} executed, out of which {successful_collections} collected successfully."
        )


        SystemInfoTelem({"collectors": system_info_telemetry}).send()

    @staticmethod
    def config_to_collectors_list() -> Sequence[SystemInfoCollector]:
        return SystemInfoCollector.get_instances()
