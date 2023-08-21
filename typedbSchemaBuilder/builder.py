from collections import deque
from .my_type import MyType
from .exceptions import TypeQLExceptions

class builder:
    def __init__(self) -> None:
        self._schema = "define"
        self._context = "?#"
        self._query_log = deque()
        self._query_id_generator = 1
        self._types = {
            "attribute": MyType("attribute"),
            "entity": MyType("entity"),
            "relation": MyType("relation")
        }
        self._types["attribute"].add_super_type("thing")
        self._types["entity"].add_super_type("thing")
        self._types["relation"].add_super_type("thing")

    def get_schema(self):
        checker = TypeQLExceptions(
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        escaped_string = r"" + self._schema
        decoded_string = bytes(escaped_string, "utf-8").decode("unicode_escape")
        print(decoded_string)
        return decoded_string

    def abstract(self, type: str, qid: int=-1):
        if self._context == type:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n\tabstract;"
        else:
            self._context = type
            self._schema += "\n" + type + " abstract;"

        if type not in self._types.keys():
            self._types[type] = MyType(type)
        self._types[type].abstract = True
        
        if(qid==-1):
            self._query_log.append(["abstract", type, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["abstract", type, qid])
            
        checker = TypeQLExceptions (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def sub(self, subtype: str, type: str, qid: int=-1):
        self._context = subtype
        self._schema += "\n" + subtype + " sub " + type + ";"

        if subtype not in self._types.keys():
            self._types[subtype] = MyType(subtype)
        self._types[subtype].add_super_type(type)
        
        if(qid==-1):
            self._query_log.append(["sub", subtype, type, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["sub", subtype, type, qid])
            
        checker = TypeQLExceptions (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def owns(self, type: str, owns: str, qid: int=-1):
        if self._context == type:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n\towns " + owns + ";"
        else:
            self._context = type
            self._schema += "\n" + type + " owns " + owns + ";"

        if type not in self._types.keys():
            self._types[type] = MyType(type)
        self._types[type].add_attribute(owns)
        
        if(qid==-1):
            self._query_log.append(["owns", type, owns, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["owns", type, owns, qid])
            
        checker = TypeQLExceptions (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def own_as(self, type: str, to_own: str, from_own: str, qid: int=-1):
        if self._context == type:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n\towns " + to_own + " as " + from_own + ";"
        else:
            self._context = type
            self._schema += "\n" + type + " owns " + to_own + " as " + from_own + ";"

        if type not in self._types.keys():
            self._types[type] = MyType(type)
        self._types[type].add_attribute(to_own)
        
        if(qid==-1):
            self._query_log.append( ["own_as", type, to_own, from_own, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append( ["own_as", type, to_own, from_own, qid])
            
        checker = TypeQLExceptions (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def relates(self, type: str, role: str, qid: int=-1):
        if self._context == type:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n\trelates " + role + ";"
        else:
            self._context = type
            self._schema += "\n" + type + " relates " + role + ";"

        if(qid==-1):
            self._query_log.append(["relates", type, role, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["relates", type, role, qid])
            
        checker = TypeQLExceptions (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def relatesAs(self, type, toRole: str, fromRole: str, qid: int=-1):
        if self._context == type:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n\towns " + toRole + " as " + fromRole + ";"
        else:
            self._context = type
            self._schema += (
                "\n" + type + " relates " + toRole + " as " + fromRole + ";"
            )
        
        if(qid==-1):
            self._query_log.append( ["relatesAs", type, toRole, fromRole, self._query_id_generator] )
            self._query_id_generator += 1
        else:
            self._query_log.append( ["relatesAs", type, toRole, fromRole, qid] )
            
        checker = TypeQLExceptions (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def plays(self, type: str, relation: str, role: str, qid: int=-1):
        if self._context == type:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n\tplays " + relation + ":" + role + ";"
        else:
            self._context = type
            self._schema += "\n" + type + " plays " + relation + ":" + role + ";"

        if type not in self._types.keys():
            self._types[type] = MyType(type)
        self._types[type].AddRole(relation, role)
        
        if(qid==-1):
            self._query_log.append(["plays", type, relation, role, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["plays", type, relation, role, qid])
            
        checker = TypeQLExceptions (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def plays_as(self, type: str, relation: str, toRole: str, fromRole: str, qid: int=-1):
        if self._context == type:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += (
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
            self._context = type
            self._schema += (
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

        if type not in self._types.keys():
            self._types[type] = MyType(type)
        self._types[type].AddRole(relation, toRole)
        
        if(qid==-1):
            self._query_log.append( ["plays_as", type, relation, toRole, fromRole, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append( ["plays_as", type, relation, toRole, fromRole, qid])

        checker = TypeQLExceptions (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def value(self, type: str, value: str, qid: int=-1):
        if self._context == type:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n\tvalue " + value + ";"
        else:
            self._context = type
            self._schema += "\n" + type + " value " + value + ";"
        
        if(qid==-1):
            self._query_log.append(["value", type, value, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["value", type, value, qid])
        
        checker = TypeQLExceptions (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def regex(self, type: str, regex: str, qid: int=-1):
        if self._context == type:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += '\n\tregex "' + regex + '";'
        else:
            self._context = type
            self._schema += "\n" + type + ' regex "' + regex + '";'
        
        if(qid==-1):
            self._query_log.append(["regex", type, regex, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["regex", type, regex, qid])
            
        checker = TypeQLExceptions (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def key(self, type: str, attribute: str, qid: int=-1):
        if self._context == type:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n\towns " + attribute + " @key;"
        else:
            self._context = type
            self._schema += "\n" + type + " owns " + attribute + " @key;"
        
        if(qid==-1):
            self._query_log.append(["key", type, attribute, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["key", type, attribute, qid])
        
        checker = TypeQLExceptions (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def unique(self, type: str, attribute: str, qid: int=-1):
        if self._context == type:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n\towns " + attribute + " @unique;"
        else:
            self._context = type
            self._schema += "\n" + type + " owns " + attribute + " @unique;"
            
        if(qid==-1):
            self._query_log.append(["unique", type, attribute, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["unique", type, attribute, qid])

        checker = TypeQLExceptions (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    # idea for remove recontrust schema after negating some queries using query ids and reconstructing schema
    def make_query(self, query: list):
            query_type = query[0]
            method_name = query_type.replace("_", "")
            getattr(self, method_name)(*query[1:])

    def remove(self, q_ids: list):
        n = len(self._query_log)
        self._schema = "define"
        for i in range(0, n):
            query = self._query_log[0]
            self._query_log.popleft()
            if query[-1] in q_ids:
                continue
            self.make_query(query)

    def print_query_log(self):
        for q in self._query_log:
            print(q)