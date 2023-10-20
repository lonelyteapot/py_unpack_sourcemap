import logging

logger = logging.getLogger("py_unpack_sourcemap")


class _LogFormatter(logging.Formatter):
    def format(self, record) -> str:
        return self._prefix(record) + super().format(record)

    @staticmethod
    def _prefix(record: logging.LogRecord) -> str:
        if record.levelno == logging.CRITICAL:
            return "[!] "
        if record.levelno == logging.ERROR:
            return "[!] "
        if record.levelno == logging.WARNING:
            return "[!] "
        if record.levelno == logging.INFO:
            return "[+] "
        if record.levelno == logging.DEBUG:
            return "[D] "
        return ""


def configure_logging_for_cli():
    formatter = _LogFormatter("%(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
