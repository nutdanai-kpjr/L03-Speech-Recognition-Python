import openai
from secret_api_key import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def askOpenAiBot(prompt):
    # return "This is my answer"

    # prompt = "What is your favorite color?"
    res = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
    )
    return res["choices"][0]["text"]  # type: ignore
