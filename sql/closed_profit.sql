with temp as
(
	select
		oper_date
		, DATETIME(oper_date, 'localtime') as result_date
		, commission
		, oper.figi
		, oper.currency
		, instrument_type
		, operation_type
		, payment
		, (COALESCE(payment, 0) + COALESCE(commission, 0)) as value
		, price
--		, (case when operation_type = 'Sell' then quantity_executed * -1 else quantity_executed end) as quantity_executed
		, (case when operation_type = 'Sell' then -1 else 1 end * quantity_executed) as quantity_executed
		, sum(case when operation_type = 'Sell' then -1 else 1 end * quantity_executed) over(partition by name order by oper_date) as ex
		, sum(payment + commission) over(partition by name order by oper_date) as profit
		, instr.name
		, instr.ticker
	from
		operations oper
		left join instruments instr
		on oper.figi = instr.figi
	where
		1=1
--		and instr.ticker = 'QIWI'
--		or instr.ticker = 'CNK'
--		and instr.ticker = 'NVTK'
--		and instr.ticker = 'VTBR'
--		and instr.ticker = 'FIVE'
		and operation_type <> 'BrokerCommission'
		and operation_type <> 'PayIn'
		and operation_type <> 'PayOut'
		and operation_type <> 'ServiceCommission'
		and operation_type <> 'Dividend'
		and operation_type <> 'TaxDividend'
		and instrument_type <> 'Currency'
		and instrument_type <> 'Etf'
		and status = 'Done'
--	order by
--		name, oper_date desc
), data as
(
	select
		figi
		, ticker
		, name
	--	, operation_type
		, price
		, value
	--	, ex
	--	, quantity_executed
	--	, lead(profit) over(partition by name order by datex desc) as test
		, coalesce(profit - (lag(profit) over(partition by name order by result_date asc)), profit) as trade_profit -- 'Прибыль за сделку'
		, profit -- "Итоговая прибыль"
		, currency
		, result_date
	from temp
	where ex = 0
--	and result_date > '2020-12-10'
	order by name, result_date desc
)
select
	ticker
	, name
	, price
	, value
	, currency
	, case when currency == 'USD' then trade_profit * 74.5 else trade_profit end as 'Прибыль за сделку'
	, case when currency == 'USD' then profit * 74.5 else profit end as "Итоговая прибыль"
	, result_date
from data
--where result_date > '2020-12-10'
;
