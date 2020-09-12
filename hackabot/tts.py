import io
import os
import sys

import pyogg

sys.path.append(os.path.abspath("../voicekit-examples/python"))

from tinkoff.cloud.tts.v1 import tts_pb2_grpc, tts_pb2
from auth import authorization_metadata
import grpc


class TTS:
    def __init__(self, config):
        self._endpoint = config['endpoint'] or "tts.tinkoff.ru:443"
        self._api_key = config['api_key']
        self._secret_key = config['secret_key']
        self._sample_rate = 48000

    def _build_request(self, text):
        return tts_pb2.SynthesizeSpeechRequest(
            input=tts_pb2.SynthesisInput(text=text),
            audio_config=tts_pb2.AudioConfig(
                audio_encoding=tts_pb2.LINEAR16,
                sample_rate_hertz=self._sample_rate,
            ),
        )

    def text2audio(self, text):
        stub = tts_pb2_grpc.TextToSpeechStub(grpc.secure_channel(self._endpoint, grpc.ssl_channel_credentials()))
        request = self._build_request(text)
        metadata = authorization_metadata(self._api_key, self._secret_key, "tinkoff.cloud.tts")
        responses = stub.StreamingSynthesize(request, metadata=metadata)

        for key, value in responses.initial_metadata():
            if key == "x-audio-num-samples":
                print("Estimated audio duration is " + str(int(value) / self._sample_rate) + " seconds")
                break

        f = io.BytesIO()
        ogg_opus_writer = pyogg.OggOpusWriter(f)
        ogg_opus_writer.set_application("audio")
        ogg_opus_writer.set_sampling_frequency(self._sample_rate)
        ogg_opus_writer.set_channels(1)
        ogg_opus_writer.set_frame_size(20)  # milliseconds
        for stream_response in responses:
            ogg_opus_writer.encode(stream_response.audio_chunk)

        # close writer
        ogg_opus_writer.close()

        # get audio
        f.seek(0)
        audio = f.getvalue()

        return audio
