import json
import os

import boto3
from config import GENERATION_CONFIG
from utils import get_bedrock_client

client = get_bedrock_client()


def _create_body(model: str, prompt: str):
    if model == "titan":
        query = prompt  #"hey titan, how many patients have the condition asthma?"
        prompt = f"""Take on the persona of a doctor named 'Dr Steve'. Interactively Interview the patient step-by-step, one question at a using the patients previous answers to decide which question to ask next. <text>{query} </text>"""
        parameter = {}
        parameter["textGenerationConfig"] = GENERATION_CONFIG
        parameter["inputText"] = prompt
        print(json.dumps(parameter))
        return json.dumps(parameter)
    else:
        raise NotImplementedError()


def _extract_output_text(model: str, response) -> str:
    if model == "titan":
        response = json.loads(response.get("body").read())
        response_body = json.loads(response.get('body').read())
        output_txt = response_body.get('results')[0].get('outputText')

        return output_txt
    else:
        raise NotImplementedError()


def get_model_id(model: str) -> str:
    if model == "titan":
        return "amazon.titan-tg1-xlarge"
    else:
        raise NotImplementedError()


def invoke(prompt: str, model: str) -> str:
    payload = _create_body(model, prompt)

    model_id = get_model_id(model)
    accept = "application/json"
    content_type = "application/json"

    response = client.invoke_model(
        body=payload, modelId=model_id, accept=accept, contentType=content_type
    )

    output_txt = _extract_output_text(model, response)

    return output_txt


def invoke_with_stream(prompt: str, model: str):
    raise NotImplementedError("Not supported yet")

    payload = _create_body(model, prompt)

    model_id = get_model_id(model)
    accept = "application/json"
    content_type = "application/json"

    response = client.invoke_model_with_response_stream(body=payload, modelId=model_id)
    stream = response.get("body")

    if stream:
        for event in stream:
            chunk = event.get("chunk")
            if chunk:
                output_txt = chunk.get("bytes").decode()
                output_txt = json.loads(output_txt).get("outputText")
                yield output_txt
