# cambie

Tools to load Compass Card usage history into SQLite.

    $ python -m cambie load_trips data/*.csv
    Ingesting trip history from data/Compass Card History - 0164.. - Dec-01-2015 to Dec-21-2015.csv
    Ingesting trip history from data/Compass Card History - 0164.. - Oct-15-2015 to Dec-01-2015.csv
    ...

    $ python -m cambie geocode_stops
    Geocoded 58501 (WB W BROADWAY FS CAMBIE ST) to 49.263340, -123.115720
    Geocoded 50852 (WB W HASTINGS ST FS RICHARDS ST) to 49.284470, -123.112450
    ...

    $ python -m cambie plot_trips_by_hour
    (histogram shown)

## Setup

To specify the SQLite file, create an `env.json`:

```json
{
    "db": "compass.sqlite3"
}
```

## License (ISC)

Copyright (c) 2016 Ben Cook.

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
