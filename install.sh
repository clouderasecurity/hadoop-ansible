#!/bin/bash

source venv/bin/activate
ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install $(grep pycrypto requirements.txt)
pip install -r requirements.txt
