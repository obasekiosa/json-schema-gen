import unittest, pathlib, os, json

from config import BASE_DIR
from schem_gen import GensonSchemaGenerator



class GensonSchemaGeneratorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.file_name = "example.json"
        self.base_dir = "tests"
        self.file_path = pathlib.PurePath(self.base_dir, self.file_name)
        self.gen = GensonSchemaGenerator(file_path=self.file_path)
        self.gen.save_schema()
        self.schema = None
        self.original_json = None

        with open(pathlib.PurePath("schema", f"schema_{self.file_name}"), "r", encoding="utf8") as file:
            self.schema = json.load(file)

        with open(self.file_path, "r", encoding="utf8") as file:
            self.original_json = json.load(file)

        

    @classmethod
    def tearDownClass(self):
        os.remove(pathlib.PurePath("schema", f"schema_{self.file_name}"))

    def test_all_schema_key_contain_default_fields(self):
        self.assertTrue("type" in self.schema)
        self.assertTrue("required" in self.schema)
        self.assertTrue("description" in self.schema)
        self.assertTrue("tag" in self.schema)

    def test_schema_created_in_schema_dir(self):
        self.assertTrue(pathlib.Path(BASE_DIR, "schema", f"schema_{self.file_name}").exists())

    def test_only_message_attributes_are_returned(self):
        keys = self.original_json.get("message", dict()).keys()

        for k in keys:
            self.assertTrue(k in self.schema)
        
        self.assertEqual(len(keys), len(self.schema.keys()) - 4, "Schema should have the same number of keys as in the original object message attribute")
    

    def test_identify_string_type(self):
        schema_type = self.schema.get("key_str", {}).get("type", None)
        self.assertTrue( schema_type == "string")
    

    def test_identify_enum_type(self):
        schema_type = self.schema.get("key_enum", {}).get("type", None)
        self.assertTrue( schema_type == "enum")
    

    def test_identify_int_type(self):
        schema_type = self.schema.get("key_int", {}).get("type", None)
        self.assertTrue( schema_type == "integer")


    def test_identify_array_type(self):
        schema_type = self.schema.get("key_array", {}).get("type", None)
        self.assertTrue( schema_type == "array")
    

    


class GensonSchemaGeneratorEmptyInputTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.file_name = "empty_example.json"
        self.base_dir = "tests"
        self.file_path = pathlib.PurePath(self.base_dir, self.file_name)
        self.gen = GensonSchemaGenerator(file_path=self.file_path)
        self.gen.save_schema()
        self.schema = None
        self.original_json = None

        with open(pathlib.PurePath("schema", f"schema_{self.file_name}"), "r", encoding="utf8") as file:
            self.schema = json.load(file)

        with open(self.file_path, "r", encoding="utf8") as file:
            self.original_json = json.load(file)

        

    @classmethod
    def tearDownClass(self):
        os.remove(pathlib.PurePath("schema", f"schema_{self.file_name}"))

    def test_schema_created_in_schema_dir(self):
        self.assertTrue(pathlib.Path(BASE_DIR, "schema", f"schema_{self.file_name}").exists())

    def test_no_message_attribute_returns_empty_schema(self):
        self.assertTrue(len(self.schema.keys()) == 0, "absent message should generate empty schema")  
    
    


class GensonSchemaGeneratorComplexInputTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.file_name = "complex_example.json"
        self.base_dir = "tests"
        self.file_path = pathlib.PurePath(self.base_dir, self.file_name)
        self.gen = GensonSchemaGenerator(file_path=self.file_path)
        self.gen.save_schema()
        self.schema = None
        self.original_json = None

        with open(pathlib.PurePath("schema", f"schema_{self.file_name}"), "r", encoding="utf8") as file:
            self.schema = json.load(file)

        with open(self.file_path, "r", encoding="utf8") as file:
            self.original_json = json.load(file)

        

    @classmethod
    def tearDownClass(self):
        os.remove(pathlib.PurePath("schema", f"schema_{self.file_name}"))

    def test_schema_created_in_schema_dir(self):
        self.assertTrue(pathlib.Path(BASE_DIR, "schema", f"schema_{self.file_name}").exists())


    def test_complex_example_is_correct(self):
        expected = None
        with open(pathlib.Path(BASE_DIR, "schema", f"schema_{self.file_name}"), "r", encoding="utf8") as file:
            expected = json.load(file)

        self.assertEqual(self.schema, expected) 
    
    


## Misc Tests (TODO if necessary)
# schema returns expected output

if __name__ == "__main__":
    unittest.main()