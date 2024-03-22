#!/usr/bin/env python3

import json
import os
import sys
import asyncio
import pathlib
import websockets
import concurrent.futures
import logging
import numpy
from vosk import Model, SpkModel, KaldiRecognizer

def process_chunk(rec, message):
    if message == '{"eof" : 1}':
        return rec.FinalResult(), True
    if message == '{"reset" : 1}':
        return rec.FinalResult(), False
    elif rec.AcceptWaveform(message):
        return rec.Result(), False
    else:
        return rec.PartialResult(), False
    
def cosine_dist(x, y):
    nx = numpy.array(x)
    ny = numpy.array(y)
    return 1 - numpy.dot(nx, ny) / numpy.linalg.norm(nx) / numpy.linalg.norm(ny)

# все косинусные дистанции
def get_distances(x_vectors_from, current_x_vector):
    distances = []
    for x_vector in x_vectors_from:
        distances.append(cosine_dist(x_vector, current_x_vector))
    
    return distances


async def recognize(websocket, path):
    global model
    global spk_model
    global args
    global pool

    loop = asyncio.get_running_loop()
    rec = None
    phrase_list = None
    sample_rate = args.sample_rate
    show_words = args.show_words
    max_alternatives = args.max_alternatives

    logging.info('Connection from %s', websocket.remote_address);

    while True:

        message = await websocket.recv()
        # logging.info('Входные данные %s', message);

        # Load configuration if provided
        if isinstance(message, str) and 'config' in message:
            jobj = json.loads(message)['config']
            # logging.info("Config %s", jobj)
            if 'phrase_list' in jobj:
                phrase_list = jobj['phrase_list']
            if 'sample_rate' in jobj:
                sample_rate = float(jobj['sample_rate'])
            if 'model' in jobj:
                model = Model(jobj['model'])
                model_changed = True
            if 'words' in jobj:
                show_words = bool(jobj['words'])
            if 'max_alternatives' in jobj:
                max_alternatives = int(jobj['max_alternatives'])
            if 'x-vectors' in jobj:
                x_vectors_from = jobj['x-vectors']
                # logging.info("Vectors %s", x_vectors_from)
            if 'spk' in jobj:
                spk = jobj['spk']
                # logging.info("Vectors %s", x_vectors_from)
            continue

        # Create the recognizer, word list is temporary disabled since not every model supports it
        if not rec or model_changed:
            model_changed = False
            if phrase_list:
                rec = KaldiRecognizer(model, sample_rate, json.dumps(phrase_list, ensure_ascii=False))
            else:
                rec = KaldiRecognizer(model, sample_rate)
            rec.SetWords(show_words)
            rec.SetMaxAlternatives(max_alternatives)
            if spk_model:
                rec.SetSpkModel(spk_model)

        response, stop = await loop.run_in_executor(pool, process_chunk, rec, message)
        resp_json = json.loads(response)
        text = '';
        dist = '';
        spk_res = '';
        if 'spk' in locals():
            if "text" in resp_json:
                # logging.info('Данные %s', resp_json['text'])
                text = resp_json['text']
            if "spk" in resp_json:
                # logging.info('Вектор %s', resp_json['spk'])
                spk_res = resp_json['spk']
        else:
            if "text" in resp_json:
                # logging.info('Данные %s', resp_json['text']);
                text = resp_json['text']
            if "spk" in resp_json:
                # logging.info('Вектор %s', resp_json['spk']);
                dist = get_distances(x_vectors_from, resp_json['spk'])
                logging.info('Косин. дистанции %s', dist);

        if 'spk' in locals():
            res = '{"text":"' + text + '", "spk":' + str(spk_res) + '}'
        else: 
            res = '{"text":"' + text + '", "cosine_dist":' + str(dist) + '}'
            
        
        await websocket.send(res)
        if stop: break



async def start():

    global model
    global spk_model
    global args
    global pool

    # Enable loging if needed
    #
    # logger = logging.getLogger('websockets')
    # logger.setLevel(logging.INFO)
    # logger.addHandler(logging.StreamHandler())
    logging.basicConfig(level=logging.INFO)

    args = type('', (), {})()

    args.interface = os.environ.get('VOSK_SERVER_INTERFACE', '0.0.0.0')
    args.port = int(os.environ.get('VOSK_SERVER_PORT', 2700))
    args.model_path = os.environ.get('VOSK_MODEL_PATH', 'model')
    args.spk_model_path = os.environ.get('VOSK_SPK_MODEL_PATH')
    # args.spk_model_path = 'vosk-model-spk-0.4'
    args.sample_rate = float(os.environ.get('VOSK_SAMPLE_RATE', 16000))
    args.max_alternatives = int(os.environ.get('VOSK_ALTERNATIVES', 0))
    args.show_words = bool(os.environ.get('VOSK_SHOW_WORDS', False))

    if len(sys.argv) > 1:
       args.model_path = sys.argv[1]
       args.spk_model_path = sys.argv[2]

    # Gpu part, uncomment if vosk-api has gpu support
    #
    # from vosk import GpuInit, GpuInstantiate
    # GpuInit()
    # def thread_init():
    #     GpuInstantiate()
    # pool = concurrent.futures.ThreadPoolExecutor(initializer=thread_init)

    model = Model(args.model_path)
    spk_model = SpkModel(args.spk_model_path) if args.spk_model_path else None

    pool = concurrent.futures.ThreadPoolExecutor((os.cpu_count() or 1))

    async with websockets.serve(recognize, args.interface, args.port):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(start())
