FROM ubuntu:latest

ENV TERM linux

run echo "travis_fold:start:Dapt\033[33;1mservice Dockerfile apt\033[0m" && \
    apt-get -qq update && apt-get -qq install python3-urllib3 &&
    echo "\ntravis_fold:end:Dapt\r"

COPY check.py /


