#!/bin/bash

function stop()
{
    ps -ef|grep gunicorn|grep -v grep |awk '{print $2}'|xargs kill -9
}

function start()
{
    gunicorn webKeepass.wsgi -b 0.0.0.0:18888 --reload -D --access-logfile logs/gunicorn.log  --error-logfile logs/gunicorn.log
}

function status() {
    ps -ef|grep gunicorn|grep -v grep
}

case $1 in
  -s)
  stop
  ;;
  -k)
  start
  ;;
  -l)
  status
  ;;
  -r)
  stop
  start
  ;;
  *)
	echo "Usage: $0"
	echo -e "\t-k[start]\n\t-s[stop]\n\t-r[restart]\n\t-l[list processes]"
esac
