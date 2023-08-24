import unittest
from typedbSchemaBuilder import Builder

class TestBuilder(unittest.TestCase):

    def setUp(self):
        self.builder_instance = Builder.Builder()

    def test_abstract(self):
        self.builder_instance.sub("brother","entity")
        self.builder_instance.abstract("brother")
        expected_output= 'define\n'+ 'brother sub entity,\n'+ '    abstract;'
        message = "Abstract method failed"
        
        # Add assertions to test the behavior of the abstract function
        self.assertEqual(self.builder_instance.get_schema(), expected_output, message)

    def test_sub(self):
        self.builder_instance.sub("sister", "entity")
        expected_output='define\n'+'sister sub entity;'
        message = "sub method failed"
        
        # Add assertions to test the behavior of the sub function
        self.assertEqual(self.builder_instance.get_schema(), expected_output, message)

    def test_owns(self):
        self.builder_instance.sub("name","attribute")
        self.builder_instance.sub("sister", "entity")
        self.builder_instance.owns("sister","name")
        expected_output='define\n'+'name sub attribute;\n'+'sister sub entity,\n'+'    owns name;'
        message = "owns method failed"
        
        # Add assertions to test the behavior of the owns function
        self.assertEqual(self.builder_instance.get_schema(), expected_output, message)

    def test_owns_as(self):
        self.builder_instance.sub("person","entity")
        self.builder_instance.own_as("person","nickname","name")
        self.builder_instance.sub("name","attribute")
        expected_output='define\n'+'person sub entity,\n'+'    owns nickname as name;\n'+'name sub attribute;'
        message = "owns method failed"
        
        # Add assertions to test the behavior of the owns function
        self.assertEqual(self.builder_instance.get_schema(), expected_output, message)

    def test_relates(self):
        pass        
# builder_instance.relates(type: str, role: str): Adds a role given as argument "role" to a relationship type given as argument "type". Returns qid attached to the query.

# builder_instance.relates_as(type: str, to_role: str, from_role: str): Adds a role given as argument "from_role" to an alias given as argument "to_role" to type given as argument "type". Returns qid attached to the query.

# builder_instance.plays(type: str, relation: str, role: str): Assigns the relation:role, where relation is given as argument "relation" and role is given as argument "role" to the type given as argument "type". Returns qid attached to the query.

# builder_instance.plays_as(type: str, relation: str, to_role: str, from_role: str): Assigns the relation:role, where relation is given as argument "relation" and role is given as argument "from_role" to alias given as "to_role" to the type given as argument "type". Returns qid attached to the query.

# builder_instance.value(type: str, value: str): Specifies the value given as argument "value" to attribute type given as argument "type". Returns qid attached to the query.

# builder_instance.regex(type: str, regex: str): Adds a regex pattern given as argument "regex" to attribute type given as argument "type". Returns qid attached to the query.

# builder_instance.key(type: str, attribute: str): Makes the attribute given as atrgument "attribute" that is owned by type given as argument "type" a @key attribute.

# builder_instance.unique(self, type: str, attribute: str): Makes the attribute given as atrgument "attribute" that is owned by type given as argument "type" a @unique attribute. Returns qid attached to the query.

# builder_instance.print_query_log(): Prints all the query IDs attached to every query.

# builder_instance.remove(q_ids: list): Removes all the queries given in list argument "q_ids". And re-renders the remaining queries.

if __name__ == '__main__':
    unittest.main()