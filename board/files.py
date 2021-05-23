import yaml


def read_yaml(path: str) -> dict:
    with open(path) as file:
        output = yaml.load(file, Loader=yaml.FullLoader)
    return output
