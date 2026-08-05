from app.services.file_service import extract_files


repo_path = "repositories/django-product-recommender"

extracted_files = extract_files(repo_path)

print("Total Python files:", len(extracted_files))

for file in extracted_files:
    print("------------------------")
    print("File:", file["file_path"])
    print("Language:", file["language"])