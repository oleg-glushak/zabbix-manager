#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import platform
import json
import sys
import requests

from pyzabbix import ZabbixAPI, ZabbixAPIException

#import MocoZabbix
#import MocoConfig


ZABBIX_API_URI = 'http://zabbix.mocomedia.ru/zabbix'
ZABBIX_USER = 'o.glushak@mocomedia.ru'
ZABBIX_PASSWORD = 'Secret'
FOREMAN_API_URI = 'http://xen-puppet1.local.dgvg.ru/api'
FOREMAN_USER = 'o.glushak'
FOREMAN_PASSWORD = 'Secret'
LOG_FILE = '/var/log/zabbix-manager.log'
CONFIG_FILE = 'foreman_zabbix_mappings.cnf'
FOREMAN_HOSTGROUP_KEY = 'hostgroup_name'

def get_short_hostname():
    #return platform.node().split(".")[0]
    return "xen-db-garbd"

def get_fqdn():
    #return platform.node()
    return "xen-db-garbd.local.dgvg.ru"

def get_foreman_hostgroup(hostname):
    try:
        req = requests.get(FOREMAN_API_URI + "/hosts/" + get_fqdn(), auth=(FOREMAN_USER, FOREMAN_PASSWORD))
        if not FOREMAN_HOSTGROUP_KEY in req.json():
            logging.debug('No hostgroup_name key in Foreman response. Exiting...')
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        logging.debug('Failed to get my hostgroup from Foreman: %s. Exiting...', e)
        sys.exit(1)

    return req.json()[FOREMAN_HOSTGROUP_KEY]

def main():
    logging.basicConfig(format=u'[%(asctime)s] %(message)s', level=logging.DEBUG, filename=LOG_FILE)

    config = MocoConfig(CONFIG_FILE)
    config.load()

    zapi = MocoZabbix(ZABBIX_API_URI)
    zapi.login(ZABBIX_USER, ZABBIX_PASSWORD)

    foreman_hostgroup = get_foreman_hostgroup(get_fqdn())
    groups = config.get_zabbix_groups(foreman_hostgroup)

    zapi.replace_groups_for_host(get_short_hostname(), groups)
    #groupid1 = zapi.hostgroup.get(filter={"name": "mysql-slave"})[0]["groupid"]
    #groupid2 = zapi.hostgroup.get(filter={"name": "mysql-master"})[0]["groupid"]
    #zapi.host.update(hostid=hostid, groups=[{"groupid": groupid1}, {"groupid": groupid2}])
    #print zapi.hostgroup.get(hostids=hostid)[0]["name"]


    #zapi.g()
    #print hostgroup
    #config.print_config()

class MocoZabbix(ZabbixAPI):

    def __get_hostid_by_hostname(self, hostname):
        return self.host.get(filter={"host": hostname})[0]["hostid"]

    def __get_groupid_by_groupname(self, groupname):
        return self.hostgroup.get(filter={"name": groupname})[0]["groupid"]

    def replace_groups_for_host(self, hostname, groupnames):
        hostid = self.__get_hostid_by_hostname(hostname)
        api_groupnames = []
        for groupname in groupnames:
            api_groupnames.append({"groupid": self.__get_groupid_by_groupname(groupname)})
        return self.host.update(hostid=hostid, groups=api_groupnames)

    def set_templates_for_host(self, hostname, templates):
        return

class MocoConfig:

    def __init__(self, file_name):
        self.name = file_name

    def load(self):
        try:
            with open(self.name) as data_file:
                self.config = json.load(data_file)
        except Exception as e:
            logging.debug('Failed to load config: %s. Exiting...', e)
            sys.exit(1)
        else:
            return self.config

    def get_zabbix_groups(self, foreman_hostgroup):
        return self.config[foreman_hostgroup]['zabbix_groups']

    def print_config(self):
        print self.config

if __name__ == '__main__':
    main()
