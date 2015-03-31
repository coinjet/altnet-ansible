#!/usr/bin/env python
import json
import yaml
import boto.ec2
import logging
import argparse
import uuid
import time
import sys
import requests

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

logging.getLogger('boto').setLevel(logging.WARN)

parser = argparse.ArgumentParser(
    description="Generate a new altnet")

parser.add_argument(
    '--size', default=5, metavar='size', type=int, help='Number of instances to spin up')
parser.add_argument(
    '--name', default='', metavar='name', type=str, help='Network name')

args = parser.parse_args()

id = str(uuid.uuid4())

logging.basicConfig(level=logging.DEBUG)
logging.debug("Spinning up altnet %s named '%s' with %d nodes...", id, args.name,
    args.size)

region = 'us-east-1'
ec2 = boto.ec2.connect_to_region(region)
ami = "ami-9a562df2"
key_name = "codius-host-virginia"
subnet = "subnet-53a17d78"
secGroups = ['sg-67fc7503']

reservation = ec2.run_instances(
    image_id=ami,
    min_count=args.size, max_count=args.size,
    key_name=key_name,
    security_group_ids=secGroups,
    instance_type='m3.medium',
    subnet_id=subnet)

tags = {
    'devnet_id': id,
    'devnet_name': args.name,
    'devnet_size': args.size
}

inventory = {
  'validator_quorum': int(args.size * 0.8),
  'validators': []
}

for i in reservation.instances:
  instanceID = str(uuid.uuid4())
  ec2.create_tags(i.id, tags)
  ec2.create_tags(i.id, {'uuid': instanceID})
  logging.info("Launching: %s -> %s", instanceID, i.id)
  i.update()
  while i.ip_address is None:
    time.sleep(2)
    i.update()
  logging.info("Got address: %s", i.ip_address)
  keys = gen_validator_keys()
  instanceMeta = {
      'uuid': instanceID,
      'key': str(keys['validation_public_key']),
      'ip': str(i.ip_address),
      'port': 51235,
      'region': region
  }
  inventory['validators'].append(instanceMeta)
  yaml.dump({
    'validation_seed': keys['validation_seed'],
    'validation_public_key': keys['validation_public_key']
  }, open('validation-keys/%s'%(instanceID), 'w'))
  logging.info("Wrote private validator keys to validation-keys/%s", instanceID)

yaml.dump(inventory, open('validators-%s.yml'%(id), 'w'),
    default_flow_style=False)
logging.info("Wrote inventory to validators-%s.yml", id)
