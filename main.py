import sys, pathlib
from schem_gen import GensonSchemaGenerator

def main():
    if len(sys.argv) != 2:
        print("Usage python main.py <path_to_file>")
        sys.exit(1)
    
    file_str = sys.argv[1]
    file_path = pathlib.Path(file_str)
    if not file_path.exists():
        print(f"file \"{file_path}\" does not exist")
        sys.exit(1)

    gen = GensonSchemaGenerator(file_path=file_path)
    gen.save_schema()
    print("Schema generated successfully")

if __name__ == "__main__":
    main()