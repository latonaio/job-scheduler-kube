#!/bin/sh

python3 -m job_scheduler
/bin/sh -c "sleep 3"
curl -s -X POST localhost:10001/quitquitquit
