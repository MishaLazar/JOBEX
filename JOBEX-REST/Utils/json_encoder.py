import json
from bson import ObjectId,json_util


class JSONEncoder(json.JSONEncoder):

    def default(self,o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.dumps(obj=o, default=json_util.default)

