docker run --rm -it -d -p9003:9003 -p8005:8005 -v /root/project/crisperdx:/home/site/api --net dockercompose_default --link postgresql-crisperdx crisperdx:v0.5 /bin/bash
