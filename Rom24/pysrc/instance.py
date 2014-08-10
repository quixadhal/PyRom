__author__ = 'quixadhal'

import os
import json
from collections import OrderedDict, namedtuple
import logging

logger = logging.getLogger()

import settings
import merc


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


class Instancer:
    def __init__(self):
        """Here is the backbone of our instancing. This function takes the global instance
        number and increments it. After dealing with the dicts for our objects, we will save
        the global instance number to a file, which will be important later when persistence
         is, or if someone wants to, be implemented.

        It is passed the object instance, for which we will make an identification.

        First we match the type we need to make, then add that to each dict that it needs to be in.

        As we are using just a single pointer between all of these dicts, we populate global_instances
        first, with a pointer to the object. The following dicts 'alias' their value to the value
        represented in global_instances[instance_id].

        This lets us maintain a single pointer, with windows to that single pointer from our sub dicts,
        allowing for a saner environment.

        This means that the destructor should destruct in reverse order, just in case."""
        super().__init__()
        self.instance_id = None

    def instancer(self):
        merc.instance_number += 1
        self.instance_id = merc.instance_number
