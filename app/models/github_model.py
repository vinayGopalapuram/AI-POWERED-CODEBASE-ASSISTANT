# TO DEFINE AND VALIDATE THE STRUCTURE OF THE INCOMING AND OUTGOING DATA
from pydantic import BaseModel


class GitHubRequest(BaseModel):
    repo_url: str