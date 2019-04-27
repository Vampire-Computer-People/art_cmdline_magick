import yaml


def get_data():
    with open('scripts/values.yml', 'r') as stream:
        return yaml.safe_load(stream)
