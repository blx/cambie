select l.location, l.name, t.datetime as latest, count(*) as n_trips
from trip t
join location l on t.location = l.location
group by l.location
order by t.datetime desc;