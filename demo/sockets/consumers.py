from channels.consumer import AsyncConsumer, SyncConsumer
import json
from sockets.models import Answer


class AsyncVoiceConsumer(AsyncConsumer):
    """"""

    async def websocket_connect(self, event):
        """"""
        print("connected", event)
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        """"""
        print("recieved", event)
        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })

    async def websocket_disconnect(self, event):
        """"""
        print("disconnected", event)
        await self.send({
            "type": "websocket.disconnect",
        })


class DummyGoogleClient:
    """contains dummy google client functions"""
    def dummy_stt(self, data):
        """"""
        return {
            "text": "dummy data from dummy stt"
        }

    def dummy_dialogue(self, data):
        """"""
        return {
            "data": None,
            "is_command": False
        }

    def dummy_tts(self, data):
        """"""
        return {
            "bytes_data": "",
        }


class VoiceConsumer(SyncConsumer):

    local_dummy_client = DummyGoogleClient()
    ques_list = [{"id": 1, "question": "Hi how are you"}]

    def websocket_connect(self, event):
        print("connected")
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        print("received")
        print(event, '/n')
        # Todo create a functionality to find when question has ended
        ques_end = False

        stt_response = self.local_dummy_client.dummy_stt(event)
        dialogue_response = self.local_dummy_client.dummy_dialogue(stt_response.text)
        if dialogue_response["is_command"]:
            tts_response = self.local_dummy_client.dummy_tts(dialogue_response.data)
            self.send({
                "type": "websocket.send",
                "text": tts_response["bytes_data"],
            })
        answer_obj = {
            'candidate_id': 1,
            'candidate_name': "John",
            'question_id': 1,
            'question': "How are you?",
            'answer': stt_response["text"]
        }

        Answer.objects.create(answer_obj)

        if ques_end:
            if len(self.ques_list) == 0:
                self.send({
                    "type": "websocket.send",
                    "text": "End Interview"
                })
            cur_ques = self.ques_list.pop()
            ques_tts_response = self.local_dummy_client.dummy_tts(cur_ques)
            self.send({
                "type": "websocket.send",
                "text": ques_tts_response["bytes_data"]
            })

        self.send({
            "type": "websocket.send",
            "text": event,
        })

    def websocket_disconnect(self, event):
        """"""
        print("disconnected", event)
        self.send({
            "type": "websocket.disconnect",
        })



from channels.generic.websocket import WebsocketConsumer
# from google.cloud import speech
# from google.oauth2 import service_account

# credentials = service_account.Credentials.from_service_account_file("319006-603d31ac86ca.json")
# client = speech.SpeechClient(credentials=credentials)

# client = speech.SpeechClient(credentials=credentials)
streaming_config = None


class SpeechToTextConsumer(WebsocketConsumer):

    def connect(self):
        print("connected")
        self.accept()

    def disconnect(self, close_code):
        print("disconnect")

    def process(self, responses):
        print("process")
        print(
            responses)  # here i am receiving  response as
        # <google.api_core.grpc_helpers._StreamingResponseIterator object at 0x000002161C7BBA88>
        # noting happens after this
        for response in responses:
            print("response", response)
            if not response.results:
                print("continue")
                continue
            result = response.results[0]
            print("result", result)
            self.send(text_data=json.dumps(result))

    def receive(self, text_data=None, bytes_data=None):
        rate = 16000
        print("recieved")
        # config = speech.RecognitionConfig(
        #     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        #     sample_rate_hertz=rate,
        #     language_code=language_code,
        # )
        # streaming_config = speech.StreamingRecognitionConfig(
        #     config=config, interim_results=True
        # )
        # speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        # stream = [bytes_data]
        # print(stream)
        # requests = (
        #     speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream
        # )
        # responses = client.streaming_recognize(streaming_config, requests)
        responses = {
            "type": "websocket.send",
            "text": "text",
        }
        self.process(responses)
