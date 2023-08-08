from antlr4 import InputStream,CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from TypeQLLexer import TypeQLLexer
from TypeQLParser import TypeQLParser
from collections import deque
import re
import copy

class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception(f"error message: {msg}")

class my_type:
    def __init__(self, name: str):
        self.name = name
        self.super_types = set()
        self.abstract = False
        self.roles= set()
    def add_super_type(self,type: str):
        self.super_types.add(type)
    def set_abstract(self,positive: bool):
        self.abstract=positive
    def add_role(self,relation: str,role: str):
        self.roles.add([relation,role])

class typedb_schema_builder_exceptions():
    def __init__(self,schema: str,query_log: deque,types: dict) -> None:
        self.schema=schema
        self.query_log=query_log
        self.types=types
        
    def test(self):
        if(self.grammar_check(copy.deepcopy(self.schema))==0):
            raise Exception("Grammar error\n")
        if(self.check_regex()==0):
            raise Exception("Regex error\n")
        if(self.super_type_check()==0):
            raise Exception("Error creating a type")
        if(self.abstract_match_check()==0):
            raise Exception("The two types on either side of an owns, relates, or plays edge must be either both abstract or both concrete.")
        
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
        query_log_twin=copy.deepcopy(self.query_log)
        n=len(query_log_twin)
        for i in range(0,n):
            query=query_log_twin[0]
            query_log_twin.popleft()
            if(query[0]=="regex"):
                expression=r''+query[2]
                re.compile(expression)
    
    def abstract_match_check(self)-> bool:
        query_log_twin=copy.deepcopy(self.query_log)
        n=len(query_log_twin)
        for i in range(0,n):
            query=query_log_twin[0]
            query_log_twin.popleft()
            abstract_count=[0,0]
            for j in range(0,len(query)):
                if(query[j] in self.types.keys()):
                    if("premitive" in self.types[query[j]].super_types):
                        continue
                    abstract_count[self.types[query[j]].abstract]+=1
            if(abstract_count[0] and abstract_count[1]):
                raise Exception("Error:Mixed types  Qid:",query[-1])
        return 1
    
    def super_type_check(self)-> bool:
        query_log_twin=copy.deepcopy(self.query_log)
        n=len(query_log_twin)
        for i in range(0,n):
            query=query_log_twin[0]
            query_log_twin.popleft()
            if(query[0]=="sub"):
                type=query[2]
                subtype=query[1]
                if(type not in self.types.keys()):
                    raise Exception("Error defining subtype: ",subtype,"\nThe type: ",type," does not exist\nqid:",query[-1] )
                if(subtype in self.types.keys()):
                    if(len(self.types[subtype].super_types)>1):
                        raise Exception("Error defining subtype: ",subtype,"\nThe subtype is already defined\nqid:",query[-1])
            if(query[0]=="plays" or query[0]=="plays_as"):
                if( len(self.types[query[1]]) ):
                    raise Exception("Error, Cannot have multiple roles:", self.types[query[1]].roles,"\nqid:",query[-1])
        return 1
    
class typedb_schema_builder:
    schema=""
    context="?#"
    query_log=deque()
    query_id_generator=1
    types={}
    
    def __init__(self) -> None:
        self.schema="define"
        self.query_id_generator=1
        self.types["attribute"]=my_type("attribute")
        self.types["attribute"].add_super_type("premitive")
        self.types["entity"]=my_type("entity")
        self.types["entity"].add_super_type("premitive")
        self.types["relation"]=my_type("relation")
        self.types["relation"].add_super_type("premitive")

    def get_schema(self):
        checker=typedb_schema_builder_exceptions(schema=self.schema,query_log=self.query_log,types=self.types)
        checker.test()
        escaped_string = r''+self.schema
        decoded_string = bytes(escaped_string, "utf-8").decode("unicode_escape")
        print(decoded_string)
        return decoded_string

    def abstract(self,type: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\tabstract;"
        else:
            self.context=type
            self.schema+="\n"+type+" abstract;"
            
        if(type not in self.types.keys()):
            self.types[type]=my_type(type)
        self.types[type].abstract=True
        self.query_log.append(["abstract",type,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def sub(self,subtype: str,type: str):
        self.context=subtype
        self.schema+= "\n"+subtype+" sub "+type+";"
        
        if(subtype not in self.types.keys()):
            self.types[subtype]=my_type(subtype)
        self.types[subtype].add_super_type(type)
        self.query_log.append(["sub",subtype,type,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def owns(self,type: str,owns: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+= "\n\towns "+owns+";"   
        else:
            self.context=type
            self.schema+= "\n"+type+" owns "+owns+";"
        self.query_log.append(["owns",type,owns,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def owns_as(self,type: str,to_own: str,from_own: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+= "\n\towns "+to_own+" as "+from_own+";"
        else:
            self.context=type
            self.schema+= "\n"+type+" owns "+to_own+" as "+from_own+";"
        self.query_log.append(["owns_as",type,to_own,from_own,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def relates(self,type: str,role: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\trelates "+role+";"
        else:
            self.context=type
            self.schema+="\n"+type+" relates "+role+";"
        
        self.query_log.append(["relates",type,role,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def relates_as(self,type,to_role: str,from_role: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+= "\n\towns "+to_role+" as "+from_role+";"
        else:
            self.context=type
            self.schema+= "\n"+type+" relates "+to_role+" as "+from_role+";"
        self.query_log.append(["relates_as",type,to_role,from_role,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def plays(self,type: str,relation: str,role: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+= "\n\tplays "+relation+":"+role+";"
        else:
            self.context=type
            self.schema+= "\n"+type+" plays "+relation+":"+role+";"

        if(type not in self.types.keys()):
            self.types[type]=my_type(type)
        self.types[type].add_role(relation,role)
        self.query_log.append(["plays",type,relation,role,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def plays_as(self,type: str,relation: str,to_role: str,from_role: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+= "\n\tplays "+relation+":"+to_role+" as "+relation+":"+from_role+";"
        else:
            self.context=type
            self.schema+= "\n"+type+" plays "+relation+":"+to_role+" as "+relation+":"+from_role+";"

        if(type not in self.types.keys()):
            self.types[type]=my_type(type)
        self.types[type].add_role(relation,to_role)
        self.query_log.append(["plays_as",type,relation,to_role,from_role,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def value(self,type: str,value: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\tvalue "+value+";"
        else:
            self.context=type
            self.schema+="\n"+type+" value "+value+";"
        self.query_log.append(["value",type,value,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def regex(self,type: str,regex: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\tregex \""+regex+"\";"
        else:
            self.context=type
            self.schema+="\n"+type+" regex \""+regex+"\";"
        self.query_log.append(["regex",type,regex,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def key(self,type: str,attribute: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\towns "+attribute+" @key;"
        else:
            self.context=type
            self.schema+="\n"+type+" owns "+attribute+" @key;"
        self.query_log.append(["key",type,attribute,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1
        
    def unique(self,type: str,attribute: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\towns "+attribute+" @unique;"
        else:
            self.context=type
            self.schema+="\n"+type+" owns "+attribute+" @unique;"
        self.query_log.append(["unique",type,attribute,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1
    
    
    #idea for remove recontrust schema after negating some queries using query ids and reconstructing schema
    def make_query(self,query: list):
        if(query[0]=="abstract"):
            self.abstract(query[1])
        elif(query[0]=="sub"):
            self.sub(query[1],query[2])
        elif(query[0]=="owns"):
            self.owns(query[1],query[2])
        elif(query[0]=="owns_as"):
            self.owns_as(query[1],query[2],query[3])
        elif(query[0]=="relates"):
            self.relates(query[1],query[2])
        elif(query[0]=="relates_as"):
            self.relates_as(query[1],query[2],query[3])
        elif(query[0]=="plays"):
            self.plays(query[1],query[2],query[3])
        elif(query[0]=="plays_as"):
            self.plays_as(query[1],query[2],query[3])
        elif(query[0]=="value"):
            self.value(query[1],query[2])
        elif(query[0]=="regex"):
            self.regex(query[1],query[2])
        elif(query[0]=="key"):
            self.key(query[1],query[2])
        elif(query[0]=="unique"):
            self.unique(query[1],query[2])
            
    def remove(self,q_ids: list):
        n=len(self.query_log)
        self.schema="define"
        for i in range(0,n):
            query=self.query_log[0]
            self.query_log.popleft()
            if query[-1] in q_ids:
                continue
            self.make_query(query)
    
    def print_query_log(self):
        for q in self.query_log:
            print(q)        
