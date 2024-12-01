from abc import ABC, abstractmethod

class BetsInterface(ABC):
    @abstractmethod
    def find_element():
        """Find betting element."""
        pass

    @abstractmethod
    def get_clicks_multiplier(number_of_losses):
        """Get clicks multiplier."""
        pass