#!/bin/bash

NREPEATS=3

for ((i=0; i<$NREPEATS; i++)); do
    echo "Iteration $i"
    /usr/bin/time ntmirror-dbload --testmode --reset \
      myuser mypass ntmirror_test /run/mysqld/mysqld.sock ntdumpdir
done

