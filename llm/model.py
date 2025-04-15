import asyncio

from ollama import AsyncClient

PROMPT = """
Depending on the given resume, and HR request. Answer can be candidate hired. Rate candidate from 0 to 10 depending
on year of experience, tools candidate know, and depending on projects, how much benefit he bring to company if given,
and is it reliable for HR requests. if you rate below 5 then give a feedback.

HR request:
{request}

Candidate is Resume:
{resume}
"""

class Model:
    model_name: str
    prompt: str = PROMPT

    def __init__(self, model_name: str, resume: str, request: str):
        self.model_name = model_name
        self.message = [
            {
                'role': 'user',
                'content': self.prompt.format(resume=resume, request=request)
              },
        ]
        self.client = AsyncClient()

    async def response(self):
        response = await self.client.chat(model=self.model_name, messages=self.message, stream=True)
        result = []
        async for message in response:
            print(message['message']['content'], end='', flush=True)
            result.append(message['message']['content'])
        return " ".join(result)

if __name__ == "__main__":
    with open("../test/resources/resume.txt", "r") as text:
        resume = text.read()
    model = Model("gemma3:1b", resume=resume, request="junior ML engineer with experience in nlp")
    result = asyncio.run(model.response())
    print(result)