from antlr4 import InputStream, CommonTokenStream
from .TypeQLLexer import TypeQLLexer
from .TypeQLParser import TypeQLParser
from .MyErrorListener import MyErrorListener
from collections import deque
import re
import copy

class TypeQLExceptions:
    def __init__(self, schema: str, query_log: deque, types_: dict) -> None:
        self.schema = schema
        self.query_log = query_log
        self.types = types_

    def test(self):
        if len(self.query_log) == 0:
            raise Exception("Error: Schema is empty. Make changes to the schema before attempting GetSchema")
        if self.grammar_check(copy.deepcopy(self.schema)) == 0:
            raise Exception("Grammar error\n")
        self.check_regex()
        self.super_type_check()
        self.abstract_match_check()
        self.key_unique_ownership_check()

    def grammar_check(self, query):
        lexer = TypeQLLexer(InputStream(query))
        lexer.removeErrorListeners()  # Remove default error listeners
        lexer.addErrorListener(MyErrorListener())
        stream = CommonTokenStream(lexer)
        parser = TypeQLParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyErrorListener())
        try:
            parser.eof_queries()
            return True  # Parsing succeeded, so the expression is valid
        except Exception as e:
            print(f"Error: {e}")  # Print the error message
            return False  # Parsing failed, so the expression is not valid

    def check_regex(self):
        query_log_twin = copy.deepcopy(self.query_log)
        n = len(query_log_twin)
        for i in range(0, n):
            query = query_log_twin[0]
            query_log_twin.popleft()
            if query[0] == "regex":
                expression = r"" + query[2]
                re.compile(expression)

    def abstract_match_check(self) -> bool:
        query_log_twin = copy.deepcopy(self.query_log)
        n = len(query_log_twin)
        for i in range(0, n):
            query = query_log_twin[0]
            query_log_twin.popleft()
            abstract_count = [0, 0]
            for j in range(0, len(query)):
                if query[j] in self.types.keys():
                    if "thing" in self.types[query[j]].super_types:
                        continue
                    abstract_count[self.types[query[j]].abstract] += 1
            if abstract_count[0] and abstract_count[1]:
                raise Exception("Error: Mixed types  Qid:", query[-1])

    def super_type_check(self) -> bool:
        query_log_twin = copy.deepcopy(self.query_log)
        n = len(query_log_twin)
        for i in range(0, n):
            query = query_log_twin[0]
            query_log_twin.popleft()
            if query[0] == "sub":
                type = query[2]
                subtype = query[1]
                if type not in self.types.keys():
                    raise Exception(
                        "Error defining subtype:",
                        subtype,
                        "\nThe type:",
                        type,
                        "does not exist\nqid:",
                        query[-1],
                    )
                if subtype in self.types.keys():
                    if len(self.types[subtype].super_types) > 1:
                        raise Exception(
                            "Error defining subtype:",
                            subtype,
                            "\nThe subtype is already defined\nqid:",
                            query[-1],
                        )
            if query[0] == "plays" or query[0] == "plays_as":
                if len(self.types[query[1]]):
                    raise Exception(
                        "Error, Cannot have multiple roles:",
                        self.types[query[1]].roles,
                        "\nqid:",
                        query[-1],
                    )

    def key_unique_ownership_check(self) -> bool:
        query_log_twin = copy.deepcopy(self.query_log)
        n = len(query_log_twin)
        for i in range(0, n):
            query = query_log_twin[0]
            query_log_twin.popleft()
            if query[0] == "key" or query[0] == "unique":
                type = query[1]
                owns = query[2]
                if owns not in self.types[type].attributes:
                    raise Exception(
                        "Error: Type=",
                        type,
                        "does not own:",
                        owns,
                        "\nqid:",
                        query[-1],
                    )
