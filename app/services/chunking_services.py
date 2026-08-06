import ast


def get_chunk_type(node):

    if isinstance(node, ast.ClassDef):
        return "class"

    if isinstance(node, ast.AsyncFunctionDef):
        return "async_function"

    return "function"

# in this fun we are passing the extracted files into file data 
def chunk_python_code(file_data: dict):

    content = file_data["content"]
    tree = ast.parse(content)
    lines = content.splitlines()
    chunks = []
    structural_nodes = []
    for node in tree.body:

        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            structural_nodes.append(node)

            start_line = node.lineno
            end_line = node.end_lineno

            chunk_content = "\n".join(
                lines[start_line - 1:end_line]
            )
            chunks.append({
                "file_path": file_data["file_path"],
                "language": "python",
                "chunk_type": get_chunk_type(node),
                "name": node.name,
                "start_line": start_line,
                "end_line": end_line,
                "content": chunk_content
            })

    structural_lines = set()

    for node in structural_nodes:
        structural_lines.update(
            range(node.lineno, node.end_lineno + 1)
        ) 


    # used to collect other module level code and then chunk it 
    module_lines = []

    for line_number, line in enumerate(lines, start=1):
        if line_number not in structural_lines:
            module_lines.append(line)

    module_content = "\n".join(module_lines).strip()


    # this is to create module chuck
    if module_content:
        chunks.append({
            "file_path": file_data["file_path"],
            "language": "python",
            "chunk_type": "module",
            "name": "module_level_code",
            "start_line": 1,
            "end_line": len(lines),
            "content": module_content
        })
    return chunks


def chunk_all_files(extracted_files: list):

    all_chunks = []

    for file_data in extracted_files:
        try:
            file_chunks = chunk_python_code(file_data)
            all_chunks.extend(file_chunks)

        except SyntaxError:
            continue

    # print(all_chunks)
    return all_chunks