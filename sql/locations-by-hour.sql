select l.name, substr(t."time", 0, 3) hour, count(*) n
from trip t
join location l on t.location = l.location
group by hour, l.name
order by hour, n desc;