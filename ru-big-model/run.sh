#!/bin/bash

MODEL_VERSION=0.42
MODEL_SPK=0.4

docker run -d -p 2700:2700 \
-v ./model/vosk-model-ru-${MODEL_VERSION}:/opt/vosk-model-big-ru \
-v ./model/vosk-model-spk-${MODEL_SPK}:/opt/vosk-model-spk \
--name vs-ru-big-model vosk-server-ru-big-model