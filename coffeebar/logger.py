import logging


class SafeLogger(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        if not SafeLogger.instance is None:
            SafeLogger.instance = logging.getLogger(__name__)
        return SafeLogger.instance

    def __getattr__(self, item):
        return getattr(self.instance, item)
