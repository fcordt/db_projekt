#!/bin/sh

x=1

while [ $x -ne 0 ]
do
    sqlplus system/$1@//127.0.0.1:1521/$2 @./scripts/create_user.sql $3 $4
    x=$?
    echo $x
    sleep 1
done