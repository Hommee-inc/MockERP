from abc import ABC, abstractmethod


class NameProvider(ABC):

    @abstractmethod
    def name(self):
        pass


class EmailProvider(ABC):

    @abstractmethod
    def email(self):
        pass


class AddressProvider(ABC):

    @abstractmethod
    def address(self):
        pass


class PhoneProvider(ABC):

    @abstractmethod
    def phone(self):
        pass


class DocumentProvider(ABC):

    @abstractmethod
    def document(self, document_type):
        pass