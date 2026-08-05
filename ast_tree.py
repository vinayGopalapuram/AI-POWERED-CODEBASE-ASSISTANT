import ast


code = """
import os


def add(a, b):
    return a + b


class Calculator:

    def multiply(self, a, b):
        return a * b
"""


tree = ast.parse(code)


for node in tree.body:

    if isinstance(node, ast.FunctionDef):

        print(
            "Function:",
            node.name
        )

    elif isinstance(node, ast.ClassDef):

        print(
            "Class:",
            node.name
        )