# -*- coding: utf-8 -*-
'''
Script to Fetch Health Vitals of A Windows server using ``Get-ComputerInfo`` and ``Get-EventLog`` PSUtil.
'''
from __future__ import absolute_import, unicode_literals, print_function

# Import libs
import subprocess as sp
import sys
import socket


def test_win():

	if  sys.platform != "win32":
		sys.exit("This module is only available on Windows.")
	else:
		return "Ok, Fetching Reboot log from the Windows Client \"{}\":-\n".format(socket.gethostname().upper())


def get_lastreb(reb=None, type=None):

	out = {}

	cmd = 'Get-ComputerInfo -Property OSUptime,OSLastBootUpTime,TimeZone,OSLocalDateTime | format-list'
	out = str(sp.Popen(["Powershell", "-ExecutionPolicy", "ByPass", "-NoLogo", "-NoProfile", "-Command", cmd], stdout=sp.PIPE, universal_newlines=True).communicate()[0].strip())
 
	return "RebootTime:-\n"+out+"\n"


def get_log_reb():

    out = {}
 
    cmd = 'Get-EventLog -LogName System -Source User32 -Newest 1 | Select-Object -Property EventID,MachineName,Source,UserName,Message,TimeWritten'
    out = str(sp.Popen(["Powershell", "-ExecutionPolicy", "ByPass", "-NoLogo", "-NoProfile", "-Command", cmd], stdout=sp.PIPE, universal_newlines=True).communicate()[0].strip())
 
    return "Reason:-\n"+out+"\n"


def vital_stats():
 
    out = {}
 
    cmd = 'Get-ComputerInfo -Property OsTotalVisibleMemorySize,OsFreePhysicalMemory,OsFreeVirtualMemory,OsTotalVirtualMemorySize,OsNumberOfProcesses,OsNumberOfUsers | format-list'
    out = str(sp.Popen(["Powershell", "-ExecutionPolicy", "ByPass", "-NoLogo", "-NoProfile", "-Command", cmd], stdout=sp.PIPE, universal_newlines=True).communicate()[0].strip())
 
    return "Host Vitals for Now:-\n"+out+"\n"
 

print(test_win())
print(get_lastreb())
print(get_log_reb())
print(vital_stats())


