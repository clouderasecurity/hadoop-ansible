Hadoop Ansible Scripts
======================

Automated deployment for Hadoop, written in Ansible.

Installation
------------

To get up and running as quick as possible, run the following commands (assuming you have `virtualenv` already installed):

```
$ git clone gitrepo
$ cd gitrepo
$ virtualenv venv
$ ./install.sh
```

Running
-------

Fill in the inventory file (typically just a `hosts` file in the root directory), and then run the `run-playbook.sh` script. Similar to:

```
./run-playbook.sh
```

You might need to add extra configurations if your SSH is not already configured.