#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import os
#import datetime
import logging
import platform
#import re
#import sys
#from operator import itemgetter

zabbix_api_uri = "http://zabbix.mocomedia.ru/api_jsonrpc.php"
zabbix_user = "api"
zabbix_password = "SecretPassword"
foreman_api_uri = "http://xen-puppet1.local.dgvg.ru/api"
foreman_user = "api"
foreman_password = "SecretPassword"
log_file = "/var/log/zabbix-manager.log"

def get_my_hostname():
    return platform.node()

def get_my_hostgroup():
    #get my hostname and get hostgroup for my hostname
    return "testhostgroup"

def main():
    hostgroup = get_my_hostgroup()
    print "Hello"

if __name__ == '__main__':
    main()
