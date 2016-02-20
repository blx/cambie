# cambie

Tools to load Compass Card usage history into SQLite.

    $ python -m cambie load_trips data/
    Ingesting trip history from data/Compass Card History - 0164.. - Dec-01-2015 to Dec-21-2015.csv
    Ingesting trip history from data/Compass Card History - 0164.. - Oct-15-2015 to Dec-01-2015.csv
    ...

    $ python -m cambie geocode_stops
    Geocoded 58501 (WB W BROADWAY FS CAMBIE ST) to 49.263340, -123.115720
    Geocoded 50852 (WB W HASTINGS ST FS RICHARDS ST) to 49.284470, -123.112450
    ...

    $ python -m cambie plot_trips_by_hour
    (histogram shown)
