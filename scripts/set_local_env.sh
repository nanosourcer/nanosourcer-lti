#!/usr/bin/env bash

while read i; do
    k=$(echo $i | cut -f1 -d:)
    v=$(echo $i | cut -f2- -d:| sed -e 's/^[ \t"]*//' |sed -e 's/"//g')
    echo $k=$v
    export $k=$v
done < ~/secure_env_vars/env.django-nanosourcer.local.yaml