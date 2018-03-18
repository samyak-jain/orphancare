#!/bin/sh
docker run -e GOOGLE_APPLICATION_CREDENTIALS=codespace-dbec9-firebase-adminsdk-b6rtr-9809b48079.json -it -p 8000:8000 -v $PWD:/usr/src/app f82d511b2d21

