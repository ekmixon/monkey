import logging

from monkey_island.cc.models.monkey import Monkey

logger = logging.getLogger(__name__)


def process_environment_telemetry(collector_results, monkey_guid):
    relevant_monkey = Monkey.get_single_monkey_by_guid(monkey_guid)
    relevant_monkey.environment = collector_results["environment"]
    relevant_monkey.save()
    logger.debug(
        f"Updated Monkey {str(relevant_monkey)} with env {collector_results}"
    )
