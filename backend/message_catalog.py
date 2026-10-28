import json
from dataclasses import asdict

MESSAGE_PATH = "backend/metadata/messages.json"


class MessageCatalog:
    def __init__(self, file_path=MESSAGE_PATH):
        with open(file_path, "r", encoding="utf-8") as file:
            self.messages = json.load(file)

    def get(self, key, data=None, **kwargs):
        if key not in self.messages:
            raise KeyError(f"Message code '{key}' not found")

        entry = self.messages[key]

        if data == None:
            return {
                "success": entry["success"],
                "code": entry["code"],
                "message": entry["message"].format(**kwargs),
            }

        return {
            "success": entry["success"],
            "code": entry["code"],
            "message": entry["message"].format(**kwargs),
            "data": [asdict(d) for d in data],
        }
