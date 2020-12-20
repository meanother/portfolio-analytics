from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, Type, TypeVar
from urls import api

__all__ = ('BaseClient', )
T = TypeVar('T')


class BaseClient(ABC):
    def __init__(self, token: str, session: Optional[T] = None):
        if not token:
            raise ValueError('Token cant be empty!')
        self._base_url = api
        self._token: str = token
        self._session = session

    @property
    def session(self) -> T:
        if self._session:
            return self._session
        raise AttributeError

    @abstractmethod
    def request(self, method: str, path: str, **kwargs: Any) -> T:
        pass
