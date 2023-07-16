import unittest


class SimpleGeneratorTestCase(unittest.TestCase):
    pass

# does all schema objects contain tag, required and description fields (must have fields)
# creating a schema creates the associated file with correct file name
# schema contains only the message key at the top level
# schema returns expected output
# string json comes out with string type
# integer json comes out with integer type
# all string array comes out with Enum  type
# non all string array comes out as array.
# empty json returns empty schema
# json with no "message" key returns empty schema
# invalid json throws error
# invalid file throws error
# can must provide only one of file_path, json_string, and json_object


class SimpleTestSuite(unittest.TestSuite):
    pass

class GesonTestSuite(unittest.TestSuite):
    pass 