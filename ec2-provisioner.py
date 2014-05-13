#!/usr/bin/env python

# Copyright 2014, Gazzang Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import boto.ec2
from sys import exit
from time import sleep
from ConfigParser import RawConfigParser

# All of the instance types currently available
instances_available = {
    'CentOS 6.4': 'ami-bf5021d6',
}

# Initiate connection to AWS, with desired credentials
def initiate(access_key, secret_key, region='us-east-1'):
    conn = boto.ec2.connect_to_region(region, aws_access_key_id = access_key, aws_secret_access_key = secret_key)
    return conn

# Spawn an instance, with a valid AWS connection parameter, an ssh key name, and an AMI ID
# Optional parameters include: instance size, security group, and number of instances
def spawn(aws_conn, ami_id, size, ssh_key='default', sec_group='default', count=1):
    reservation = None
    try:
        reservation = aws_conn.run_instances(ami_id, min_count = 1, max_count = count, key_name = ssh_key, instance_type = size, security_groups = [sec_group])
    except Exception as e:
        print "Error encountered:\n %s" % e
        exit(1)
    return reservation

# Collect valid information from instance, once booted
def wait_until_loaded(reservation):
    print "Request made. Waiting for instance(s) to come online..."
    for instance in reservation.instances:
        while instance.public_dns_name == '':
            sleep(5)
            instance.update()

# Read ec2 configuration
def provision(ami_type, size, count):
    print "Creating instance type [%s], of size [%s]" % (ami_type, size)
    import ConfigParser, os
    conf_file='ec2-credentials'
    print "Parsing ec2-credentials file [%s]" % conf_file
    config = ConfigParser.ConfigParser()
    config.read(conf_file)
    conn = initiate(access_key=config.get('ec2', 'access_key'), secret_key=config.get('ec2', 'secret_key'), region=config.get('ec2', 'region'))
    reservation = spawn(conn, instances_available.get(ami_type), size, ssh_key=config.get('ec2', 'ssh_key'), count=count)
    wait_until_loaded(reservation) # wait until the instances are loaded and ready for requests
    print "Instance(s) launched successfully."
    print "\nPublic hostnames:"
    for instance in reservation.instances:
        print instance.public_dns_name
    print ""


# Retrieve and parse CLI arguments
def get_args():
    from argparse import ArgumentParser
    main_parser = ArgumentParser(description='[ec2-provisioner] Initiator of instances on AWS EC2.')
    main_parser.add_argument('--instance',
                            help = 'Type of instance to spawn. Defaults to MySQL on CentOS.',
                            default = 'CentOS 6.4',
                            required = False)
    main_parser.add_argument('--size',
                            help = 'Size of instance (defaults to t1.micro)',
                            default = 'm1.small',
                            required = False)
    main_parser.add_argument('--count',
                            help = 'Number of instances to provision (defaults to 1)',
                            default = '1',
                            required = False)
    main_parser.add_argument('--group',
                            help = 'Security group to use.',
                            default = 'default',
                            required = False)
    print "Parsing arguments..."
    args = main_parser.parse_args()
    return args

def main():
    args = get_args()
    provision(args.instance, args.size, args.count)

if __name__ == "__main__":
    main()
