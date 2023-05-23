#!/bin/bash

# Run the command passed as argument or start a shell
if [ $# -gt 0 ]; then
    exec "$@"
else
    echo 'Running...' && tail -f /dev/null
fi