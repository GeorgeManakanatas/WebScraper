@echo off

rem calling the function with the proper parameters
CALL :postgres_container_command_line scraperpostgresql , postgres , scrapedbpass , autoscrapedb , 5454 , 5432

rem function for starting the containers
EXIT /B %ERRORLEVEL%
:postgres_container_command_line
rem stop existing container
docker container stop %~1
rem remove container
docker container rm %~1
rem run container
docker run  --name %~1 -e POSTGRESQL_USER=%~2 -e POSTGRESQL_PASSWORD=%~3 -e POSTGRESQL_DATABASE=%~4 -p %~5:%~6 --restart=always -d centos/postgresql-96-centos7
EXIT /B 0