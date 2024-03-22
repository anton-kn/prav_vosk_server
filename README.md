Установка и настрока Vosk сервера

Установить библитеку для распознавания речи “Воск”
1. Установить python3 и pip3

2. Выполнить следующие команды
    pip3 install vosk

    sudo apt update
    sudo apt install ffmpeg

    Проверить установилась ли программа vosk, выполнив команду в консоли
    vosk-transcriber -h

3. Скачать языковую модель для русского языка
https://alphacephei.com/vosk/models
vosk-model-ru-0.42 (большая модель) и
vosk-model-small-ru-0.22 (маленькая модель). 
Модель положить в папку /storage/app/voskModel

ВНИМАНИЕ!!!
Большим моделям требуется до 16 ГБ оперативной памяти.


Запустить сервер
1. Запустить download.sh или установить на docker. Для запуска в docker надо запустить build.sh далее run.sh