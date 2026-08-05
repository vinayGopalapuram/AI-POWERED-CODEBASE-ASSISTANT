from app.services.file_service import extract_files
from app.services.chunking_services import chunk_python_code


repo_path = "repositories/django-product-recommender"

extracted_files = extract_files(repo_path)


for file in extracted_files:

    if file["file_path"].endswith("views.py"):

        chunks = chunk_python_code(file)

        print("FILE:", file["file_path"])
        print("TOTAL CHUNKS:", len(chunks))

        for chunk in chunks:

            print("\n" + "=" * 70)

            print("NAME:", chunk["name"])
            print("TYPE:", chunk["chunk_type"])

            print(
                "LINES:",
                chunk["start_line"],
                "-",
                chunk["end_line"]
            )

            print("\nCODE:")
            print(chunk["content"])