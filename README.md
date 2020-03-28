# Project for a Load testing

## Structure
**Python/Locust** *:tcp (socket) -> tcp:* **InfluxDB** *:http <- http:* **Grafana**

[Locust](https://docs.locust.io/en/stable) - load testing framework written in Python. Based on libs: requests, gevent/evenlet  

[InfluxDB](https://docs.influxdata.com/influxdb/v1.7/introduction/getting-started) - Time-series database. In this case it uses graphite protocol. 

[Grafana](https://grafana.com/docs/grafana/latest/features/datasources/influxdb/) - dashboard system to visualize metrics  

---

## Deployment
`docker-compose build` - to build docker containers  
`docker-compose up` - to launch containers  

By default container with tests executes `ENTRYPOINT ["tail", "-f", "/dev/null"]` command. [More.](https://unix.stackexchange.com/questions/230887/what-does-dev-null-mean/230888)  

Create bash-session to container with tests:  
`docker-compose exec tests bash`  

Then use Locust CLI to execute tests with required parameters.  
Example:  
Пример:  
`locust -f TEST_FILE_NAME.py --no-web -c 1000 -r 100 -t 5m --only-summary`  
`-f` - path to test file  
`--no-web` - start without default web interface (we are using Grafana dashboard for data visualization)  
`-c` - specifies the number of Locust users to spawn  
`-r` - the hatch rate (number of users to spawn per second)  
`-t` - specify the run time. Supported units: `h, min, sec`  
`--only-summary` - show only the final results  

---

For a connection to InfluxDB database use the following command:  
`docker-compose exec influxdb influx`  

[Influx Query Language.](https://docs.influxdata.com/influxdb/v1.7/query_language/) Examples:  

    SHOW databases
    USE graphite  
    SHOW series  
    SELECT * FROM "performance./login"  
    SELECT * FROM "performance./login" LIMIT 5
    select * from "mem" limit 5

---

## Notes  
Project consists of 3 parts:

### Grafana

Local dashboard server:  
По адресу:  http://127.0.0.1:3000  
username: `admin`  
password: `admin`


### InfluxDB
Configs can be found in  `influxdb/influxdb.config`  

For a DB connection we are using `graphite` protocol. [See.](https://docs.influxdata.com/influxdb/v1.7/supported_protocols/graphite/)


Data recording format:  
`<metric path> <metric value> <metric timestamp>`
```
sensu.metric.net.server0.eth0.rx_packets 461295119435 1444234982
sensu.metric.net.server0.eth0.tx_bytes 1093086493388480 1444234982
sensu.metric.net.server0.eth0.rx_bytes 1015633926034834 1444234982
sensu.metric.net.server0.eth0.tx_errors 0 1444234982
```

### Locust/Python


```python
# <metric path> <metric value> <metric timestamp>
string = '%s %d %d\n' % (name, response_time, time.time())
sock.send(string.encode('utf-8'))
```
