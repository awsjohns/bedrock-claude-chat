import json
import unittest
from pprint import pprint

from bedrock import client, invoke
from repositories.model import ContentModel, MessageModel
from utils import get_buffer_string

MODEL = "titan"


class TestBedrock(unittest.TestCase):
    def test_invoke(self):
        prompt = "Recommended Japanese anime"
        model = MODEL

        reply_txt = invoke(prompt, model)
        print(reply_txt)

    def test_invoke_with_multi_messages(self):
        messages = [
            MessageModel(
                id="2",
                role="user",
                content=ContentModel(
                    content_type="text",
                    body="Hello",
                ),
                model=MODEL,
                create_time=1627984879.9,
            ),
            MessageModel(
                id="3",
                role="assistant",
                content=ContentModel(
                    content_type="text",
                    body="Hello! What happened?",
                ),
                model=MODEL,
                create_time=1627984879.9,
            ),
            MessageModel(
                id="4",
                role="user",
                content=ContentModel(	
                    content_type="text",
                    body="Learn about good ways to learn AWS",
                ),
                model=MODEL,
                create_time=1627984879.9,
            ),
        ]

        prompt = get_buffer_string(messages)
        model = MODEL

        reply_txt = invoke(prompt, model)
        print(reply_txt)


class TestBedrockStream(unittest.TestCase):
    def test_invoke_with_stream(self):
        payload = {
            "body": '{"max_tokens_to_sample": 500, "temperature": 0.0, "top_k": 250, "top_p": 0.999, "stop_sequences": ["Human: ", "Assistant: "], "prompt": "Human: famous ghibli movies 1\\nAssistant: "}',
            "modelId": "amazon.titan-tg1-large",
            "accept": "application/json",
            "contentType": "application/json",
        }
        # Invoke bedrock endpoint directly

        response = client.invoke_model_with_response_stream(**payload)

        stream = response.get("body")

        if stream:
            for event in stream:
                chunk = event.get("chunk")
                if chunk:
                    # pprint(chunk)
                    chunk_bytes = chunk.get("bytes")
                    chunk_data = json.loads(chunk_bytes.decode("utf-8"))
                    completion = chunk_data.get("completion")
                    if completion:
                        print(completion)


if __name__ == "__main__":
    unittest.main()
