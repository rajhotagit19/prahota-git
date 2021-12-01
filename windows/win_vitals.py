# -*- coding: utf-8 -*-
'''
Module for get Health vitals of Windows server using ``Get-ComputerInfo`` and ``Get-EventLog``
'''
from __future__ import absolute_import, unicode_literals, print_function

# Import libs
import subprocess as sp
import sys
import socket
import re


cmd = 'Powershell -ExecutionPolicy ByPass -NoLogo -NoProfile -Command Get-ComputerInfo'
out = sp.Popen(cmd, stdout=sp.PIPE, universal_newlines=True).communicate()[0].splitlines()


def test_win():

  if  sys.platform != "win32":
    sys.exit("This module is only available on Windows.")
  else:
    return "Ok, Fetching Reboot log from the Windows Client \"{}\":-\n".format(socket.gethostname().upper())




def get_lastreb():

  res = []

  #cmd = 'Get-ComputerInfo -Property OsUptime,OsLastBootUpTime,TimeZone,OsLocalDateTime | format-list'
  for line in out:
    for chk in ["OsUptime","OsLastBootUpTime","TimeZone","OsLocalDateTime"]:
      if re.match(chk, line):
        res.append(re.sub(r"{}\s+".format(chk), chk, line))
        res.append("\n")


  return "Rebooted at:-\n"+"".join(res)


def get_log_reb():

  out1 = {}

  cmd1 = 'Powershell -ExecutionPolicy ByPass -NoLogo -NoProfile -Command Get-EventLog -LogName System -Source User32 -Newest 1 | Select-Object -Property EventID,MachineName,Source,UserName,Message,TimeWritten'
  out1 = str(sp.Popen(cmd1, stdout=sp.PIPE, universal_newlines=True).communicate()[0].strip())

  return "Reason of Reboot:-\n"+out1+"\n"


def vital_stats():

  res = []

  #cmd = 'Get-ComputerInfo -Property OsTotalVisibleMemorySize,OsFreePhysicalMemory,OsFreeVirtualMemory,OsTotalVirtualMemorySize,OsNumberOfProcesses,OsNumberOfUsers | format-list'
  for line in out:
    for chk in ["OsTotalVisibleMemorySize","OsFreePhysicalMemory","OsFreeVirtualMemory","OsTotalVirtualMemorySize"]:
      if re.match(chk, line):
        res.append(re.sub(r"{}\s+".format(chk), chk, line)+" KB\n")

    for chk in ["OsNumberOfProcesses","OsNumberOfUsers"]:
      if re.match(chk, line):
        res.append(re.sub(r"{}\s+".format(chk), chk, line)+"\n")


  return "Host Vitals for Now:-\n"+"".join(res)


print(test_win())
print(get_lastreb())
print(get_log_reb())
print(vital_stats())

