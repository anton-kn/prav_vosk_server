Установка и настрока Vosk-сервера

Варианты запуска Vosk-сервера:
1. Запустить сервер в Docker
1.1. Из папки ru-big-model
- загрузить модели download.sh
- запустить build.sh далее run.sh

1.2 Из папки ru-big-model_v2
- запустить build.sh далее run.sh

1.3 Из папки ru-small-model
- запустить build.sh далее run.sh

2. Запустить сервер в локально 
- установить python3 и pip3
- выполнить следующие команды
    pip3 install vosk
    sudo apt update
    sudo apt install ffmpeg

    Проверить установилась ли программа vosk, выполнив команду в консоли
    vosk-transcriber -h
2.1 Из папки ru-small-model
- загрузить модели download.sh
- запустить run_server.sh

2.2 Из папки ru-big-model
- загрузить модели download.sh
- запустить run_server.sh


ВНИМАНИЕ!!!
Большим моделям требуется до 16 ГБ оперативной памяти.


