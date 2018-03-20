#!/bin/bash
# for the prod server: fetches new code and restarts the server.

git pull origin master
touch /var/www/www_thedevopscourse_com_wsgi.py
