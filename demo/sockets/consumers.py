from channels.consumer import AsyncConsumer, SyncConsumer
import json
from sockets.models import Answer
from ..utils.clients.apiClient import ApiClient


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
        print("received", event)
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
            "bytes_data": b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                          b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                          b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                          b"\x00\x00\x00\x00\x00\x00\x00",
        }


class VoiceConsumer(SyncConsumer):

    local_dummy_client = DummyGoogleClient()
    localApiClient = ApiClient()
    ques_list = []
    cur_ques = None
    candidate_details = None
    assignment_details = None

    def get_bot_intro(self):
        """get conversation bot intro lines"""
        # Todo implement this func
        res = {
            "question": "Hi there this is my intro!",
            "audio": b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                     b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                     b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                     b"\x00\x00\x00\x00\x00\x00\x00",
            "isEnded": False

        }
        return res

    def websocket_connect(self, event):
        print("connected")
        if event.get("candidate_id"):
            candidate_id = event["candidate_id"]
            self.candidate_details = self.localApiClient.dummy_get_candidate_info_by_id(candidate_id)
            if self.candidate_details.status_code != 200:
                # Todo
                print("Could not fetch candidate details!")
        else:
            # Todo
            print("no candidate id provided!")
        if event.get("assignment_id"):
            assignment_id = event["assignment_id"]
            self.assignment_details = self.localApiClient.dummy_get_assignment_info_by_id(assignment_id)
            if self.assignment_details.status_code != 200:
                # Todo
                print("Could not fetch assignment details!")
            else:
                ques_list_details = self.localApiClient.dummy_get_assignment_questions(assignment_id)
                if ques_list_details.status_code != 200:
                    # Todo
                    print("Could not fetch assignment questions!")
                else:
                    self.ques_list = ques_list_details.data

        else:
            # Todo
            print("no assignment id provided!")

        intro_data = self.get_bot_intro()

        self.send({
            "type": "websocket.accept",
            "data": intro_data
        })

    def websocket_receive(self, event):
        print("received")
        print(event, '/n')
        # Todo create a functionality to find when question has ended
        ques_end_trigger = False

        stt_response = self.local_dummy_client.dummy_stt(event)
        # sending received data to gcp dialogue Flow
        dialogue_response = self.local_dummy_client.dummy_dialogue(stt_response['text'])
        if dialogue_response["is_command"]:
            # Todo implement this later, no use now
            tts_response = self.local_dummy_client.dummy_tts(dialogue_response['data'])
            self.send({
                "type": "websocket.send",
                "text": tts_response["bytes_data"],
            })

        # this data will be coming from frontend
        answer_obj = {
            'candidate_id': self.candidate_details.id,
            'candidate_name': self.candidate_details.name,
            'question_id': 1,
            'question': "How are you?",
            'answer': stt_response["text"]
        }
        # save the data into the db
        Answer.objects.create(**answer_obj)

        if ques_end_trigger:
            if len(self.ques_list) == 0:
                # Todo add bot salutations here
                self.send({
                    "type": "websocket.send",
                    "text": "End Interview"
                })
                self.cur_ques = None

            if self.cur_ques is not None:

                answer_obj = {
                    'candidate_id': self.candidate_details.id,
                    'candidate_name': self.candidate_details.name,
                    'question_id': self.cur_ques.id,
                    'question': self.cur_ques.question,
                    'answer': stt_response["text"]
                }
                # save the data into the db
                Answer.objects.create(**answer_obj)

            self.cur_ques = self.ques_list.pop()
            ques_tts_response = self.local_dummy_client.dummy_tts(self.cur_ques.question)
            res = {
                "question_id": self.cur_ques.id,
                "question": self.cur_ques.question,
                "audio": ques_tts_response["bytes_data"]
            }
            self.send({
                "type": "websocket.send",
                "data": res
            })

        self.send({
            "type": "websocket.send",
            "text": stt_response["text"],
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
