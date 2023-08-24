from collections import deque
from .Type import Type
from .Exceptions import SchemaChecker

class Builder:
    def __init__(self) -> None:
        self._schema = "define"
        self._context = "?#"
        self._query_log = deque()
        self._query_id_generator = 1
        self._types = {
            "attribute": Type("attribute"),
            "entity": Type("entity"),
            "relation": Type("relation")
        }
        self._types["attribute"].add_super_type("thing")
        self._types["entity"].add_super_type("thing")
        self._types["relation"].add_super_type("thing")

    def get_schema(self):
        escaped_string = r"" + self._schema
        decoded_string = bytes(escaped_string, "utf-8").decode("unicode_escape")
        print(decoded_string)
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return decoded_string

    def abstract(self, type_: str, qid: int=-1):
        if self._context == type_:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n    abstract;"
        else:
            self._context = type_
            self._schema += "\n" + type_ + " abstract;"

        
        if(qid==-1):
            self._query_log.append(["abstract", type_, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["abstract", type_, qid])
            
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        self._types[type_].abstract = True
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def sub(self, subtype: str, type_: str, qid: int=-1):
        self._context = subtype
        self._schema += "\n" + subtype + " sub " + type_ + ";"

        if(qid==-1):
            self._query_log.append(["sub", subtype, type_, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["sub", subtype, type_, qid])
            
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        self._types[subtype] = Type(subtype)
        self._types[subtype].add_super_type(type_)            
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        
        return self._query_log[-1][-1]

    def owns(self, type_: str, owns: str, qid: int=-1):
        if self._context == type_:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n    owns " + owns + ";"
        else:
            self._context = type_
            self._schema += "\n" + type_ + " owns " + owns + ";"


        if(qid==-1):
            self._query_log.append(["owns", type_, owns, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["owns", type_, owns, qid])

        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        self._types[type_].add_attribute(owns)
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def own_as(self, type_: str, to_own: str, from_own: str, qid: int=-1):
        if self._context == type_:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n    owns " + to_own + " as " + from_own + ";"
        else:
            self._context = type_
            self._schema += "\n" + type_ + " owns " + to_own + " as " + from_own + ";"
        
        if(qid==-1):
            self._query_log.append( ["own_as", type_, to_own, from_own, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append( ["own_as", type_, to_own, from_own, qid])
        
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        self._types[type_].add_attribute(to_own)
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def relates(self, type_: str, role: str, qid: int=-1):
        if self._context == type_:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n    relates " + role + ";"
        else:
            self._context = type_
            self._schema += "\n" + type_ + " relates " + role + ";"

        if(qid==-1):
            self._query_log.append(["relates", type_, role, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["relates", type_, role, qid])
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        self._types[type_].add_relation_roles(role)
        return self._query_log[-1][-1]

    def relates_as(self, type_, to_role: str, from_role: str, qid: int=-1):
        if self._context == type_:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n    owns " + to_role + " as " + from_role + ";"
        else:
            self._context = type_
            self._schema += (
                "\n" + type_ + " relates " + to_role + " as " + from_role + ";"
            )
        
        if(qid==-1):
            self._query_log.append( ["relates_as", type_, to_role, from_role, self._query_id_generator] )
            self._query_id_generator += 1
        else:
            self._query_log.append( ["relates_as", type_, to_role, from_role, qid] )
        
        self._types[type_].add_relation_roles(from_role)
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def plays(self, type_: str, relation: str, role: str, qid: int=-1):
        if self._context == type_:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n    plays " + relation + ":" + role + ";"
        else:
            self._context = type_
            self._schema += "\n" + type_ + " plays " + relation + ":" + role + ";"
        
        if(qid==-1):
            self._query_log.append(["plays", type_, relation, role, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["plays", type_, relation, role, qid])
        
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        self._types[type_].add_role(relation, role)
        return self._query_log[-1][-1]

    def plays_as(self, type_: str, relation: str, to_role: str, from_role: str, qid: int=-1):
        if self._context == type_:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += (
                "\n    plays "
                + relation
                + ":"
                + to_role
                + " as "
                + relation
                + ":"
                + from_role
                + ";"
            )
        else:
            self._context = type_
            self._schema += (
                "\n"
                + type_
                + " plays "
                + relation
                + ":"
                + to_role
                + " as "
                + relation
                + ":"
                + from_role
                + ";"
            )

        
        if(qid==-1):
            self._query_log.append( ["plays_as", type_, relation, to_role, from_role, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append( ["plays_as", type_, relation, to_role, from_role, qid])
        
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        self._types[type_].add_role(relation, to_role)
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def value(self, type_: str, value: str, qid: int=-1): 
        if self._context == type_:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n    value " + value + ";"
        else:
            self._context = type_
            self._schema += "\n" + type_ + " value " + value + ";"
        
        if(qid==-1):
            self._query_log.append(["value", type_, value, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["value", type_, value, qid]) 
        
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def regex(self, type_: str, regex: str, qid: int=-1): 
        if self._context == type_:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += '\n    regex "' + regex + '";'
        else:
            self._context = type_
            self._schema += "\n" + type_ + ' regex "' + regex + '";'
        
        if(qid==-1):
            self._query_log.append(["regex", type_, regex, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["regex", type_, regex, qid])
        
        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )            
        checker.test()
        return self._query_log[-1][-1]

    def key(self, type_: str, attribute: str, qid: int=-1): 
        if self._context == type_:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n    owns " + attribute + " @key;"
        else:
            self._context = type_
            self._schema += "\n" + type_ + " owns " + attribute + " @key;"
        
        if(qid==-1):
            self._query_log.append(["key", type_, attribute, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["key", type_, attribute, qid]) 

        checker = SchemaChecker (
            schema=self._schema, query_log=self._query_log, types_=self._types
        )
        checker.test()
        return self._query_log[-1][-1]

    def unique(self, type_: str, attribute: str, qid: int=-1): 
        if self._context == type_:
            if self._schema[-1] == ";":
                self._schema = self._schema[:-1] + ","
            self._schema += "\n    owns " + attribute + " @unique;"
        else:
            self._context = type_
            self._schema += "\n" + type_ + " owns " + attribute + " @unique;"
            
        if(qid==-1):
            self._query_log.append(["unique", type_, attribute, self._query_id_generator])
            self._query_id_generator += 1
        else:
            self._query_log.append(["unique", type_, attribute, qid])

        checker = SchemaChecker (
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