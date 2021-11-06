# Zabbix Transceiver Cisco Nexus Template
Zabbix Template with Python script to monitoring transceivers from Cisco Nexus series.

Compatiblity: Zabbix 5.0>

Install Puresnmp:

pip install puresnmp

##Tested with Python 3.6 and Python 3.8 without any problems.

The first line in the cisco_nx_fiber.py should be your Python3 dir. In my scenario is: #!/usr/bin/python3.8  - Edit for yours if is needed.

The file cisco_nx_fiber.py should be put in your external files directory and give permission to be executed.

The XML file is exported direct inside Zabbix Frontend.

This template is modular, should work with any GBIC/Transceiver without a problem, even if is 4 lanes and give no errors. Tested in Cisco 3000 Nexus series only.

The values that are collect:

-Voltage
-Temperature
-Signal RX
-Signal TX
-Bias
-Threshold RX
-Threshold TX

I believe there is still improviments to be done, but for now is working without any problem.
Triggers,Graphs and Tags are in Portuguese.
