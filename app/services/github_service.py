import os
from git import Repo


REPOSITORIES_DIR = "repositories"


def clone_repository(repo_url: str):
    # WHEN THE USER SENDS THE FITHUB URL THIS CODE WILL REMOVE ANY / IN THE END.
    repo_name = repo_url.rstrip("/").split("/")[-1]

    # IF THE FOLDER ENDS WITH .GIT/ THEN THIS IF CONDITION REMOVES THE LAST 4 CHAR
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]


    # THIS WILL CREATE AN LOCAL PATH
    repo_path = os.path.join(
        REPOSITORIES_DIR,
        repo_name
    )

    # if repo already exists then reuse it
    if os.path.exists(repo_path):
        # print("repo already exists:",repo_path)
        return repo_path
    
    # HERE THE CLONING HAPPENS AND THE GITPYTHON CONTACTS THE FITHUB AND THEN STORES IT REPOSITORIES
    Repo.clone_from(
        repo_url,
        repo_path
    )

    return repo_path