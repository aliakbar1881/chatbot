from langchain_gemini import ChatGemini

from app.models.model import Model


class GeminiModel(Model):
    def __init__(self, *args, **kwargs):
        self.super(*args, **kwargs)
    
    def __call__(self):
        self.model = ChatGemini()

    def generate(self, query):
        return self.model.invoke(query).content
