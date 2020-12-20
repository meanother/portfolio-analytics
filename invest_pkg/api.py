from abc import ABC
from typing import Any, Generic, Optional, TypeVar, Dict, List
from datetime import datetime, timezone
from pytz import timezone as tz
from base_client import BaseClient
from simple_client import TOKEN, SyncClient
from pydantic import BaseModel, Field
from enum import Enum

class Currency(str, Enum):
    rub = 'RUB'
    usd = 'USD'
    eur = 'EUR'
    gbp = 'GBP'
    hkd = 'HKD'
    chf = 'CHF'
    jpy = 'JPY'
    cny = 'CNY'
    try_ = 'TRY'

class MoneyAmount(BaseModel):
    """MoneyAmount"""

    currency: Currency
    value: float

class InstrumentType(str, Enum):
    stock = 'Stock'
    currency = 'Currency'
    bond = 'Bond'
    etf = 'Etf'


class OperationTypeWithCommission(str, Enum):
    buy = 'Buy'
    buy_card = 'BuyCard'
    sell = 'Sell'
    broker_commission = 'BrokerCommission'
    exchange_commission = 'ExchangeCommission'
    service_commission = 'ServiceCommission'
    margin_commission = 'MarginCommission'
    other_commission = 'OtherCommission'
    pay_in = 'PayIn'
    pay_out = 'PayOut'
    tax = 'Tax'
    tax_lucre = 'TaxLucre'
    tax_dividend = 'TaxDividend'
    tax_coupon = 'TaxCoupon'
    tax_back = 'TaxBack'
    repayment = 'Repayment'
    part_repayment = 'PartRepayment'
    coupon = 'Coupon'
    dividend = 'Dividend'
    security_in = 'SecurityIn'
    security_out = 'SecurityOut'


class OperationStatus(str, Enum):
    done = 'Done'
    decline = 'Decline'
    progress = 'Progress'

class OperationTrade(BaseModel):
    date: datetime
    price: float
    quantity: int
    trade_id: str = Field(alias='tradeId')


class Operation(BaseModel):
    commission: Optional[MoneyAmount]
    # commission: Optional[Any]
    currency: Currency
    date: datetime
    figi: Optional[str]
    id: str
    # instrument_type: Optional[InstrumentType] = Field(alias='instrumentType')
    instrument_type: Optional[Any]
    is_margin_call: bool = Field(alias='isMarginCall')
    operation_type: Optional[OperationTypeWithCommission] = Field(alias='operationType')
    payment: float
    price: Optional[float]
    quantity: Optional[int]
    quantity_executed: Optional[int] = Field(alias='quantityExecuted')
    status: OperationStatus
    trades: Optional[List[OperationTrade]]



class Operations(BaseModel):
    operations: List[Operation]


class OperationsResponse(BaseModel):
    payload: Operations
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


T = TypeVar('T', bound=BaseClient)

valid_from = datetime.strptime('01.12.2016', '%d.%m.%Y')
valid_to = tz('Europe/Moscow').localize(datetime.now())


class BaseApi(ABC, Generic[T]):
    def __init__(self, client: T) -> None:
        self._client = client

    @property
    def client(self) -> T:
        return self._client


class OperationsApi(BaseApi[T]):

    def operations_get(self, from_, to, figi: Optional[str] = None, **kwargs: Dict) -> Any:
        print(kwargs)
        kwargs.setdefault('params', {})
        print(kwargs)
        params = kwargs['params']
        params.setdefault('from', from_)
        params.setdefault('to', to)
        return self.client.request(
            'GET', '/operations', response_model=OperationsResponse, **kwargs
        )

client = SyncClient(TOKEN)
print(client.session)
# data = client.request('GET', '/operations')
# print(data.json())

api = OperationsApi(client)
print(api)
print(api.client)
data = api.operations_get(from_=valid_from.replace(tzinfo=timezone.utc).isoformat(), to=valid_to.replace(tzinfo=timezone.utc).isoformat())
qwe = data.parse_json().payload.operations
for j in qwe:
    print(j.commission and j.commission.value)


#
# print(valid_from)
# print(valid_from.isoformat())
# print(valid_from.replace(tzinfo=timezone.utc).isoformat())
# print(valid_to.replace(tzinfo=timezone.utc).isoformat())


