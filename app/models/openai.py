from langchain_openai import ChatOpenAI

from app.models.model import Model


class OpenAIModel(Model):
    def __init__(self, *args, **kwargs):
        self.super(*args, **kwargs)
    
    def __call__(self):
        self.model = ChatOpenAI()

    def generate(self, query):
        return self.model.invoke(query).content
