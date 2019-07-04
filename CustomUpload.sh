#!/usr/bin/env bash

curl -X POST "http://192.168.0.253:9898/api/apps/5d15e0763f1ef9001e64eb45/upload" -H "accept: application/json" -H "apikey:de39f04d5da810ff28ca9d9d487687de" -H "content -type: mudata" -F "file=@${1}"