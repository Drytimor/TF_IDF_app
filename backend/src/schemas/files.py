from pydantic import BaseModel, ConfigDict


class BaseFile(BaseModel):
    path: str
    filename: str
    number_words: int


class CreateFile(BaseFile):
    pass


class ReadFile(BaseFile):
    model_config = ConfigDict(from_attributes=True)
    id: int



