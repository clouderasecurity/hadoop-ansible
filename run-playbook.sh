#!/bin/bash
# Quick script to verify syntax before running. All CLI args are passed to 'ansible-playbook'
ansible-playbook site.yml -i hosts --syntax-check && ansible-playbook site.yml -i hosts $@
