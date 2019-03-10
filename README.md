# ogn-python

[![Build Status](https://travis-ci.org/glidernet/ogn-python.svg?branch=master)](https://travis-ci.org/glidernet/ogn-python)
[![Coverage Status](https://img.shields.io/coveralls/glidernet/ogn-python.svg)](https://coveralls.io/r/glidernet/ogn-python)

A database backend for the [Open Glider Network](http://wiki.glidernet.org/).
The ogn-python module saves all received beacons into a database with [SQLAlchemy](http://www.sqlalchemy.org/).
It connects to the OGN aprs servers with [python-ogn-client](https://github.com/glidernet/python-ogn-client).
It requires [PostgreSQL](http://www.postgresql.org/) and [PostGIS](http://www.postgis.net/).
For best performance you should use [TimescaleDB](https://www.timescale.com), which is based on PostgreSQL.

[Examples](https://github.com/glidernet/ogn-python/wiki/Examples)


## Installation and Setup
1. Checkout the repository

    ```
    git clone https://github.com/glidernet/ogn-python.git
    ```

2. Install python requirements

    ```
    pip install -r requirements.txt
    ```

3. Install [PostgreSQL](http://www.postgresql.org/) with [PostGIS](http://www.postgis.net/) Extension.
    Create a database (use "ogn" as default, otherwise you have to modify the configuration, see below)

4.  Optional: Install redis for asynchronous tasks (like takeoff/landing-detection)

    ```
    apt-get install redis-server
    ```

5. Create database

    ```
    ./flask database init
    ```

6. Optional: Prepare tables for TimescaleDB

    ```
    ./flask database init_timescaledb
    ```

7. Optional: Import world border dataset (needed if you want to know the country a receiver belongs to, etc.)
    Get the [World Borders Dataset](http://thematicmapping.org/downloads/world_borders.php) and unpack it.
    Then import it into your database (we use "ogn" as database name).
    
    ```
    shp2pgsql -s 4326 TM_WORLD_BORDERS-0.3.shp world_borders_temp | psql -d ogn
    psql -d ogn -c "INSERT INTO countries SELECT * FROM world_borders_temp;"
    psql -d ogn -c "DROP TABLE world_borders_temp;"
    ```
    
8. Optional: Import world elevation data (needed for AGL calculation)
    For Europe we can get the DEM as GeoTIFF files from the
    [European Environment Agency](https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1).
    Because the spatial reference system (SRID) of these files is 3035 and we want 4326 we have to convert them:
    
    ```
    gdalwarp -s_srs "EPSG:3035" -t_srs "EPSG:4326" source.tif target.tif
    ```
    
    Then we can import the GeoTIFF into the elevation table:
    
    ```
    raster2pgsql -c -C -I -M -t 100x100 elevation_data.tif public.elevation | psql -d ogn
    ```
    
There is also a [Vagrant](https://www.vagrantup.com/) environment for the development of ogn-python.
You can create and start this virtual machine with `vagrant up` and login with `vagrant ssh`.
The code of ogn-python will be available in the shared folder `/vagrant`.

## Usage
### Running the aprs client and task server
To schedule tasks like takeoff/landing-detection (`logbook.compute`),
[Celery](http://www.celeryproject.org/) with [Redis](http://www.redis.io/) is used.
The following scripts run in the foreground and should be deamonized
(eg. use [supervisord](http://supervisord.org/)).

- Start the aprs client

  ```
  ./flask gateway run
  ```

- Start a task server (make sure redis is up and running)

  ```
  celery -A ogn_python.collect worker -l info
  ```

- Start the task scheduler (make sure a task server is up and running)

  ```
  celery -A ogn_python.collect beat -l info
  ```


To load a custom configuration, create a file `myconfig.py` (see [config/default.py](config/default.py))
and set the environment variable `OGN_CONFIG_MODULE` accordingly.

```
touch myconfig.py
export OGN_CONFIG_MODULE="myconfig"
./flask gateway run
```

### Flask - Command Line Interface
```
Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  Provides commands from Flask, extensions, and the application. Loads the
  application defined in the FLASK_APP environment variable, or from a
  wsgi.py file. Setting the FLASK_ENV environment variable to 'development'
  will enable debug mode.

    $ export FLASK_APP=app.py
    $ export FLASK_ENV=development
    $ flask run

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  database  Database creation and handling.
  db        Perform database migrations.
  export    Export data in several file formats.
  flights   Create 2D flight paths from data.
  gateway   Connection to APRS servers.
  logbook   Handling of logbook data.
  routes    Show the routes for the app.
  run       Runs a development server.
  shell     Runs a shell in the app context.
  stats     Handling of statistical data.
```

Most commands are command groups, so if you execute this command you will get further (sub)commands.

### Available tasks (deprecated - needs rework)

- `ogn.collect.database.import_ddb` - Import registered devices from the DDB.
- `ogn.collect.database.import_file` - Import registered devices from a local file.
- `ogn.collect.database.update_country_code` - Update country code in receivers table if None.
- `ogn.collect.database.update_devices` - Add/update entries in devices table and update foreign keys in aircraft beacons.
- `ogn.collect.database.update_receivers` - Add/update_receivers entries in receiver table and update receivers foreign keys and distance in aircraft beacons and update foreign keys in receiver beacons.
- `ogn.collect.logbook.update_logbook` - Add/update logbook entries.
- `ogn.collect.logbook.update_max_altitude` - Add max altitudes in logbook when flight is complete (takeoff and landing).
- `ogn.collect.stats.update_device_stats` - Add/update entries in device stats table.
- `ogn.collect.stats.update_receiver_stats` - Add/update entries in receiver stats table.
- `ogn.collect.takeoff_landing.update_takeoff_landing` - Compute takeoffs and landings.

If the task server is up and running, tasks could be started manually.

```
python3
>>>from ogn.collect.database import import_ddb
>>>import_ddb.delay()
```

## License
Licensed under the [AGPLv3](LICENSE).
