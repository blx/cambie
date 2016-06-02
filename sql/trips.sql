select *
from compass
where "transaction" not like 'Missing %'
and "transaction" not like 'Loaded %'
order by datetime;