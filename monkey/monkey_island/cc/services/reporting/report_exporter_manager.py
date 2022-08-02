import logging

logger = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


class ReportExporterManager(object, metaclass=Singleton):
    def __init__(self):
        self._exporters_set = set()

    def get_exporters_list(self):
        return self._exporters_set

    def add_exporter_to_list(self, exporter):
        self._exporters_set.add(exporter)

    def export(self, report):
        for exporter in self._exporters_set:
            logger.debug(f"Trying to export using {repr(exporter)}")
            try:
                exporter().handle_report(report)
            except Exception as e:
                logger.exception(f"Failed to export report, error: {e}")
