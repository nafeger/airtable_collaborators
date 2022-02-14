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
    users_table: Table = None
    workspace_id: str = None

    def __init__(self, base_id: str, airtable_api_key: str, workspace_id: str):
        self.base_id = base_id
        self.airtable_api = Api(api_key=airtable_api_key)
        self.base_table = Table(api_key=airtable_api_key, base_id=self.base_id, table_name=Schema.BASES_TABLE_NAME)
        self.users_table = Table(api_key=airtable_api_key, base_id=self.base_id, table_name=Schema.USERS_TABLE_NAME)
        self.users_to_base_table = Table(api_key=airtable_api_key, base_id=self.base_id,
                                         table_name=Schema.USERSTOBASES_TABLE_NAME)
        self.workspace_id = workspace_id

        if not self.workspace_id:
            raise Exception("Workspace ID is required")

    def upsert(self, table: Table, column_name: str, column_value: str, data: Dict):
        found = table.all(formula=match({column_name: column_value}))
        if found:
            table.update(record_id=found[0]['id'], fields=data)
        else:
            data[column_name] = column_value
            table.create(fields=data)

    def populate_bases(self):
        bases = get_api_bases(self.airtable_api)
        for b in bases['bases']:
            base_id = b['id']
            base_name = b['name']
            self.upsert(table=self.base_table, column_name='Id', column_value=base_id, data={'Name': base_name})

    def populate(self):
        self.populate_bases()

        e = self.workspaces(workspace_id=self.workspace_id)
        self.populate_workspace_collaborators(collaborators=e['collaborators']['workspaceCollaborators'])

        self.populate_base_collaborators(base_collaborators=e['collaborators']['baseCollaborators'])

        # TODO finish this method.
        return -1

    def clear(self):
        records = True
        while records:
            records = self.base_table.all(max_records=1000)
            ids = [d['id'] for d in records]
            self.base_table.batch_delete(ids)

    def workspaces(self, workspace_id):
        base_schema_url = posixpath.join(
            self.airtable_api.API_URL, "meta", "workspaces", workspace_id
        ) + "?include=collaborators"
        return self.airtable_api._request("get", base_schema_url)

    def populate_workspace_collaborators(self, collaborators):
        for u in collaborators:
            user_id = u['userId']
            email = u['email']
            permission_level = u['permissionLevel']
            self.upsert(table=self.users_table, column_name='Id', column_value=user_id, data={'Email': email,
                                                                                              'Workspace Permissions': permission_level,
                                                                                              'Workspace Grant Date': u[
                                                                                                  'createdTime']})

    def populate_base_collaborators(self, base_collaborators: List):
        for u in base_collaborators:
            user_id = u['userId']
            email = u['email']
            self.upsert(table=self.users_table, column_name='Id', column_value=user_id, data={'Email': email})

            base_id = u['baseId']
            base = self.base_table.first(formula=match({'Id': base_id}))
            if base is None:
                print(f"Unable to find base: {base_id}")
            base_record_key = base['id']
            user = self.users_table.first(formula=match({'Id': user_id}))
            if user is None:
                print(f"Unable to find user: {user_id}")
            user_record_key = user['id']
            permission_level = u['permissionLevel']
            user_base = f"{user_id}-{base_id}"
            self.upsert(table=self.users_to_base_table,
                        column_name='User Base',
                        column_value=user_base,
                        data={'Base': [base_record_key],
                              'User': [user_record_key],
                              'Access Type': permission_level
                              })
