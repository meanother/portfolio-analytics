with prepare as
(
	select
		oper.id
		, oper_date
		, oper.currency
		, commission
		, oper.figi
		, instrument_type
		, operation_type
		, payment + commission as payment
		, price
		, (case when operation_type = 'Sell' then quantity * -1 else quantity end) as quantity
		, (case when operation_type = 'Sell' then quantity_executed * -1 else quantity_executed end) as quantity_executed
		, status
		, instr.isin
		, instr.name as name
		, (case when instr.ticker is null then instrument_type else instr.ticker end) as ticker
	from
		operations oper
		left join instruments instr
		on oper.figi = instr.figi
	where
		1=1
		--and instr.ticker = 'QIWI'
		and operation_type <> 'BrokerCommission'
		and status = 'Done'
	order by
		oper_date desc
),
data as
(
	select
		ticker
		, name
		, sum(quantity_executed) as cnt
		, sum(payment) as profit
		, currency
	from
		prepare
	group by ticker, name, currency
)
select
	ticker
	, name
	, profit
	, currency
	, case when currency = 'USD' then profit * 73 else profit end as profit_in_rub
from
	data where cnt = 0
order by profit_in_rub desc;