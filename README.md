Ripple Altnet Ansible Magics
============================

These playbooks help us manage the Ripple Altnet. There are a couple common
tasks that one might want to perform:

Emergency Shutdown of Altnet
----------------------------

    $ ansible-playbook -i hosts.txt big-red-button.yml

It will confirm that you do in fact want to ruin everyone's day before actually
killing all rippled processes on all machines.

Modifying network quorum
------------------------

    $ ansible-playbook -i hosts.txt -e validation_quorum=4 plays/restart-network.yml

Adding a new validator
----------------------

Add your new validator to hosts.txt with the appropriate region, IP, key, and UUID.
Do the same for vars/validators.yml, and update the validation_quorum in there
appropriately. Finally, add the private keys to validation-keys/{{uuid}} Then:

    $ ansible-playbook -i hosts.txt plays/restart-network.yml

Installing SumoLogic log collection
-----------------------------------

    $ ansible-playbook -i hosts.txt plays/sumologic.yml

Run an RPC command
------------------

    $ ansible-playbook -i hosts.txt plays/do-rpc.yml

Recover after a validator crash (EXPERIMENTAL)
----------------------------------------------

This playbook is highly experimental, and hasn't been used successfully yet.
However it should provide some illumination as to what it takes to bootstrap a
rippled validator network should the network sink below the quorum threshold.

    $ ansible-playbook -i hosts.txt plays/recover-network.yml
