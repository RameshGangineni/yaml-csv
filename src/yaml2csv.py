import pandas as pd
import yaml
from yaml.constructor import ConstructorError


def no_duplicates_constructor(loader, node, deep=False):
    """Check for duplicate keys."""

    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        value = loader.construct_object(value_node, deep=deep)
        if key in mapping:
            raise ConstructorError("while constructing a mapping", node.start_mark,
                                   "found duplicate key (%s)" % key, key_node.start_mark)
        mapping[key] = value

    return loader.construct_mapping(node, deep)


yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, no_duplicates_constructor)

files = ['../data/sample.yaml','../data/example.yaml']
for file in files:
    print(file)
    if file.endswith(".yaml"):
        print("Converting Yaml {} to CSV".format(file))
        with open(file, 'r') as f:
            try:
                data_yaml = yaml.load(f)
            except yaml.YAMLError as exc:
                print("\n")
                print("Error validating: {0}".format(file))
                print("\n")
                print(exc)
                print("\n")
                answer = input("Would you like to continue? yes or no?").lower()
                if answer == 'no':
                    exit(1)
                else:
                    continue
            df = pd.io.json.json_normalize(data_yaml)
            df = df.replace(r'\n',' ', regex=True)
            df = df.replace(r' +', ' ',  regex=True)
            csv_file_path=file.replace("yaml", "csv")

        df.to_csv(csv_file_path,index=False)
