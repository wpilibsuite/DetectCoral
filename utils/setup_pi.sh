#!/bin/bash

sudo apt-get update

wget https://dl.google.com/coral/edgetpu_api/edgetpu_api_latest.tar.gz -O edgetpu_api.tar.gz --trust-server-names

tar xzf edgetpu_api.tar.gz

sudo edgetpu_api/install.sh

