from abc import ABC, abstractmethod
from typing import Any


class ServiceManagerInterface(ABC):

    @abstractmethod
    def subscribe(self, observer: Any) -> None:
        pass

    @abstractmethod
    def notify_location_auto_complete(self, data):
        pass

    @abstractmethod
    def notify_total_volunteers(self, data):
        pass

    @abstractmethod
    def get_location_data(self, location):
        pass

    @abstractmethod
    def unsubscribe(self, observer: Any) -> None:
        pass
