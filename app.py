import json
import os
import uuid

from pathlib import Path

from flask import Flask, request, abort
from flask_rest4 import Api, Resource


DATA_FOLDER = "data"
if not os.path.isdir(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
ACCOUNTS_FILE = os.path.join("data", "accounts.json")
if not os.path.isfile(ACCOUNTS_FILE):
    Path(ACCOUNTS_FILE).touch()
RECORDS_FILE = os.path.join("data", "records.json")
if not os.path.isfile(RECORDS_FILE):
    Path(RECORDS_FILE).touch()

app = Flask(__name__)
api = Api(app)


@api.route("/accounts/<account_id>")
class Account(Resource):
    def list(self):
        return self._get_accounts()

    def create(self):
        data = request.json
        name = data["name"]

        accounts = self._get_accounts()
        if self._has_account(accounts, name):
            abort(403)
        new_account = {
            "id": str(uuid.uuid4()),
            "name": name
        }
        accounts.append(new_account)
        return self._save_accounts(accounts)

    def delete(self, account_id):
        accounts = self._get_accounts()
        accounts = self._delete_account(accounts, account_id)
        return self._save_accounts(accounts)

    def _get_accounts(self):
        with open(ACCOUNTS_FILE) as file:
            data = file.read()
            return json.loads(data) if data else []

    def _save_accounts(self, accounts):
        with open(ACCOUNTS_FILE, "w") as file:
            json.dump(accounts, file)
            return accounts

    def _has_account(self, accounts, name):
        return any(account["name"] == name for account in accounts)

    def _delete_account(self, accounts, account_id):
        return [account for account in accounts if account["id"] != account_id]


@api.route("/records/<record_id>")
class Record(Resource):
    def list(self):
        return self._get_records()

    def create(self):
        data = request.json
        records = self._get_records()
        new_record = {
            "id": str(uuid.uuid4()),
            "title": data["title"],
            "date": data["date"],
            "amount": data["amount"],
            "description": data["description"]
        }
        records.append(new_record)
        return self._save_records(records)

    def delete(self):
        records = self._get_records()
        records = self._delete_record(records, record_id)
        return self._save_records(records)

    def _get_records(self):
        with open(RECORDS_FILE) as file:
            data = file.read()
            return json.loads(data) if data else []

    def _save_records(self, records):
        with open(RECORDS_FILE, "w") as file:
            json.dump(records, file)
            return records

    def _delete_record(self, records, record_id):
        return [record for record in records if record["id"] != record_id]


print(api)
app.run(host='0.0.0.0', port=8000, debug=True)
