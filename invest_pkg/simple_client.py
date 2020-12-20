from typing import Any, Generic, Optional, Type, TypeVar
from requests import Response, Session
from pydantic import BaseModel
from base_client import BaseClient
from utils import set_default_headers
# T = TypeVar('T')

TOKEN = ''

T = TypeVar('T', bound=BaseModel)  # pragma: no mutate


class ResponseWrapper(Generic[T]):

    S = TypeVar('S', bound=BaseModel)

    def __init__(self, response: Response, response_model: Type[T]):
        self._response = response
        self._response_model = response_model

    def __getattr__(self, name):
        return getattr(self._response, name)

    def parse_json(self, **kwargs: Any) -> T:
        return self._parse_json(self._response_model, **kwargs)

    def _parse_json(self, response_model: Type[S], **kwargs: Any):
        return response_model.parse_obj(self._response.json(**kwargs))


class SyncClient(BaseClient):

    def __init__(self, token: str, *, session: Optional[Session] = None):
        super().__init__(token, session=session)
        if not session:
            self._session = Session()

    def request(self, method: str, path: str, response_model: Type[T], **kwargs: Any) -> ResponseWrapper[T]:
        url = self._base_url + path
        set_default_headers(kwargs, self._token)
        print(kwargs)
        response = ResponseWrapper[T](self.session.request(method, url, **kwargs), response_model)
        return response



