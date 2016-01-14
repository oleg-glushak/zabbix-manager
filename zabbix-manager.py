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

def get_my_short_hostname():
    return platform.node().split('.')[0]

def get_my_hostgroup():
    return "testhostgroup"

def main():
    hostgroup = get_my_hostgroup()
    print get_my_short_hostname()

if __name__ == '__main__':
    main()
