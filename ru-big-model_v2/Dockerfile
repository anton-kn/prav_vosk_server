FROM alphacep/kaldi-vosk-server:latest

ENV MODEL_VERSION 0.42
ENV MODEL_SPK 0.4

RUN mkdir /opt/vosk-model-ru \
   && cd /opt/vosk-model-ru \
   && wget -q https://alphacephei.com/vosk/models/vosk-model-ru-${MODEL_VERSION}.zip \
   && unzip vosk-model-ru-${MODEL_VERSION}.zip \
   && mv vosk-model-ru-${MODEL_VERSION} model \
   && rm vosk-model-ru-${MODEL_VERSION}.zip \
   && mkdir /opt/vosk-model-spk \
   && cd /opt \
   && wget -q https://alphacephei.com/vosk/models/vosk-model-spk-${MODEL_SPK}.zip \
   && unzip vosk-model-spk-${MODEL_SPK}.zip \
   && cd vosk-model-spk-${MODEL_SPK} \
   && mv * /opt/vosk-model-spk \
   && cd ../ \
   && rm vosk-model-spk-${MODEL_SPK}.zip \
   && pip install numpy

COPY ./websocket/asr_server_2.py /opt/vosk-server/websocket

EXPOSE 2700
WORKDIR /opt/vosk-server/websocket
ENV VOSK_SAMPLE_RATE 16000
CMD [ "python3", "./asr_server_2.py", "/opt/vosk-model-ru/model", "/opt/vosk-model-spk" ]
