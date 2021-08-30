#!/bin/bash
################
# general info #
################

# reset postgres for development

########################
# supporting functions #
########################
notification(){
  # will display a notification with given text
  zenity --notification --window-icon="info" --text="$1" --timeout=2
}
reset_postgresql(){
  # postgresql variables
  postgresContainerName="scraperpostgresql"
  postgresName="autoscrapedb"
  postgresUserName="postgres"
  postgresPassword="scrapedbpass"
  postgresEnvironmentPort="5454"
  postgresContainerPort="5432"
  # stop remove and make new container
  docker container stop $postgresContainerName ;
  docker container rm $postgresContainerName ;

  docker run  --name $postgresContainerName \
              -e POSTGRESQL_USER=$postgresUserName \
              -e POSTGRESQL_PASSWORD=$postgresPassword \
              -e POSTGRESQL_DATABASE=$postgresName \
              -p $postgresEnvironmentPort:$postgresContainerPort \
              --restart=always \
              -d centos/postgresql-96-centos7 ;
  # wait for container to start
  sleep 10 ;
  docker ps -a ;
  docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' scraperpostgresql;
  ifconfig ;
}
export_postgresql(){
  docker exec -t scraperpostgresql pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
}
import_dump_to_postgresql(){
  dump=$(zenity --entry --title="Dump file" --text="Dump file name" );
  cat $dump | docker exec -i your-db-container psql -U postgres
}
start_container(){
 # popup for user to give the name of the container to be started and starts it
 container=$(zenity --entry --title="Start Container" --text="Container to start" );
 docker container start $container
}
stop_container(){
  # popup for user to give the name of the container to be stoped and stops it
  container=$(zenity --entry --title="Stop Container" --text="Container to stop" );
  docker container stop $container
}
remove_container(){
  # popup for the user to give the name of the container to be removed
  container=$(zenity --entry --title="Remove Container" --text="Container to remove" );
  # and then proceeds to stop the container and remove it
  docker container stop $container
  docker container rm $container
}
remove_image(){
  # popup for the user to give the name of the image to be removed
  image=$(zenity --entry --title="Remove Image" --text="Image to remove" );
  # and then proceeds to remove iamge
  docker image rm $image
}

#################
# main function #
#################

start_menu(){
  #zenity configuration
  title="General script"
  prompt="Please select action"
  windowHeight=500
  #
  response=$(zenity --height="$windowHeight" --list --checklist \
    --title="$title" --column="" --column="Options" \
    False "Reset scraping DB" \
    False "Export scraping DB" \
    False "Import dump to scraping DB" \
    False "Show containers" \
    False "Start container" \
    False "Stop container" \
    False "Remove Container" \
    False "Show Images" \
    False "Remove Image" --separator=':');

  # check for no selection
  if [ -z "$response" ] ; then
     echo "No selection"
     exit 1
  fi

  IFS=":" ; for word in $response ; do
     case $word in
        "Reset scraping DB")
          reset_postgresql
          notification "PostgreSQL reset" ;;
        "Export scraping DB")
          export_postgresql
          notification "PostgreSQL exported" ;;
        "Import dump to scraping DB")
          import_dump_to_postgresql
          notification "PostgreSQL imported" ;;
        "Stop container")
        	stop_container
        	notification "Container stoped" ;;
      	"Start container")
        	start_container
        	notification "Container started" ;;
        "Show containers")
          docker ps -a ;;
        "Remove Container" )
          remove_container
          notification "Container removed" ;;
        "Show Images")
          docker images ;;
        "Remove Image")
        	remove_image
          notification "Image removed" ;;
     esac
  done
}

# loop ensuring that main window function restarts once task is finished
while true; do
  start_menu
done