#!/bin/bash

cd model

MODEL_VERSION=0.22
MODEL_SPK=0.4

echo "Идет загрузка моделей..."

wget -q https://alphacephei.com/vosk/models/vosk-model-small-ru-${MODEL_VERSION}.zip
unzip vosk-model-small-ru-${MODEL_VERSION}.zip
rm vosk-model-small-ru-${MODEL_VERSION}.zip

wget -q https://alphacephei.com/vosk/models/vosk-model-spk-${MODEL_SPK}.zip
unzip vosk-model-spk-${MODEL_SPK}.zip
rm vosk-model-spk-${MODEL_SPK}.zip

echo "Модели загружены."