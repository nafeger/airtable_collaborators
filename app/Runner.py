import argparse

from Schema import Schema
from Populator import Populator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--base_id", help="Airtable Base ID", required=True)
    parser.add_argument("-a", "--airtable_api_key", help="Airtable API Key", required=True)
    parser.add_argument("-c", "--clear_records", help="Clear Records", action='store_true')

    args = parser.parse_args()

    x = Schema(base_id=args.base_id, airtable_api_key=args.airtable_api_key)
    if x.validate() != 0:
        print("Error: Schema is not valid")
        exit(1)

    p = Populator(base_id=args.base_id, airtable_api_key=args.airtable_api_key)
    if args.clear_records:
        exit(p.clear())

    exit(p.populate())
