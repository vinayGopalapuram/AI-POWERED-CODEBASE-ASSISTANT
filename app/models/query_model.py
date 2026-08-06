from pydantic import BaseModel


class queryrequest(BaseModel):
    question:str
    repo_name:str