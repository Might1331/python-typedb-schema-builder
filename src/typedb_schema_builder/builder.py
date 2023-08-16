from collections import deque
from .my_type import my_type
from .exceptions import exceptions

class builder:
    schema = ""
    context = "?#"
    query_log = deque()
    query_id_generator = 1
    types = {}

    def __init__(self) -> None:
        self.schema = "define"
        self.query_id_generator = 1
        self.types["attribute"] = my_type("attribute")
        self.types["attribute"].add_super_type("thing")
        self.types["entity"] = my_type("entity")
        self.types["entity"].add_super_type("thing")
        self.types["relation"] = my_type("relation")
        self.types["relation"].add_super_type("thing")

    def get_schema(self):
        checker = exceptions (
            schema=self.schema, query_log=self.query_log, types=self.types
        )
        checker.test()
        escaped_string = r"" + self.schema
        decoded_string = bytes(escaped_string, "utf-8").decode("unicode_escape")
        print(decoded_string)
        return decoded_string

    def abstract(self, type: str):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\tabstract;"
        else:
            self.context = type
            self.schema += "\n" + type + " abstract;"

        if type not in self.types.keys():
            self.types[type] = my_type(type)
        self.types[type].abstract = True
        self.query_log.append(["abstract", type, self.query_id_generator])
        self.query_id_generator += 1
        return self.query_id_generator - 1

    def sub(self, subtype: str, type: str):
        self.context = subtype
        self.schema += "\n" + subtype + " sub " + type + ";"

        if subtype not in self.types.keys():
            self.types[subtype] = my_type(subtype)
        self.types[subtype].add_super_type(type)
        self.query_log.append(["sub", subtype, type, self.query_id_generator])
        self.query_id_generator += 1
        return self.query_id_generator - 1

    def owns(self, type: str, owns: str):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\towns " + owns + ";"
        else:
            self.context = type
            self.schema += "\n" + type + " owns " + owns + ";"

        if type not in self.types.keys():
            self.types[type] = my_type(type)
        self.types[type].add_attribute(owns)
        self.query_log.append(["owns", type, owns, self.query_id_generator])
        self.query_id_generator += 1
        return self.query_id_generator - 1

    def owns_as(self, type: str, to_own: str, from_own: str):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\towns " + to_own + " as " + from_own + ";"
        else:
            self.context = type
            self.schema += "\n" + type + " owns " + to_own + " as " + from_own + ";"

        if type not in self.types.keys():
            self.types[type] = my_type(type)
        self.types[type].add_attribute(to_own)
        self.query_log.append(
            ["owns_as", type, to_own, from_own, self.query_id_generator]
        )
        self.query_id_generator += 1
        return self.query_id_generator - 1

    def relates(self, type: str, role: str):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\trelates " + role + ";"
        else:
            self.context = type
            self.schema += "\n" + type + " relates " + role + ";"

        self.query_log.append(["relates", type, role, self.query_id_generator])
        self.query_id_generator += 1
        return self.query_id_generator - 1

    def relates_as(self, type, to_role: str, from_role: str):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\towns " + to_role + " as " + from_role + ";"
        else:
            self.context = type
            self.schema += (
                "\n" + type + " relates " + to_role + " as " + from_role + ";"
            )
        self.query_log.append(
            ["relates_as", type, to_role, from_role, self.query_id_generator]
        )
        self.query_id_generator += 1
        return self.query_id_generator - 1

    def plays(self, type: str, relation: str, role: str):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\tplays " + relation + ":" + role + ";"
        else:
            self.context = type
            self.schema += "\n" + type + " plays " + relation + ":" + role + ";"

        if type not in self.types.keys():
            self.types[type] = my_type(type)
        self.types[type].add_role(relation, role)
        self.query_log.append(["plays", type, relation, role, self.query_id_generator])
        self.query_id_generator += 1
        return self.query_id_generator - 1

    def plays_as(self, type: str, relation: str, to_role: str, from_role: str):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += (
                "\n\tplays "
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
            self.context = type
            self.schema += (
                "\n"
                + type
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

        if type not in self.types.keys():
            self.types[type] = my_type(type)
        self.types[type].add_role(relation, to_role)
        self.query_log.append(
            ["plays_as", type, relation, to_role, from_role, self.query_id_generator]
        )
        self.query_id_generator += 1
        return self.query_id_generator - 1

    def value(self, type: str, value: str):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\tvalue " + value + ";"
        else:
            self.context = type
            self.schema += "\n" + type + " value " + value + ";"
        self.query_log.append(["value", type, value, self.query_id_generator])
        self.query_id_generator += 1
        return self.query_id_generator - 1

    def regex(self, type: str, regex: str):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += '\n\tregex "' + regex + '";'
        else:
            self.context = type
            self.schema += "\n" + type + ' regex "' + regex + '";'
        self.query_log.append(["regex", type, regex, self.query_id_generator])
        self.query_id_generator += 1
        return self.query_id_generator - 1

    def key(self, type: str, attribute: str):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\towns " + attribute + " @key;"
        else:
            self.context = type
            self.schema += "\n" + type + " owns " + attribute + " @key;"
        self.query_log.append(["key", type, attribute, self.query_id_generator])
        self.query_id_generator += 1
        return self.query_id_generator - 1

    def unique(self, type: str, attribute: str):
        if self.context == type:
            if self.schema[-1] == ";":
                self.schema = self.schema[:-1] + ","
            self.schema += "\n\towns " + attribute + " @unique;"
        else:
            self.context = type
            self.schema += "\n" + type + " owns " + attribute + " @unique;"
        self.query_log.append(["unique", type, attribute, self.query_id_generator])
        self.query_id_generator += 1
        return self.query_id_generator - 1

    # idea for remove recontrust schema after negating some queries using query ids and reconstructing schema
    def make_query(self, query: list):
        if query[0] == "abstract":
            self.abstract(query[1])
        elif query[0] == "sub":
            self.sub(query[1], query[2])
        elif query[0] == "owns":
            self.owns(query[1], query[2])
        elif query[0] == "owns_as":
            self.owns_as(query[1], query[2], query[3])
        elif query[0] == "relates":
            self.relates(query[1], query[2])
        elif query[0] == "relates_as":
            self.relates_as(query[1], query[2], query[3])
        elif query[0] == "plays":
            self.plays(query[1], query[2], query[3])
        elif query[0] == "plays_as":
            self.plays_as(query[1], query[2], query[3])
        elif query[0] == "value":
            self.value(query[1], query[2])
        elif query[0] == "regex":
            self.regex(query[1], query[2])
        elif query[0] == "key":
            self.key(query[1], query[2])
        elif query[0] == "unique":
            self.unique(query[1], query[2])

    def remove(self, q_ids: list):
        n = len(self.query_log)
        self.schema = "define"
        for i in range(0, n):
            query = self.query_log[0]
            self.query_log.popleft()
            if query[-1] in q_ids:
                continue
            self.make_query(query)

    def print_query_log(self):
        for q in self.query_log:
            print(q)
