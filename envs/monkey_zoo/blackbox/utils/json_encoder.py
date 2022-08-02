import json

from bson import ObjectId


class MongoQueryJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return str(o) if isinstance(o, ObjectId) else json.JSONEncoder.default(self, o)
