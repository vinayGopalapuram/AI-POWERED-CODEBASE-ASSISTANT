import os
SUPPORTED_EXTENSIONS = {
    ".py": "python"
}
IGNORED_DIRECTORIES = {
    ".git",
    "venv",
    ".venv",
    "node_modules",
    "__pycache__",
    ".idea",
    ".vscode",
    "dist",
    "build",
}

def extract_files(repo_path: str):
    # used to contain the extracted files 

    extracted_files = []

    # here the os.walk will go through the entire file recursively that is first when the user sends the github url then it will go to the root file and then in the next iteration it goes to the inner file of the root 
    for root, directories, files in os.walk(repo_path):

        directories[:] = [
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        ]

        for file_name in files:
            # it splits the file name from files that is if filename is main.py then ["main",".py"] and then extract the index 1 that is .py and then stores it in extension
            extension = os.path.splitext(file_name)[1].lower()

            # here we check if the extension os valid or not if yes we continue the processing else move to next file
            if extension not in SUPPORTED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file_name)

            try:
                # this logic is used to read the source code 
                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:
                    # file.read() converts the entire thing into a Python string:
                    content = file.read()

            except (UnicodeDecodeError, OSError):
                continue
            # after the whole process of checking the file is compateble or not and then extracting the source code and turning it into py string we append it into the extracted files list  in the form of dict
            extracted_files.append({
                "file_path": file_path,
                "language": SUPPORTED_EXTENSIONS[extension],
                "content": content
            })
    
    return extracted_files     
    