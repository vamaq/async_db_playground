#!/usr/bin/env bash

print_help () {
    echo "Parameter error:"
    echo "      $filename <ACTION> <USERNAME> <DB_HOST> <PORT> <DB_NAME>"
    echo "      ACTION: C = Create / D = Delete / U = Update"
    echo "      i.e: $filename C/D/U twdb localhost 5432 twdb"
}

filename=$(basename "${BASH_SOURCE[0]}")
basedir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ -z "${1}" ] || [ -z "${2}" ] || [ -z "${3}" ] || [ -z "${4}" ] || [ -z "${5}" ]; then
    print_help
    exit
fi

echo "Accessing $basedir"
cd $basedir

if [ "${1}" == "C" ]; then
    psql -U ${2} -h ${3} -p ${4} ${5} -f create_model.sql
elif [ "${1}" == "D" ]; then
    psql -U ${2} -h ${3} -p ${4} ${5} -f delete_model.sql
elif [ "${1}" == "U" ]; then
    cat delete_model.sql create_model.sql | psql -U ${2} -h ${3} -p ${4} ${5} -f -
fi
