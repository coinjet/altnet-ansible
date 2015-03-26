Ripple Altnet Ansible Magics
============================

First thing you'll want to do is pull the private credentials repositories:

    $ git submodule update --init

These playbooks help us manage the Ripple Altnet. There are a couple common
tasks that one might want to perform:

Emergency Shutdown of Altnet
----------------------------

    $ ansible-playbook -i inventory.py big-red-button.yml

It will confirm that you do in fact want to ruin everyone's day before actually
killing all rippled processes on all machines.

Temporarily Modifying network quorum
------------------------

    $ ansible-playbook -i inventory.py -e validation_quorum=4 plays/restart-network.yml

Adding a new validator
----------------------

Add your new validator to validators.yml with the appropriate region, IP, key, and UUID.
Next, update validation_quorum in validators.yml.
Finally, add the private keys to validation-keys/{{uuid}} Then:

    $ ansible-playbook -i validators.yml plays/restart-network.yml

Installing SumoLogic log collection
-----------------------------------

    $ ansible-playbook -i validators.yml plays/sumologic.yml

Run an RPC command
------------------

    $ ansible-playbook -i validators.yml plays/do-rpc.yml

Recover after a validator crash (EXPERIMENTAL)
----------------------------------------------

This playbook is highly experimental, and hasn't been used successfully yet.
However it should provide some illumination as to what it takes to bootstrap a
rippled validator network should the network sink below the quorum threshold.

    $ ansible-playbook -i validators.yml plays/recover-network.yml
