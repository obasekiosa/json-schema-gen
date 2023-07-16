import json
import pathlib

from abc import abstractmethod
from genson import SchemaBuilder

from config import BASE_DIR


class InvalidParameterError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class SchemaNotGeneratedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class JSONSchemaGenerator:
    """
    JSONSchemea generator base class
    """

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
        
        self._file_path = file_path
        self._json_object = json_object or (json_string and json.loads(json_string))
        self._json_string = json_string
        self._schema = None
        self._BASE_DIR = BASE_DIR

        if self._file_path is not None:
            with open(self._file_path, "rb") as file:
                self._json_object = json.load(file)
    
    def get_schema(self):
        return self._schema

    def save_schema(self, path=None):
        if self._schema is None:
            raise SchemaNotGeneratedError("schema has not been generated")

        file_name = self._file_path if self._file_path else "output"
        file_name = pathlib.PurePath(file_name).stem
        if path is None:
            path = self._BASE_DIR.joinpath("schema", f"schema_{file_name}.json")
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self._schema, file, indent=2)
    
    def __str__(self) -> str:
        return json.dumps(self._schema)


class GensonSchemaGenerator(JSONSchemaGenerator):
    """
    JSONSchemea generator that uses the genson package to generate a
    json schema. Also performs type compression and attribute modifications
    """

    def __init__(self, **kwargs) -> None:
        JSONSchemaGenerator.__init__(self, **kwargs)

        self._builder = SchemaBuilder(schema_uri=None)
        self._schema = None
        self._build_schema()

    def _build_schema(self):
        json_obj = json.loads(json.dumps(self._json_object)) # deep copy
        if isinstance(json_obj, dict):
            keys = list(json_obj.keys())
            for k in keys:
                if k != "message":
                    json_obj.pop(k)

        json_obj = json_obj.get("message", None)
        if json_obj is None:
            self._schema = dict()
        else:
            self._builder.add_object(json_obj)
            self._schema = self._builder.to_schema()
            self._update_meta(self._schema)
            self._compress_type_meta(self._schema)
            self._restructure_meta(self._schema)
    
    def _update_value(self, v):
        if isinstance(v, dict) and v.get("type", False):
            v['required'] = False
            v["description"] = ""
            v["tag"] = ""
        
    def _update_meta(self, schema):
        values = None
        if isinstance(schema, dict):
            values = list(schema.values())
            self._update_value(schema)
        elif isinstance(schema, list):
            values = schema
        else:
            return

        for v in values:
                self._update_meta(v)

    def _compress(self, value):
        if isinstance(value, dict):
            items = value.get("items", None)
            if value.get("type") == "array" and items is not None \
                  and items.get("type", None) == "string":
                
                value["type"] = "enum"

    def _compress_type_meta(self, schema):
        if isinstance(schema, dict):
            values = list(schema.values())
            self._compress(schema)
            for v in values:
                self._compress_type_meta(v)
        elif isinstance(schema, list):
            for v in schema:
                self._compress_type_meta(v)
        else:
            return


    def _restructure_meta(self, schema):
        if isinstance(schema, dict):
            self._restructure(schema)
            values = list(schema.values())
            for v in values:
                self._restructure_meta(v)
        elif isinstance(schema, list):
            for v in schema:
                self._restructure_meta(v)
        else:
            return

    def _restructure(self, value):
        if isinstance(value, dict):
            props = value.get("properties", None)
            if props is not None:
                for k, v in props.items():
                    value[k] = v
                value.pop("properties")