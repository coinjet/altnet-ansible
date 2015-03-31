import requests
import yaml
import json
import uuid

regions = {
    'us-east-1': {
      'ami': 'ami-6ab4ee02',
      'subnet': 'subnet-53a17d78',
      'groups': ['sg-67fc7503'],
      'key': 'codius-host-virginia'
    },
    'us-west-2': {
      'ami': 'ami-91af8ca1',
      'subnet': 'subnet-444aca21',
      'key': 'codius-host-oregon',
      'groups': ['sg-b05c68d5']
    },
    'us-west-1': {
      'ami': 'ami-e3ab4ca7',
      'subnet': 'subnet-c7d2cc81',
      'key': 'codius-host-california',
      'groups': ['sg-85e44be0']
    }
}

def gen_validator_keys():
  url = 'https://localhost:5005'
  data = {
      'method': 'validation_create',
      'params': [],
  }
  headers = {
      'content-type': 'application/json'
  }

  return requests.post(url, data=json.dumps(data), headers=headers,
      verify=False).json()['result']

class Validator(object):
    def __init__(self):
        super(Validator, self).__init__()
        self.uuid = str(uuid.uuid4())
        keys = gen_validator_keys()
        self.public_key = str(keys['validation_public_key'])
        self.seed = str(keys['validation_seed'])

    def __str__(self):
      return self.uuid
