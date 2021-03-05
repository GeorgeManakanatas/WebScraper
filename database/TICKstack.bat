@ECHO OFF

:: This batch file pulls images and starts containers for a coplete TICK stack
FOR /F "tokens=*" %%g IN ('docker --version') do (SET value=%%g)
ECHO docker version is: %value%
ECHO.
ECHO "Available images are:"
docker image ls -a
ECHO.
ECHO "Pull the tick stack images?"
CHOICE /C YN /M "Yes or No" 
IF %ERRORLEVEL% EQU 1 (
        ECHO "Pulling the TICK stack"
    docker pull influxdb
    docker pull kapacitor
    docker pull telegraf
    docker pull chronograf
)
IF %ERRORLEVEL% EQU 2 (
    ECHO "Not pulling the TICK stack"
)

SET container_list=influxdb kapacitor telegraf chronograf

ECHO "Reset the TICK stack containers?"
CHOICE /C YN /M "Yes or No" 
IF %ERRORLEVEL% EQU 1 (
    ECHO "Resetting TICK stack containers"
    FOR %%V in (%container_list%) do (
        docker container stop %%V
        ECHO stopping %%V
        docker container rm %%V
        ECHO removing %%V
        if %%V EQU influxdb (
            ECHO "InfluxDB with default options, 8086 port and influxdb name"
            docker run --name influxdb --detach -p 8086:8086 influxdb
        )
        if %%V EQU kapacitor (
            ECHO "Kapacitor with default options, 9092 port and kapacitor name"
            docker run --name kapacitor --detach -p 9092:9092 kapacitor
        )
        if %%V EQU telegraf (
            ECHO "telegraf not setup"
        )
        if %%V EQU chronograf (
            ECHO "Chronograf with default options, 8888 port and chronograf name"
            docker run --name chronograf --detach -p 8888:8888 chronograf
        )
    )
)
IF %ERRORLEVEL% EQU 2 (
    ECHO "Not resetting TICK stack containers"
)
docker container ls -a
