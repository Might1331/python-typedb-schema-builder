# python-typedb-schema-builder
typedb schema builder package for linkml

How to test the builder out:
1. Unzip the file 
2. Run

   ``` python -m venv .venv ```
   
   ``` .\.venv\Scripts\activate ```
4. Write the queries inside the main.py file and run to print schema.

   
Functions offered:

*get_schema():
Returns schema string and prints schema string.

*abstract(type: str):
Makes type abstract. Returns qid attached to the query.

*sub(subtype: str, type: str):
Create a new type given as argument "subtype" with supertype given as argument "type". Returns qid attached to the query.

*owns(type: str, owns: str):
Assigns ownership of attribute given as argument "owns" to type given as argument "type". Returns qid attached to the query.

*owns_as(type: str, to_own: str, from_own: str):
Assigns ownership of attribute given as argument "from_own" to alias given as argument "to_own" to type given as argument "type". Returns qid attached to the query.

*relates(type: str, role: str):
Adds a role given as argument "role" to a relationship type given as argument "type". Returns qid attached to the query.

*relates_as(type: str, to_role: str, from_role: str):
Adds a role given as argument "from_role" to an alias given as argument "to_role" to type given as argument "type". Returns qid attached to the query.

*plays(type: str, relation: str, role: str):
Assigns the relation:role, where relation is given as argument "relation" and role is given as argument "role" to the type given as argument "type". Returns qid attached to the query.

*plays_as(type: str, relation: str, to_role: str, from_role: str):
Assigns the relation:role, where relation is given as argument "relation" and role is given as argument "from_role" to alias given as "to_role" to the type given as argument "type". Returns qid attached to the query.

*value(type: str, value: str):
Specifies the value given as argument "value" to attribute type given as argument "type". Returns qid attached to the query.

*regex(type: str, regex: str):
Adds a regex pattern given as argument "regex" to attribute type given as argument "type". Returns qid attached to the query.

*key(type: str, attribute: str):
Makes the attribute given as atrgument "attribute" that is owned by type given as argument "type" a @key attribute.

*unique(self, type: str, attribute: str):
Makes the attribute given as atrgument "attribute" that is owned by type given as argument "type" a @unique attribute. Returns qid attached to the query.

*print_query_log():
Prints all the query IDs attached to every query.

*remove(q_ids: list):
Removes all the queries given in list argument "q_ids". And re-renders the remaining queries.
