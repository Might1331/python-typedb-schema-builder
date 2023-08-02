from antlr4 import InputStream,CommonTokenStream,ParseTreeWalker
from TypeQLListener import TypeQLListener
from TypeQLLexer import TypeQLLexer
from TypeQLParser import TypeQLParser
from collections import deque
import copy

class keyPrinter(TypeQLListener):
    pass

class typedb_schema_builder:
    schema=""
    context="?#"
    query_log=deque()
    query_id_generator=1
    q_to_int={"abstract":1,"sub":2,"owns":3,"owns_as":4,"relates":5,"relates_as":6,"plays":7,
              "plays_as":8,"value":9,"regex":10,"key":11,"unique":12}
    
    def __init__(self) -> None:
        self.schema="define"
        self.query_id_generator=1

    def get_schema(self):
        if( self.grammarCheck(copy.deepcopy(self.schema))==0 ):
            print("grammar error in schema")
            return 0
        
        # if(self.constraintCheck()==0):
        #     print("Invalid Constraints")
        #     return 0
        print(self.schema)
        return 1

    # Error/exception catcher functions
    def grammarCheck(self, query):
        lexer = TypeQLLexer(InputStream(query))
        stream = CommonTokenStream(lexer)
        parser = TypeQLParser(stream)

        try:
            parser.eof_queries()
            return True  # Parsing succeeded, so the expression is valid
        except Exception as e:
            print(f"Error: {e}")  # Print the error message
            return False  # Parsing failed, so the expression is not valid
    
    def constraintCheck():
        pass
    
    
    #defining functions
    def abstract(self,type: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\tabstract;"
        else:
            self.context=type
            self.schema+="\n"+type+"abstract;"
        self.query_log.append([1,type,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def sub(self,subtype: str,type: str):
        self.context=subtype
        self.schema+= "\n"+subtype+" sub "+type+";"
        self.query_log.append([2,subtype,type,self.query_id_generator])
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
        self.query_log.append([3,type,owns,self.query_id_generator])
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
        self.query_log.append([4,type,to_own,from_own,self.query_id_generator])
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
        self.query_log.append([5,type,role,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def relates_as(self,type,to_role: str,from_role: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+= "\n\towns "+to_role+" as "+from_role+";"
        else:
            self.context=type
            self.schema+= "\n"+type+" owns "+to_role+" as "+from_role+";"
        self.query_log.append([6,type,to_role,from_role,self.query_id_generator])
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
        self.query_log.append([7,type,relation,role,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    def plays_as(self,type: str,to_role: str,from_role: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+= "\n\towns "+to_role+" as "+from_role+";"
        else:
            self.context=type
            self.schema+= "\n"+type+" owns "+to_role+" as "+from_role+";"
        self.query_log.append([8,type,to_role,from_role,self.query_id_generator])
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
        self.query_log.append([9,type,value,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1

    # type must be an attribute
    def regex(self,type: str,regex: str):
        if(self.context==type):
            if(self.schema[-1]==';'):
                self.schema=self.schema[:-1]+','
            self.schema+="\n\tregex \""+regex+"\";"
        else:
            self.context=type
            self.schema+="\n"+type+" regex \""+regex+"\";"
        self.query_log.append([10,type,regex,self.query_id_generator])
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
        self.query_log.append([11,type,attribute,self.query_id_generator])
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
        self.query_log.append([12,type,attribute,self.query_id_generator])
        self.query_id_generator+=1
        return self.query_id_generator-1
    
    
    #idea for remove recontrust schema after negating some queries using query ids and reconstructing schema
    #{{"abstract",1},{"sub",2},{"owns",3},{"owns_as",4},{"relates",5},{"relates_as",6},{"plays",7},
    #           {"plays_as",8},{"value",9},{"regex",10},{"key",11},{"unique",12}}
    def make_query(self,query: list):
        if(query[0]==1):
            self.abstract(query[1])
        elif(query[0]==2):
            self.sub(query[1],query[2])
        elif(query[0]==3):
            self.owns(query[1],query[2])
        elif(query[0]==4):
            self.owns_as(query[1],query[2],query[3])
        elif(query[0]==5):
            self.relates(query[1],query[2])
        elif(query[0]==6):
            self.relates_as(query[1],query[2],query[3])
        elif(query[0]==7):
            self.plays(query[1],query[2],query[3])
        elif(query[0]==8):
            self.plays_as(query[1],query[2],query[3])
        elif(query[0]==9):
            self.value(query[1],query[2])
        elif(query[0]==10):
            self.regex(query[1],query[2])
        elif(query[0]==11):
            self.key(query[1],query[2])
        elif(query[0]==12):
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
            self.query_log.append(query)
        
