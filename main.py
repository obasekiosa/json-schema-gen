from abc import abstractmethod
from genson import SchemaBuilder
import json

class InvalidParameterError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class JSONSchemaGenerator:

    def __init__(self, **kwargs) -> None:
        file_path = kwargs.get("file_path", None)
        json_object = kwargs.get("json_object", None)
        json_string = kwargs.get("json_string", None)

        opts = [file_path, json_object, json_string]
        set_opts = list(filter(lambda x: x is not None, opts))

        if len(set_opts) > 1:
            raise InvalidParameterError("only one of file_path and json_object parameters should be set")
        
        if len(set_opts) == 0:
            raise InvalidParameterError("at least one of file_path or json_object parameters should be set")
        
        self.file_path = file_path
        self.json_object = json_object or (json_string and json.loads(json_string))
        self.json_string = json_string

        if self.file_path is not None:
            with open(self.file_path, "r") as file:
                self.json_object = json.load(file)
    
    @abstractmethod
    def generate_schema(self):
        raise NotImplementedError("This method hasn't been implemented yet")
    

class SimpleSchemaGenerator(JSONSchemaGenerator):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # perfom generation here


class GensonSchemaGenerator(JSONSchemaGenerator, SchemaBuilder):

    def __init__(self, **kwargs) -> None:
        JSONSchemaGenerator.__init__(self, **kwargs)
        SchemaBuilder.__init__(self)
        # perfom generation here


if __name__ == "__main__":
    gen = GensonSchemaGenerator(file_path="data/data_1.json")
    simple = SimpleSchemaGenerator(file_path="data/data_2.json")

    print(gen.json_object)
    print(simple.json_object)