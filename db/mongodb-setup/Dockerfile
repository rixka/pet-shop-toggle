FROM mvertes/alpine-mongo

RUN apk add --no-cache mongodb-tools

COPY pets.json /pets.json
COPY init.sh /init.sh
COPY init.js /init.js
#CMD mongoimport --host mongodb --db development --collection pets --type json --file /pets.json --jsonArray
CMD sh /init.sh
