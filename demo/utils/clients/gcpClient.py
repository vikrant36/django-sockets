import logging

from google.cloud.texttospeech_v1 import SynthesizeSpeechResponse
from google.cloud import speech
from google.cloud import texttospeech
from google.oauth2 import service_account
# credentials = service_account.Credentials.from_service_account_file("319006-603d31ac86ca.json")
from base.exceptions.exceptions import CustomServerError
from constants import WAVENET_SERVICE, LANGUAGE_CODE, AUDIO_PITCH, SPEECH_RATE


class VoiceService:
    """"""

    client = speech.SpeechClient()
    streaming_config = None
    male_voice = texttospeech.SsmlVoiceGender.MALE
    encode_audio = texttospeech.AudioEncoding.MP3
    speech_encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16

    def text_to_speech(self, text) -> SynthesizeSpeechResponse:
        try:
            client = texttospeech.TextToSpeechClient()

            input_text = texttospeech.SynthesisInput(text=text)

            # Note: the voice can also be specified by name.
            # Names of voices can be retrieved with client.list_voices().
            voice = texttospeech.VoiceSelectionParams(
                language_code=LANGUAGE_CODE,
                name=WAVENET_SERVICE,
                ssml_gender=self.male_voice
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=self.encode_audio,
                pitch=AUDIO_PITCH
            )

            response = client.synthesize_speech(
                request={"input": input_text,
                         "voice": voice,
                         "audio_config": audio_config
                         }
            )
            print(response)
            return response
        except Exception as e:
            return CustomServerError(e)

    def speech_to_text(self, content):
        try:
            client = speech.SpeechClient()
            audio = speech.RecognitionAudio(content=content)

            config = speech.RecognitionConfig(
                encoding=self.speech_encoding,
                sample_rate_hertz=SPEECH_RATE,
                language_code=LANGUAGE_CODE,
            )

            operation = client.long_running_recognize(config=config, audio=audio)

            print("Waiting for operation to complete...")
            response = operation.result()
            print(response)

            # Each result is for a consecutive portion of the audio. Iterate through
            # them to get the transcripts for the entire audio file.
            for result in response.results:
                # The first alternative is the most likely one for this portion.
                print(u"Transcript: {}".format(result.alternatives[0].transcript))
                print("Confidence: {}".format(result.alternatives[0].confidence))

            return response
        except Exception as e:
            return CustomServerError(e)

    def stt_chunks(self, data):
        print("stt_recieved")
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=SPEECH_RATE,
            language_code=LANGUAGE_CODE,
        )
        streaming_config = speech.StreamingRecognitionConfig(
            config=config, interim_results=True
        )
        speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        print(data)
        requests = (
            speech.StreamingRecognizeRequest(audio_content=data)
        )
        responses = self.client.streaming_recognize(streaming_config, requests)
        return responses
