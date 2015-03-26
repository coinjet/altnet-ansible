#!/usr/bin/env python
import yaml
import json

fh = open('validators.yml', 'r')

validators = yaml.load(fh.read())

inventory = {
  '_meta': {
    'hostvars': {}
  }
}

for validator in validators['validators']:
  meta = {}

  for k,v in validator.iteritems():
    groupName = '%s_%s'%(k, v)

    if groupName not in inventory:
      inventory[groupName] = []

    inventory[groupName].append(validator['ip'])
    meta['validator_%s'%k] = v

  keyFH = open('validation-keys/%s'%(validator['uuid']), 'r')
  keys = yaml.load(keyFH.read())
  keyFH.close()

  peers = []

  for peer in validators['validators']:
    peers.append(peer)

  meta['validator_peers'] = peers
  meta['validator_private_key'] = keys['validation_seed']
  meta['ansible_ssh_private_key_file'] = 'skynet-keys/%s.pem'%(meta['validator_region'])
  meta['validation_quorum'] = validators['validation_quorum']

  inventory['_meta']['hostvars'][validator['ip']] = meta

print json.dumps(inventory, indent=2)
