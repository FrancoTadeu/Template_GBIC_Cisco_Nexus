#!/usr/bin/python3.8
#_*_ coding: utf-8 _*_

import sys
import puresnmp
import json

script, snmp_community, snmp_host, port = sys.argv

#Error message to avoid zabbix errors.
error_message = '[{"{#INTERFACE}": "null","{#TX_OID_LANE1}": "null","{#RX_OID_LANE1}": "null","{#VOLTAGE_OID_LANE1}": "null","{#BIAS_OID_LANE1}": "null","{#TEMPERATURE_OID_LANE1}": "null","{#TX_OID_LANE2}": "null","{#RX_OID_LANE2}": "null",	"{#VOLTAGE_OID_LANE2}": "null","{#BIAS_OID_LANE2}": "null","{#TEMPERATURE_OID_LANE2}": "null","{#TX_OID_LANE3}": "null","{#RX_OID_LANE3}": "null","{#VOLTAGE_OID_LANE3}": "null","{#BIAS_OID_LANE3}": "null","{#TEMPERATURE_OID_LANE3}": "null","{#TX_OID_LANE4}": "null","{#RX_OID_LANE4}": "null","{#VOLTAGE_OID_LANE4}": "null","{#BIAS_OID_LANE4}": "null","{#TEMPERATURE_OID_LANE4}": "null"}'



alias_dic = {}
try:
    for row in puresnmp.multiwalk(snmp_host, snmp_community, ['.1.3.6.1.2.1.31.1.1.1.18', '.1.3.6.1.2.1.31.1.1.1.1'], port=int(port), timeout=4):
        #row_format = str(row[0]) + ":" + str(row[1].decode())

        snmp_alias_oid = str(row[0]).split('.',11)[10]
        snmp_oid = str(row[0]).split('.',11)[11]
        snmp_interface = str(row[1].decode())
        #print(snmp_oid + " - " + snmp_interface)
        #Buiding the dictionary

        if not snmp_oid in alias_dic:
            alias_dic[snmp_oid] = {}

        if snmp_alias_oid == '18':
            alias_dic[snmp_oid]['{#ALIAS}'] = snmp_interface

        if snmp_alias_oid == '1':
            alias_dic[snmp_oid]['{#IFNAME}'] = snmp_interface

        #snmp_alias = row_format.split(' ',7)[0]
        #print(snmp_alias)
        #alias_dic[snmp_interface] = {}

except puresnmp.exc.Timeout as error:
    print(error_message)
    sys.exit()


def search_alias(snmp_interface):
    for interface in alias_dic.values():
        #print(interface['{#ALIAS}'])
        if snmp_interface == interface['{#IFNAME}']:
            #print(interface['{#ALIAS}'])
            return interface['{#ALIAS}']


dic = {}
#For in the snmpwalk
try:
    for row in puresnmp.multiwalk(snmp_host, snmp_community, ['.1.3.6.1.2.1.47.1.1.1.1.2','.1.3.6.1.2.1.31.1.1.1.1','.1.3.6.1.2.1.31.1.1.1.18'], port=int(port), timeout=4):

        #Filtering the information, because there is a lot of crap.
        if ('Transceiver' in row[1].decode()) and ('Ethernet' in row[1].decode()):
            #print(row)
            #Formating to remove some bytes inside the row[1]
            row_format = str(row[1].decode())
            
            #print("{} : {}".format(row[0],row[1].decode()))
            
            #Getting the variables with split and formating.
            snmp_interface = row_format.split(' ',7)[0]
            index_oid= str(row[0]).split('.',12)[12]
            snmp_module = row_format.split(' ', 7)[4]
            snmp_lane = row_format.split(' ', 7)[2]
            
            #Buiding the dictionary
            if not snmp_interface in dic:
                dic[snmp_interface] = {}
            
            #Is possible 4 lanes, so... this is why exist.
            if not snmp_lane in dic[snmp_interface]:
                dic[snmp_interface][snmp_lane] = {}

            #Above is the ID's for each lane.
            if 'Voltage' in snmp_module:
                dic[snmp_interface][snmp_lane]['{#VOLTAGE_OID}'] = index_oid

            if 'Temperature' in snmp_module:
                dic[snmp_interface][snmp_lane]['{#TEMPERATURE_OID}'] = index_oid

            if 'Receive' in snmp_module:
                dic[snmp_interface][snmp_lane]['{#RX_OID}'] = index_oid

            if 'Transmit' in snmp_module:
                dic[snmp_interface][snmp_lane]['{#TX_OID}'] = index_oid
            
            if 'Bias' in snmp_module:
                dic[snmp_interface][snmp_lane]['{#BIAS_OID}'] = index_oid

#Exception for Timeout
except puresnmp.exc.Timeout as error:
    print(error_message)
    sys.exit()

#For the count of the lanes.
x = 1
#Empty for the json.list
l = []
for interface in dic:
    #Starting the object for each interface
    obj = {}
    
    #Starting the first level of the dict
    obj['{#INTERFACE}'] = interface
    obj['{#ALIAS}'] = search_alias(interface)
    #Lanes 1 to 4.
    for x in range(1, 5):

        #If the lane REAL exist, will populate with the OID.
        if str(x) in dic[interface]:
            #print(x)
            obj['{#TX_OID_LANE' + str(x) + '}'] = dic[interface][str(x)]['{#TX_OID}']
            obj['{#RX_OID_LANE' + str(x) + '}'] = dic[interface][str(x)]['{#RX_OID}']
            obj['{#VOLTAGE_OID_LANE' + str(x) + '}'] = dic[interface][str(x)]['{#VOLTAGE_OID}']
            obj['{#BIAS_OID_LANE' + str(x) + '}'] = dic[interface][str(x)]['{#BIAS_OID}']
            obj['{#TEMPERATURE_OID_LANE' + str(x) + '}'] = dic[interface][str(x)]['{#TEMPERATURE_OID}']
            

        #If the lane doesn't exist, fill populate with 0, because Zabbix need some value to apply the filter. Dumb stuffs.
        else:
            obj['{#TX_OID_LANE' + str(x) + '}'] = "0"
            obj['{#RX_OID_LANE' + str(x) + '}'] = "0"
            obj['{#VOLTAGE_OID_LANE' + str(x) + '}'] = "0"
            obj['{#BIAS_OID_LANE' + str(x) + '}'] = "0"
            obj['{#TEMPERATURE_OID_LANE' + str(x) + '}'] = "0"
            

    #Append the dictonary to the list   
    l.append(obj)


#Safe exception for any possibles errors.
if not l:
    print(error_message)
    sys.exit()

#Magic convert the list to json.
jsonStr = json.dumps(l)
print(jsonStr)