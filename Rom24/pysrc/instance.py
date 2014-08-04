__author__ = 'quixadhal'
import os
import json
from collections import OrderedDict, namedtuple
import logging

logger = logging.getLogger()

import settings


# NOTE:  This is nowhere near finished, just a WIP at the moment, ideas to be explored.
data = {}
max_id = 0


class InstanceEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        elif isinstance(o, set):
            return {
                '__type__': o.__class__.__name__,
                '__data__': [json.JSONEncoder.default(self, k) for k in o]
            }
        elif isinstance(o, tuple):
            return {
                '__type__': o.__class__.__name__,
                '__data__': [json.JSONEncoder.default(self, k) for k in o]
            }
        elif isinstance(o, OrderedDict):
            return {
                '__type__': o.__class__.__name__,
                '__data__': [json.JSONEncoder.default(self, k) for k in o.items]
            }
        return json.JSONEncoder.default(self, o)


class InstanceDecoder(json.JSONDecoder):
    pass


def save():
    os.makedirs(settings.INSTANCE_DIR, 0o755, True)
    filename = os.path.join(settings.INSTANCE_DIR, 'list' + '.json')
    with open(filename, 'w') as fp:
        json.dump({'max_id': max_id, 'data': data}, fp, cls=InstanceEncoder)
        fp.close()


def load():
    filename = os.path.join(settings.INSTANCE_DIR, 'list' + '.json')
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            tmp = json.load(fp)
            global max_id, data
            max_id = tmp['max_id']
            data = tmp['data']
            fp.close()


class Instance:
    def __init__(self, instance_id: int=None, ref_type: str=None, vnum: int=None, ref=None):
        self.instance_id = instance_id
        self.ref_type = ref_type
        self.vnum = vnum
        self.ref = ref

    def to_json(self):
        if isinstance(self, Instance):
            return {
                '__Instance__': {
                    'instance_id': self.instance_id,
                    'ref_type': self.ref_type,
                    'vnum': self.vnum,
                    'ref': self.ref,
                },
            }
        raise TypeError(repr(self) + " is not JSON serializable")

