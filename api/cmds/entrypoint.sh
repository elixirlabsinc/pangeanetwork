#!/bin/bash

cd /opt/api

# The entrypoint for the Postscript Homework API
./cmds/wait-for-it.sh db:5432 -s -- printf "Database Successfully Started\n"

# Execute main run command
exec "$@"
exit