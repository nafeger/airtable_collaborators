import posixpath
from typing import Dict, List

from pyairtable import Api, Table
from pyairtable.metadata import get_api_bases
from pyairtable.formulas import match

from Schema import Schema


class Populator:
    base_id: str = None
    airtable_api: Api = None
    base_table: Table = None


    def __init__(self, base_id: str, airtable_api_key: str):
        self.base_id = base_id
        self.airtable_api = Api(api_key=airtable_api_key)
        self.base_table = Table(api_key=airtable_api_key, base_id=self.base_id, table_name=Schema.BASES_TABLE_NAME)

    def upsert(self, table: Table, column_name: str, column_value: str, data):
        found = table.all(formula=match({column_name: column_value}))
        if found:
            table.update(record_id=found[0]['id'], fields=data)
        else:
            data[column_name] = column_value
            table.create(fields=data)

    def load_bases(self):
        bases = get_api_bases(self.airtable_api)
        for b in bases['bases']:
            id = b['id']
            name = b['name']
            self.upsert(table=self.base_table, column_name='Id', column_value=id, data={'Name': name})

    def populate(self):
        bases = self.load_bases()

        # TODO finish this method.
        return -1

    def clear(self):
        records = True
        while records:
            records = self.base_table.all(max_records=1000)
            ids = [d['id'] for d in records]
            self.base_table.batch_delete(ids)
