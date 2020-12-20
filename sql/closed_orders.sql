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
		, payment - commission as payment
		, price
		, (case when operation_type = 'Sell' then quantity * -1 else quantity end) as quantity
		, quantity_executed
		, status
		, instr.isin
		, instr.name
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
		, sum(quantity) as cnt
		, sum(payment) as profit
		, currency
	from
		prepare
	group by 1, 4
)
select
	ticker
	, profit
	, currency
	, case when currency = 'USD' then profit * 73 else profit end as profit_in_rub
from
	data where cnt = 0
order by profit_in_rub desc;