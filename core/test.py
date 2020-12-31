from datetime import datetime
from typing import Dict, List, AnyStr
from config import ACC_MAIN, TOKEN, NEKIT_TOKEN
from database import insert
import tinvest
from pytz import timezone
from pprint import pprint


# client = tinvest.SyncClient(TOKEN)
client = tinvest.SyncClient(NEKIT_TOKEN)

user_api = tinvest.UserApi(client)
operations_api = tinvest.OperationsApi(client)
market_api = tinvest.MarketApi(client)

accounts = user_api.accounts_get().parse_json().payload.accounts
main_acc = accounts[0].broker_account_id
# main_iis = accounts[1].broker_account_id

valid_from = datetime.strptime('01.12.2016', '%d.%m.%Y')
valid_to = timezone('Europe/Moscow').localize(datetime.now())


operations = operations_api.operations_get(broker_account_id=main_acc, from_=valid_from, to=valid_to)\
    .parse_json().payload.operations

for operation in operations:
    data = {
        'id': operation.id,
        'oper_date': operation.date,
        'currency': operation.currency.value if operation.currency else None,
        'commission': operation.commission.value if operation.commission else None,
        'figi': operation.figi,
        'instrument_type': operation.instrument_type.value if operation.instrument_type else None,
        'is_margin_call': str(operation.is_margin_call),
        'operation_type': operation.operation_type.value if operation.operation_type else None,
        'payment': operation.payment,
        'price': operation.price,
        'quantity': operation.quantity,
        'quantity_executed': operation.quantity_executed,
        'status': operation.status.value,
        # 'trades': operation.trades.value,
    }
    # print(data)
    insert('operations', data)

stocks = market_api.market_stocks_get().parse_json().payload.instruments
for instrument in stocks:
    instrument_data = {
        'currency': instrument.currency.value,
        'figi': instrument.figi,
        'isin': instrument.isin,
        'lot': instrument.lot,
        'min_price_increment': instrument.min_price_increment,
        'name': instrument.name,
        'ticker': instrument.ticker,
        'type': instrument.type.value,
        'min_quantity': instrument.min_quantity
    }
    print(instrument_data)
    # insert('instruments', instrument_data)

etfs = market_api.market_etfs_get().parse_json().payload.instruments
for etf in etfs:
    etf_data = {
        'currency': etf.currency.value,
        'figi': etf.figi,
        'isin': etf.isin,
        'lot': etf.lot,
        'min_price_increment': etf.min_price_increment,
        'name': etf.name,
        'ticker': etf.ticker,
        'type': etf.type.value,
        'min_quantity': etf.min_quantity
    }
    print(etf_data)
    # insert('instruments', etf_data)


bonds = market_api.market_bonds_get().parse_json().payload.instruments
for bond in bonds:
    bond_data = {
        'currency': bond.currency.value,
        'figi': bond.figi,
        'isin': bond.isin,
        'lot': bond.lot,
        'min_price_increment': bond.min_price_increment,
        'name': bond.name,
        'ticker': bond.ticker,
        'type': bond.type.value,
        'min_quantity': bond.min_quantity
    }
    print(bond_data)
    # insert('instruments', bond_data)


portfolio_api = tinvest.PortfolioApi(client)
# print(dir(tinvest))
# print(dir(portfolio))

portfolio = portfolio_api.portfolio_get().parse_json().payload.positions
for item in portfolio:
    # print(item)
    item_data = {
        'name': item.name,
        'average_position_price': item.average_position_price.currency.value,
        'average_position_price_no_nkd': item.average_position_price_no_nkd,
        'balance': item.balance,
        'blocked': item.blocked,
        'expected_yield': item.expected_yield.currency.value,
        'figi': item.figi,
        'instrument_type': item.instrument_type.value,
        'isin': item.isin,
        'lots': item.lots,
        'ticker': item.ticker,
    }
    # print(item)
    print(item_data)
    # insert('portfolio', item_data)
