select substr(datetime, 0, 11) day, count(*) tap_count
from trip
where "transaction" not like 'Missing %'
and "transaction" not like 'Loaded %'
group by day
order by datetime desc;