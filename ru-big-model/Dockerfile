FROM alphacep/kaldi-vosk-server:latest

ENV MODEL_VERSION 0.22
ENV MODEL_SPK 0.4
RUN mkdir /opt/vosk-model-big-ru \
   && mkdir /opt/vosk-model-spk \
   && pip install numpy

COPY ./websocket/asr_server_2.py /opt/vosk-server/websocket

EXPOSE 2700
WORKDIR /opt/vosk-server/websocket
ENV VOSK_SAMPLE_RATE 16000

CMD [ "python3", "./asr_server_2.py", "/opt/vosk-model-big-ru", "/opt/vosk-model-spk" ]
