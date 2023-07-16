# Json-Schema-Gen
A command line tool for generating json schema.

## dependencies
This project depends on the python [genson](https://pypi.org/project/genson) package  

The genson package is used for intermediate steps in the schema generation pipeline
After which various transformations are performed on its output to generate the desired schema

## Setup
To setup run 
```sh
pip install -r requirements.txt
```

## Usage
To use run 
```sh
python main.py <path to file>
```

## Testing
This project makes use of the unittests library for testing  
To run the tests run
```sh
python tests.py
```


## Author
[Osakpolor T. Obaseki](obasekiosa.github.io)
