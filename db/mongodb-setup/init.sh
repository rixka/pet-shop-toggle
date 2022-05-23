#!/bin/bash

mongoimport --host mongodb --db development --collection pets --type json --file /pets.json --jsonArray
mongo --host mongodb < init.js
