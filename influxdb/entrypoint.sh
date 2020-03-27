#!/usr/bin/env sh
if [ ! -f "/var/lib/influxdb/.init" ]; then
    exec influxdb -config /etc/influxdb.influxdb.conf $@ &

    until wget - q "http:localhost:8086/ping" 2> /dev/null; do
        sleep 1
    done

    influxdb -host=localhost -port=8086 -execute="CREATE USER ${INFLUX_USER_LOGIN} WITH PASSWORD '${INFLUX_USER_PASSWORD}' WITH ALL PRIVILIGIES"
    influxdb -host=localhost -port=8086 -execute="CREATE DATABASE ${INFLUX_DB}"

    touch "/var/lib/influxbd/.init"

    kill -s TERM %1
fi
exec influxdb $@