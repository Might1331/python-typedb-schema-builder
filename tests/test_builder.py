import unittest
from typedbSchemaBuilder import builder

class TestBuilder(unittest.TestCase):

    def setUp(self):
        self.builder_instance = builder.Builder()

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


if __name__ == '__main__':
    unittest.main()