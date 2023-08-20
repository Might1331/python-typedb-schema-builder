from collections import deque
from .MyType import MyType
from .exceptions import exceptions

class builder:
    schema = ""
    context = "?#"
    QueryLog = deque()
    QueryIdGenerator = 1
    types = {}

    def __init__(self) -> None:
        self.schema = "define"
        self.QueryIdGenerator = 1
        self.types["attribute"] = MyType("attribute")
        self.types["attribute"].AddSuperType("thing")
        self.types["entity"] = MyType("entity")
        self.types["entity"].AddSuperType("thing")
        self.types["relation"] = MyType("relation")
        self.types["relation"].AddSuperType("thing")

    def getSchema(self):
        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        escapedString = r"" + self.schema
        decodedString = bytes(escapedString, "utf-8").decode("unicode_escape")
        print(decodedString)
        return decodedString

    def abstract(self, type: str, qid: int=-1):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\tabstract;"
        else:
            self.context = type
            self.schema += "\n" + type + " abstract;"

        if type not in self.types.keys():
            self.types[type] = MyType(type)
        self.types[type].abstract = True
        
        if(qid==-1):
            self.QueryLog.append(["abstract", type, self.QueryIdGenerator])
            self.QueryIdGenerator += 1
        else:
            self.QueryLog.append(["abstract", type, qid])
            
        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        return self.QueryLog[-1][-1]

    def sub(self, subtype: str, type: str, qid: int=-1):
        self.context = subtype
        self.schema += "\n" + subtype + " sub " + type + ";"

        if subtype not in self.types.keys():
            self.types[subtype] = MyType(subtype)
        self.types[subtype].AddSuperType(type)
        
        if(qid==-1):
            self.QueryLog.append(["sub", subtype, type, self.QueryIdGenerator])
            self.QueryIdGenerator += 1
        else:
            self.QueryLog.append(["sub", subtype, type, qid])
            
        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        return self.QueryLog[-1][-1]

    def owns(self, type: str, owns: str, qid: int=-1):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\towns " + owns + ";"
        else:
            self.context = type
            self.schema += "\n" + type + " owns " + owns + ";"

        if type not in self.types.keys():
            self.types[type] = MyType(type)
        self.types[type].AddAttribute(owns)
        
        if(qid==-1):
            self.QueryLog.append(["owns", type, owns, self.QueryIdGenerator])
            self.QueryIdGenerator += 1
        else:
            self.QueryLog.append(["owns", type, owns, qid])
            
        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        return self.QueryLog[-1][-1]

    def ownsAs(self, type: str, to_own: str, from_own: str, qid: int=-1):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\towns " + to_own + " as " + from_own + ";"
        else:
            self.context = type
            self.schema += "\n" + type + " owns " + to_own + " as " + from_own + ";"

        if type not in self.types.keys():
            self.types[type] = MyType(type)
        self.types[type].AddAttribute(to_own)
        
        if(qid==-1):
            self.QueryLog.append( ["ownsAs", type, to_own, from_own, self.QueryIdGenerator])
            self.QueryIdGenerator += 1
        else:
            self.QueryLog.append( ["ownsAs", type, to_own, from_own, qid])
            
        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        return self.QueryLog[-1][-1]

    def relates(self, type: str, role: str, qid: int=-1):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\trelates " + role + ";"
        else:
            self.context = type
            self.schema += "\n" + type + " relates " + role + ";"

        if(qid==-1):
            self.QueryLog.append(["relates", type, role, self.QueryIdGenerator])
            self.QueryIdGenerator += 1
        else:
            self.QueryLog.append(["relates", type, role, qid])
            
        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        return self.QueryLog[-1][-1]

    def relatesAs(self, type, toRole: str, fromRole: str, qid: int=-1):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\towns " + toRole + " as " + fromRole + ";"
        else:
            self.context = type
            self.schema += (
                "\n" + type + " relates " + toRole + " as " + fromRole + ";"
            )
        
        if(qid==-1):
            self.QueryLog.append( ["relatesAs", type, toRole, fromRole, self.QueryIdGenerator] )
            self.QueryIdGenerator += 1
        else:
            self.QueryLog.append( ["relatesAs", type, toRole, fromRole, qid] )
            
        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        return self.QueryLog[-1][-1]

    def plays(self, type: str, relation: str, role: str, qid: int=-1):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\tplays " + relation + ":" + role + ";"
        else:
            self.context = type
            self.schema += "\n" + type + " plays " + relation + ":" + role + ";"

        if type not in self.types.keys():
            self.types[type] = MyType(type)
        self.types[type].AddRole(relation, role)
        
        if(qid==-1):
            self.QueryLog.append(["plays", type, relation, role, self.QueryIdGenerator])
            self.QueryIdGenerator += 1
        else:
            self.QueryLog.append(["plays", type, relation, role, qid])
            
        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        return self.QueryLog[-1][-1]

    def playsAs(self, type: str, relation: str, toRole: str, fromRole: str, qid: int=-1):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += (
                "\n\tplays "
                + relation
                + ":"
                + toRole
                + " as "
                + relation
                + ":"
                + fromRole
                + ";"
            )
        else:
            self.context = type
            self.schema += (
                "\n"
                + type
                + " plays "
                + relation
                + ":"
                + toRole
                + " as "
                + relation
                + ":"
                + fromRole
                + ";"
            )

        if type not in self.types.keys():
            self.types[type] = MyType(type)
        self.types[type].AddRole(relation, toRole)
        
        if(qid==-1):
            self.QueryLog.append( ["playsAs", type, relation, toRole, fromRole, self.QueryIdGenerator])
            self.QueryIdGenerator += 1
        else:
            self.QueryLog.append( ["playsAs", type, relation, toRole, fromRole, qid])

        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        return self.QueryLog[-1][-1]

    def value(self, type: str, value: str, qid: int=-1):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\tvalue " + value + ";"
        else:
            self.context = type
            self.schema += "\n" + type + " value " + value + ";"
        
        if(qid==-1):
            self.QueryLog.append(["value", type, value, self.QueryIdGenerator])
            self.QueryIdGenerator += 1
        else:
            self.QueryLog.append(["value", type, value, qid])
        
        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        return self.QueryLog[-1][-1]

    def regex(self, type: str, regex: str, qid: int=-1):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += '\n\tregex "' + regex + '";'
        else:
            self.context = type
            self.schema += "\n" + type + ' regex "' + regex + '";'
        
        if(qid==-1):
            self.QueryLog.append(["regex", type, regex, self.QueryIdGenerator])
            self.QueryIdGenerator += 1
        else:
            self.QueryLog.append(["regex", type, regex, qid])
            
        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        return self.QueryLog[-1][-1]

    def key(self, type: str, attribute: str, qid: int=-1):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\towns " + attribute + " @key;"
        else:
            self.context = type
            self.schema += "\n" + type + " owns " + attribute + " @key;"
        
        if(qid==-1):
            self.QueryLog.append(["key", type, attribute, self.QueryIdGenerator])
            self.QueryIdGenerator += 1
        else:
            self.QueryLog.append(["key", type, attribute, qid])
        
        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        return self.QueryLog[-1][-1]

    def unique(self, type: str, attribute: str, qid: int=-1):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\towns " + attribute + " @unique;"
        else:
            self.context = type
            self.schema += "\n" + type + " owns " + attribute + " @unique;"
            
        if(qid==-1):
            self.QueryLog.append(["unique", type, attribute, self.QueryIdGenerator])
            self.QueryIdGenerator += 1
        else:
            self.QueryLog.append(["unique", type, attribute, qid])

        checker = exceptions (
            schema=self.schema, QueryLog=self.QueryLog, types=self.types
        )
        checker.test()
        return self.QueryLog[-1][-1]

    # idea for remove recontrust schema after negating some queries using query ids and reconstructing schema
    def makeQuery(self, query: list):
        if query[0] == "abstract":
            self.abstract(query[1])
        elif query[0] == "sub":
            self.sub(query[1], query[2])
        elif query[0] == "owns":
            self.owns(query[1], query[2])
        elif query[0] == "ownsAs":
            self.ownsAs(query[1], query[2], query[3])
        elif query[0] == "relates":
            self.relates(query[1], query[2])
        elif query[0] == "relatesAs":
            self.relatesAs(query[1], query[2], query[3])
        elif query[0] == "plays":
            self.plays(query[1], query[2], query[3])
        elif query[0] == "playsAs":
            self.playsAs(query[1], query[2], query[3])
        elif query[0] == "value":
            self.value(query[1], query[2])
        elif query[0] == "regex":
            self.regex(query[1], query[2])
        elif query[0] == "key":
            self.key(query[1], query[2])
        elif query[0] == "unique":
            self.unique(query[1], query[2])

    def remove(self, q_ids: list):
        n = len(self.QueryLog)
        self.schema = "define"
        for i in range(0, n):
            query = self.QueryLog[0]
            self.QueryLog.popleft()
            if query[-1] in q_ids:
                continue
            self.makeQuery(query)

    def printQueryLog(self):
        for q in self.QueryLog:
            print(q)
