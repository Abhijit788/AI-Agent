from pydantic import BaseModel


class CurrentWeatherInput(BaseModel):
    location: str


class FutureWeatherInput(BaseModel):
    location: str
    date: str



class ConversationManager(BaseModel):
    def __init__(self):
        self.conversations = {}