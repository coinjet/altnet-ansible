#!/usr/bin/env python
import json
import random
import yaml
import boto.ec2
import logging
import argparse
import uuid
import time
import sys
import requests

import lib

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('boto').setLevel(logging.WARN)

parser = argparse.ArgumentParser(
    description="Generate a new altnet validator")

parser.add_argument(
    '--region', default=None, metavar='region', type=str, help='AWS region')

args = parser.parse_args()

id = str(uuid.uuid4())

if args.region is None:
  args.region = random.choice(lib.regions.keys())

region = lib.regions[args.region]

inventory = yaml.load(open('validators.yml', 'r'))

validator = lib.Validator()

logging.debug("Spinning up altnet validator %s in %s...", validator.uuid,
    args.region)

ec2 = boto.ec2.connect_to_region(args.region)

instance = ec2.run_instances(
    image_id=region['ami'],
    min_count=1, max_count=1,
    key_name=region['key'],
    security_group_ids=region['groups'],
    instance_type='m3.medium',
    subnet_id=region['subnet']).instances[0]

tags = {
    'uuid': validator.uuid,
    'environment': 'production',
    'site': 'rippletest.net',
    'devnet_name': 'altnet',
    'Name': 'Altnet validator %s'%(validator.uuid)
}
ec2.create_tags(instance.id, tags)

logging.info("Launching: %s -> %s", validator, instance.id)
instance.update()
while instance.ip_address is None:
  time.sleep(2)
  instance.update()
logging.info("Got address: %s", instance.ip_address)
instanceMeta = {
    'uuid': validator.uuid,
    'key': validator.public_key,
    'ip': str(instance.ip_address),
    'port': 51235,
    'region': args.region,
}
inventory['validators'].append(instanceMeta)
yaml.dump({
  'validation_seed': validator.seed,
  'validation_public_key': validator.public_key
}, open('validation-keys/%s'%(validator.uuid), 'w'), default_flow_style=False)
logging.info("Wrote private validator keys to validation-keys/%s",
    validator.uuid)

yaml.dump(inventory, open('validators.yml', 'w'),
    default_flow_style=False)
logging.info("Wrote updated inventory to validators.yml")

