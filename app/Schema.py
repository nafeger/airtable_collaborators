import argparse
from typing import Dict

from pyairtable import Api
from pyairtable import Base, Table
from pyairtable.metadata import get_base_schema, get_api_bases, get_table_schema


class Schema:
    """
    This class will check to see if the schema columns are the expected ones.
    In the future this should be used to create the schema if it doesn't exist.
    """
    base_id: str = None
    airtable_api: Api = None
    exit_code: int = 0

    schema: Dict = {
        'Bases': {
            'Id': 'singleLineText',
            'Name': 'singleLineText',
            'Update Date': 'lastModifiedTime',
            'Users-to-base': 'multipleRecordLinks'
        },
        'Users': {
            'Id': 'singleLineText',
            'Users-to-base': 'singleLineText',
            'Workspace Permissions': '',
            'Workspace Grant Date': '',
            'Base Permissions': '',
            'Email': '',
            'Base Names': '',
        },
        'Users-to-Base': {
            'User Base': '',
            'Base': '',
            'Access Type': '',
            'User': '',
            'Update Date': '',
            'Base Name': '',
            'User Email': '',
        }

    }

    def __init__(self, base_id: str, airtable_api_key: str):
        self.base_id = base_id
        self.airtable_api = airtable_api_key

    def validate(self):
        base = Base(api_key=self.airtable_api, base_id=self.base_id)

        schema = get_base_schema(base=base)
        for tuples in schema.items():
            # print()
            tables = tuples[1]
            for t in tables:
                # print(t)
                if t['name'] not in self.schema:
                    print("Unexpected table found: {}".format(t['name']))
                    self.exit_code |= -1
                    continue
                target_columns = self.schema[t['name']].keys()
                for f in t['fields']:
                    # print(f)
                    if f['name'] not in target_columns:
                        print(f"Unexpected column: {t['name']}({f['name']})")
                        self.exit_code |= -1
                # print("***")
        return self.exit_code


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--base_id", help="Airtable Base ID")
    parser.add_argument("-a", "--airtable_api_key", help="Airtable API Key")

    args = parser.parse_args()

    x = Schema(base_id=args.base_id, airtable_api_key=args.airtable_api_key)
    exit(x.validate())
