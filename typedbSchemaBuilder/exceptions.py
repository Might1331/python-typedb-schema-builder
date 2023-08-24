from antlr4 import InputStream, CommonTokenStream
from .TypeQLLexer import TypeQLLexer
from .TypeQLParser import TypeQLParser
from .MyErrorListener import MyErrorListener
from collections import deque
import re
import copy

class SchemaChecker:
    def __init__(self, schema: str, query_log: deque, types_: dict) -> None:
        self.schema = schema
        self.query_log = query_log
        self.types = types_

    def test(self)-> None:
        if len(self.query_log) == 0:
            raise Exception("Error: Schema is empty. Make changes to the schema before attempting GetSchema")
        
        self.grammar_check(copy.deepcopy(self.schema))
        self.predefined_type_check()
        self.check_regex()
        self.super_type_check()
        self.abstract_match_check()
        self.key_unique_ownership_check()
        # Check for defination availability

    def grammar_check(self, query: str)-> bool:
        lexer = TypeQLLexer(InputStream(query))
        lexer.removeErrorListeners()  # Remove default error listeners
        lexer.addErrorListener(MyErrorListener())
        stream = CommonTokenStream(lexer)
        parser = TypeQLParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyErrorListener())
        try:
            parser.eof_queries()
        except Exception as e:
            raise Exception(e)

    def check_regex(self)-> None:
        query_log_twin = copy.deepcopy(self.query_log)
        n = len(query_log_twin)
        for i in range(0, n):
            query = query_log_twin[0]
            query_log_twin.popleft()
            if query[0] == "regex":
                expression = r"" + query[2]
                re.compile(expression)

    def abstract_match_check(self) -> None:
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
                raise Exception("Error: Mixed types\nqid:"+str(query[-1]))

    def super_type_check(self) -> None:
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
                        "Error defining subtype:"+
                        subtype+
                        "\nThe type:"+
                        type+
                        "does not exist\nqid:"+
                        str(query[-1]),
                    )
                if subtype in self.types.keys():
                    if len(self.types[subtype].super_types)>1:
                        raise Exception(
                            "Error defining subtype:"+
                            subtype+
                            "\nThe subtype is already defined\nqid:"+
                            str(query[-1])
                        )
                    elif len(self.types[subtype].super_types) and type not in self.types[subtype].super_types:
                        raise Exception(
                            "Error defining subtype:"+
                            subtype+
                            "\nThe subtype is already defined\nqid:"+
                            str(query[-1])
                        )
            if query[0] == "plays" or query[0] == "plays_as":
                if len(self.types[query[1]].roles)>1:
                    raise Exception(
                        "Error, Cannot have multiple roles:",
                        self.types[query[1]].roles,
                        "\nqid:"+
                        str(query[-1])
                    )
                elif len(self.types[query[1]].roles) and (query[2],query[-2]) not in self.types[query[1]].roles:
                    raise Exception(
                        "Error, Cannot have multiple roles:",
                        self.types[query[1]].roles,
                        "\nqid:"+
                        str(query[-1]),
                        len(self.types[query[1]].roles)
                    )

    def key_unique_ownership_check(self) -> None:
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
                        "Error: Type="+
                        type+
                        "does not own:"+
                        owns+
                        "\nqid:"+
                        str(query[-1])
                    )
    
    def predefined_type_check(self) -> None:
        query_log_twin = copy.deepcopy(self.query_log)
        n = len(query_log_twin)
        for i in range(0, n):
            query = query_log_twin[0]
            query_log_twin.popleft()
            if query[0] in ["abstract","value","regex"]:
                if query[1] not in self.types.keys():
                    raise Exception("Error: type = "+query[1]+" is not defined"+"\nqid: "+str(query[-1]))
            elif query[0] in ["relates","relates_as"]:
                if query[1] not in self.types.keys():
                    raise Exception("Error: type = "+query[1]+" is not defined"+"\nqid: "+str(query[-1]))
                elif "relation" not in self.types[query[1]].super_types:
                    raise Exception("Error:"+query[1]+" is not an relation type"+"\nqid: "+str(query[-1]))
            elif query[0] in ["owns","owns_as","key","unique"]:
                if query[1] not in self.types.keys():
                    raise Exception("Error: type = "+query[1]+" is not defined"+"\nqid: "+str(query[-1]))
                elif "entity" not in self.types[query[1]].super_types:
                    raise Exception("Error:"+query[1]+" is not an entity type"+"\nqid: "+str(query[-1]))
                
                if query[-2] not in self.types.keys():
                    raise Exception("Error:"+query[-2]+" is not defined"+"\nqid: "+str(query[-1]))
                elif "attribute" not in self.types[query[-2]].super_types:
                    raise Exception("Error:"+query[-2]+" is not an attribute type"+"\nqid: "+str(query[-1]))
            elif query[0] in ["sub"]:
                if query[-2] not in self.types.keys():
                    raise Exception("Error: type = "+query[1]+" is not defined"+"\nqid: "+str(query[-1]))
            elif query[0] in ["plays","plays_as"]:
                if query[1] not in self.types.keys():
                    raise Exception("Error: type = "+query[1]+" is not defined"+"\nqid: "+str(query[-1]))
                if "entity" not in self.types[query[1]].super_types:
                    raise Exception("Error: not entity, type = "+query[1]+"\nqid: "+str(query[-1]))
                
                if query[2] not in self.types.keys():
                    raise Exception("Error: relationship type = "+query[2]+" is not defined"+"\nqid: "+str(query[-1]))
                if "relation" not in self.types[query[2]].super_types:
                    raise Exception("Error: not relationship, type = "+query[2]+"\nqid: "+str(query[-1]))
                
                if query[-2] not in self.types[query[2]].relation_roles:
                    raise Exception("Error: relationship type = "+query[2]+" has no role = "+query[-2]+"\nqid: "+str(query[-1]))
                
        
