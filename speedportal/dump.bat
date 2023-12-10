@echo off
python -Xutf8 %~dp0/manage.py dumpdata --exclude auth.permission --exclude contenttypes -o %~dp0/fixtures/dump1.json