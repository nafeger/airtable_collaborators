import argparse
from typing import Dict

from pyairtable import Api
from pyairtable import Base, Table
from pyairtable.metadata import get_base_schema, get_api_bases, get_table_schema


class Schema:
    """
    This class will check to see if the schema columns are the expected ones.
    In the future this should be used to create the schema if it doesn't exist.

    TODO:
    [ ] Install the missing columns?
    """
    base_id: str = None
    airtable_api: Api = None
    exit_code: int = 0

    BASES_TABLE_NAME: str = "Bases"
    USERS_TABLE_NAME: str = "Users"
    USERSTOBASES_TABLE_NAME: str = "Users-to-Bases"

    schema: Dict = {
        BASES_TABLE_NAME: {
            'Id': 'singleLineText',
            'Name': 'singleLineText',
            'Update Date': 'lastModifiedTime',
            'Users-to-base': 'multipleRecordLinks'
        },
        USERS_TABLE_NAME: {
            'Id': 'singleLineText',
            'Users-to-base': 'multipleRecordLinks',
            'Workspace Permissions': 'singleSelect',
            'Workspace Grant Date': 'dateTime',
            'Base Permissions': 'rollup',
            'Email': 'email',
            'Base Names': 'rollup',
        },
        USERSTOBASES_TABLE_NAME: {
            'User Base': 'singleLineText',
            'Base': 'multipleRecordLinks',
            'Access Type': 'singleSelect',
            'User': 'multipleRecordLinks',
            'Update Date': 'lastModifiedTime',
            'Base Name': 'multipleLookupValues',
            'User Email': 'multipleLookupValues',
            'Permission Description': '<formula>'
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
                    else:
                        column_type = f['type']
                        if column_type != self.schema[t['name']][f['name']]:
                            print("Found invalid column type: {}({}-<{}>)".format(t['name'], f['name'], column_type))
        return self.exit_code

