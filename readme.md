Hadoop Ansible Scripts
======================

Automated deployment for Cloudera's Distribution of Hadoop (CDHv5, MRv1), leveraging Ansible (1.5).

Design
------

In it's current form, there are two main groups of hosts:
* master
* worker

The master nodes (by default) contain the following services:
* namenode
* secondary namenode
* job tracker

And the worker nodes (again, by default) contain:
* datanode
* task tracker

There are different roles for each type of service, so you can also separate the nodes out as much as you would like. For the sake of simplicity and ease of deployment, it is typically easier just to stick with masters and workers.

Installation
------------

To get up and running as quick as possible, run the following commands (assuming you have `virtualenv` already installed):

```
$ git clone REPO
$ cd repo
$ virtualenv venv
$ ./install.sh
```

Running
-------

Fill in the inventory file (typically just a `hosts` file in the repository root directory), and then run the `run-playbook.sh` script:

```
./run-playbook.sh
```

This is assuming you already have SSH configured.

Local Testing
-------------

As an example, for local testing (if you happen to be using vagrant):

```
./run-playbook.sh --private-key=~/.vagrant.d/insecure_private_key
```

Where your hosts file can look something like:

```
[hadoop:children]
master
worker

[master:children]
namenode
secondary_namenode
jobtracker

[namenode]
localhost ansible_ssh_port=2222 ansible_ssh_user=vagrant

[secondary_namenode]
localhost ansible_ssh_port=2222 ansible_ssh_user=vagrant

[jobtracker]
localhost ansible_ssh_port=2222 ansible_ssh_user=vagrant

[worker:children]
datanode

[datanode]
localhost ansible_ssh_port=2222 ansible_ssh_user=vagrant
```

Remote Testing
--------------

If you would like to use AWS for remote testing, there is an `ec2-provisioner.py` script that you are welcome to use to spin up servers. Once the servers have been allocated, you can copy the hostnames into your inventory file.

A simple workflow to run some EC2 tests might look something like:

```
# Create EC2 credentials file
cat << EOF >./ec2-credentials
[ec2]
access_key=REDACTED
secret_key=REDACTED
ssh_key=my-aws-ssh-key
region=us-east-1
EOF

# Provision servers
./ec2-provisioner.py --count=5 # 4 workers, 1 master

# Copy hostnames to appropriate groups in hosts file, then launch
./run-playbook.sh --private-key=~/.ssh/my-aws-ssh-key -u root
```

Caveats
-------

Only MapReduce v1 is supported at this time. The project goal is to also include MapReduce v2 (YARN) as it becomes more prevalent.

In addition, there are other planned goals for this project:
* Increase security around the cluster
* Integrated support for Zookeeper
* HA Hadoop configuration (multi-master and Zookeeper ensemble)
* Dynamic inventory, allowing for elastic scaling of workers, masters, etc. (probably using tags)
* Investigate support for fireball and optimizing

Contributing
------------

Questions, suggestions, contributions are always welcome. Just send us a pull request.