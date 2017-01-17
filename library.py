#!/usr/bin/python3.5

################################################################################
# library.py - Library of functions for memcheck_threshold_notifier.py     
#  
# Copyright 2016-2017 by David Brenner Jr <david.brenner.jr@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
################################################################################

# import required modules
try:
  import sys
  import platform
  import subprocess
  import os
  import re
  import io
  import syslog
except ImportError:
  print("FAILURE: Failed to import required modules")
  sys.exit()

# globals
status_flag = False
path_chk = False
log_chk = False
fd_chk = False
heap_chk = False
leak_chk = False
error_chk = False

# exec system command, return output or nothing
def syscmd(command): 
  if command != 0 or command != "":  
    command2 = "%s" % command
    p = subprocess.Popen(command2, shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    try:
      out, _ = p.communicate()
    except ValueError or OSError:
      p.kill()
  else:
    pass
  return out

# try checking operating system name and operating system version exists
# in list of supported operating systems, else throw OS error then
# display non-critical warning message.   
def check_distribution():
  try:
    tested_os = {"Ubuntu":16, "Test1":1, "Test2":2}
    os_name, os_version, _ = platform.linux_distribution()
    if str(os_name) in tested_os.keys():
      if int(round(float(os_version),0)) != tested_os[os_name]:     
        print("WARNING: Distribution not supported: %s %s" % (os_name, os_version))
        raise OSError
      else:
        pass
    else:
      print("WARNING: Distribution not supported: %s %s" % (os_name, os_version)) 
      raise OSError
  except OSError:
    os_list = ""
    for key in tested_os:
      os_list = os_list + key + " " + str(tested_os[key]) + ", "
    print("Supported distributions: %s" % os_list[:-2])
    
# try querying the package management system for the status of the required
# packages, else throw OS error then display failure message and exit.
def check_dependencies():
  try:
    package = syscmd("dpkg-query -W --showformat='${Package} ${Status} ${Version}\n' valgrind")
    package = package.strip()
    if "valgrind install ok installed" not in package:
      raise OSError
    else:
      pass
  except OSError:
    print("FAILURE: valgrind not installed: %s" % package)
    sys.exit()
  try:
    package = syscmd("dpkg-query -W --showformat='${Package} ${Status} ${Version}\n' rsyslog")
    package = package.strip()
    if "rsyslog install ok installed" not in package:
      raise OSError
    else:
      pass
  except OSError:
    print("FAILURE: rsyslog not installed: %s" % package)
    sys.exit()
    
# check opening/creating required log file
def check_required_options():
  global path_chk
  global log_chk
  # check path of binary
  if path_chk is False:
    try:
      if os.path.exists(sys.argv[1]):
        # convert path_chk to value of option
        path_chk = str(sys.argv[1])
      else:
        raise IOError
    except IOError:
      print("FAILURE: Can't find binary %s" % sys.argv[1])
      print("Usage: ./memcheck_threshold_notifier.py /path/to/binary --log-file /path/to/file <options>")
      sys.exit()
  else:
    pass 
  # valgrind redirects its output to active console window. the output from
  # the binary ran by valgrind is sent to stdout. So --log-file is required to
  # parse valgrind's error report. check log file or create it
  if log_chk is False:
    try:
      if sys.argv[2] == "--log-file":
        fd = open(sys.argv[3], 'a')
        fd.close()
        # convert log_chk to value of option
        log_chk = str(sys.argv[3])
      else:
        raise IOError
    except IOError:
      print("FAILURE: Can't open/create required log file %s" % sys.argv[3])
      print("Usage: ./memcheck_threshold_notifier.py /path/to/binary --log-file /path/to/file <options>")
      sys.exit()
  else:
    pass
    
# check memcheck.py arguments, throw failure
def check_other_options():
  global fd_chk
  global heap_chk
  global leak_chk
  global error_chk
  try:
    i = 4
    while i < len(sys.argv):
      # check option file descriptors thresholds
      if sys.argv[i] == "--fd-threshold":
        if fd_chk is False:
          try:
            # check input pattern
            if re.match("[0-9]{1,5}", sys.argv[i+1]):
              # convert fd_chk to value of option
              fd_chk = str(sys.argv[i+1])
            else:
              raise ValueError
          except ValueError:
            print("WARNING: Invalid input for fd-threshold, ignoring it")
        else:
          pass
      # check option heap summary thresholds
      elif sys.argv[i] == "--heap-threshold":
        if heap_chk is False:
          try:
            # check input pattern
            if re.match("[0-9]{1,8}\,[0-9]{1,8}", sys.argv[i+1]):
              # convert heap_chk to value of option
              heap_chk = str(sys.argv[i+1])
            else:
              raise ValueError
          except ValueError:
            print("WARNING: Invalid input for heap-threshold, ignoring it")
        else:
          pass
      # check option leak summary thresholds
      elif sys.argv[i] == "--leak-threshold":
        if leak_chk is False:
          try:
            # check input pattern
            if re.match("[0-9]{1,8}\,[0-9]{1,8}\,[0-9]{1,8}\,[0-9]{1,8}\,[0-9]{1,8}", sys.argv[i+1]):
              # convert leak_chk to value of option
              leak_chk = str(sys.argv[i+1])
            else:
              raise ValueError
          except ValueError:
            print("WARNING: Invalid input for leak-threshold, ignoring it")
        else:
          pass
      # check option error summary thresholds
      elif sys.argv[i] == "--error-threshold":
        if error_chk is False:
          try:
            # check input pattern
            if re.match("[0-9]{1,8}\,[0-9]{1,8}", sys.argv[i+1]):
              # convert error_chk to value of option
              error_chk = str(sys.argv[i+1])
            else:
              raise ValueError
          except ValueError:
            print("WARNING: Invalid input for error-threshold, ignoring it")
        else:
          pass
      else:
        pass
      # increment while loop
      i = i + 1     
  except IOError:
    print("FAILURE: Invalid format of options for memcheck_threshold_notifier.py")
    print("Usage: ./memcheck_threshold_notifier.py /path/to/binary --log-file /path/to/file <options>")
    sys.exit()

# run required checks
check_distribution()
check_dependencies()
check_required_options()
check_other_options()

# remove code for checks 
del check_distribution
del check_dependencies
del check_required_options
del check_other_options

# return next line
def nextline(fileobj):
  newline = fileobj.readline()
  newline = newline.strip()
  return newline

# try checking service status of rsyslog, else throw OSError. if rsyslog is
# running, set flag to true. if rsyslog is not running, set flag to false.
def check_rsyslog_status():
  global status_flag
  try:
    status = syscmd("service rsyslog status")
    if "Active: active (running)" in status:
      status_flag = True
    else:
      raise OSError
  except OSError:
    status_flag = False
    
# check status of rsyslog service before logging data. if rsyslog is not running,
# save actual memcheck log file at "logs/memcheck/timestamp".
def log_data(message=""):
  global status_flag
  global log_chk
  check_rsyslog_status()
  # send data to local rsyslog service
  if status_flag is True:    
    syslog.syslog("MEMCHECK_THRESHOLD_NOTIFIER.PY %s" % str(message))
  # save to logs/memcheck/timestamp
  else:
    timestamp = calendar.timegm(time.gmtime())
    if os.path.exists("logs/memcheck"):
      _ = syscmd("cat %s > logs/memcheck/%s" % (log_chk, timestamp))
      message = '%s' % message
      _ = syscmd("echo %s >> logs/memcheck/%s" % (message, timestamp))
    else:
      _ = syscmd("mkdir -p logs/memcheck")
      _ = syscmd("cat %s > logs/memcheck/%s" % (log_chk, timestamp))
      message = '%s' % message
      _ = syscmd("echo %s >> logs/memcheck/%s" % (message, timestamp))
      
# run memcheck with options, return output. 
def run_memcheck():  
  global path_chk
  global log_chk
  try:
    # assemble command string with both options, run memcheck   
    if path_chk is not False and log_chk is not False:
      # syscmd returns the output of the command specified as path_chk. should
      # check the format of that output matches expected format.
      _ = syscmd("valgrind --tool=memcheck --trace-children=yes --track-fds=yes --leak-check=full --leak-resolution=high --leak-check-heuristics=all --show-reachable=no --partial-loads-ok=no --track-origins=yes --log-file=%s %s" % (log_chk, path_chk))
    else:   
      raise RuntimeError
  except RuntimeError:
    print("FAILURE: Couldn't get output from memcheck")
    sys.exit()

# open memcheck error report, compare kvp in report to thresholds
def parse_report():
  global path_chk
  global log_chk
  global fd_chk
  global heap_chk
  global leak_chk
  global error_chk
  if os.path.exists(log_chk):
    try:
      report = open(log_chk, "r")
      report.seek(0)
    except IOError:
      print("FAILURE: Couldn't open/read memcheck error report")
      sys.exit()
  else:
    pass
  for line in report:
    if "FILE DESCRIPTORS:" in line:
      if fd_chk is not False:
        # match (first) numerical value
        _, phrase = line.split(':', 2)
        phrase = phrase.strip()
        value1 = re.search(r'[0-9]*\,?[0-9]* ', phrase)
        value1 = value1.group().replace(',','')
        # compare thresholds
        if int(value1) > int(fd_chk):
          log_data("Binary %s: Fd threshold exceeded for max file descriptors: Cur %s Max %s" % (str(path_chk), str(value1), int(fd_chk)))
        else:
          pass
      else:
        pass
    elif "HEAP SUMMARY:" in line:
      if heap_chk is not False:
        # get heap summary thresholds: <max allocs>,<max frees>
        mavalue, mfvalue = heap_chk.split(',', 2)
        # goto 2nd line after heading, search for values
        i = 1
        while i < 3:
          line = nextline(report)
          if i == 2:
            _, phrase1 = line.split(':', 2)
            phrase1 = phrase1.strip()          
            # get allocs from report
            phrase2 = re.search(r'[0-9]*\,?[0-9]* allocs', phrase1)
            value2, _ = phrase2.group().split(' ', 2)
            value2 = value2.replace(',','')
            # compare allocs to threshold
            if int(value2) > int(mavalue):
              log_data("Binary %s: Heap threshold exceeded for max heap allocs: Cur %s Max %s" % (str(path_chk), str(value2), str(mavalue)))   
            else:
              pass
            # get frees from report
            phrase2 = re.search(r'[0-9]*\,?[0-9]* frees', phrase1)
            value2, _ = phrase2.group().split(' ', 2)
            value2 = value2.replace(',','')
            # compare frees to threshold
            if int(value2) > int(mfvalue):
              log_data("Binary %s: Heap threshold exceeded for max heap frees: Cur %s Max %s" % (str(path_chk), str(value2), str(mfvalue)))
            else:
              pass
          # increment while loop
          i = i + 1
      else:
        pass
    elif "LEAK SUMMARY:" in line:
      if leak_chk is not False:
        # get leak thresholds: <max definitely lost>,<max indirectly lost>,<max possibly lost>,<max reachable>,<max suppressed>
        mdlvalue, milvalue, mplvalue, mrvalue, msvalue = leak_chk.split(',')      
        # for first five lines after heading, search each line for values
        i = 1
        while i < 6:
          line = nextline(report)
          if i == 1:
            # definitely lost bytes
            _, phrase = line.split(':', 2)
            phrase = phrase.strip()
            # get bytes from report
            value1 = re.search(r'[0-9]*\,?[0-9]* bytes', phrase)
            value1, _ = value1.group().split(' ', 2)
            value1 = value1.replace(',','')
            # compare definitely lost to threshold
            if int(value1) > int(mdlvalue):
              log_data("Binary %s: Leak threshold exceeded for max definitely lost bytes: Cur %s Max %s" % (str(path_chk), str(value1), str(mdlvalue)))
            else:
              pass
          elif i == 2:
            # indirectly lost bytes
            _, phrase = line.split(':', 2)
            phrase = phrase.strip()
            value1 = re.search(r'[0-9]*\,?[0-9]* bytes', phrase)
            value1, _ = value1.group().split(' ', 2)
            value1 = value1.replace(',','')
            # compare indirectly lost to threshold
            if int(value1) > int(milvalue):
              log_data("Binary %s: Leak threshold exceeded for max indirectly lost bytes: Cur %s Max %s" % (str(path_chk), str(value1), str(milvalue)))
            else:
              pass   
          elif i == 3:
            # possibly lost bytes
            _, phrase = line.split(':', 2)
            phrase = phrase.strip()
            value1 = re.search(r'[0-9]*\,?[0-9]* bytes', phrase)
            value1, _ = value1.group().split(' ', 2)
            value1 = value1.replace(',','')
            # compare possibly lost to threshold
            if int(value1) > int(mplvalue):
              log_data("Binary %s: Leak threshold exceeded for max possibly lost bytes: Cur %s Max %s" % (str(path_chk), str(value1), str(mplvalue)))
            else:
              pass
          elif i == 4:
            # still reachable bytes
            _, phrase = line.split(':', 2)
            phrase = phrase.strip()
            value1 = re.search(r'[0-9]*\,?[0-9]* bytes', phrase)
            value1, _ = value1.group().split(' ', 2)
            value1 = value1.replace(',','')
            # compare reachable to threshold
            if int(value1) > int(mrvalue):
              log_data("Binary %s: Leak threshold exceeded for max reachable bytes: Cur %s Max %s" % (str(path_chk), str(value1), str(mrvalue)))
            else:
              pass   
          elif i == 5:
            # suppressed bytes
            _, phrase = line.split(':', 2)
            phrase = phrase.strip()
            value1 = re.search(r'[0-9]*\,?[0-9]* bytes', phrase)
            value1, _ = value1.group().split(' ', 2)
            value1 = value1.replace(',','')
            # compare suppressed to threshold
            if int(value1) > int(msvalue):
              log_data("Binary %s: Leak threshold exceeded for max suppressed bytes: Cur %s Max %s" % (str(path_chk), str(value1), str(msvalue)))
            else:
              pass          
          else:
            pass
          # increment while loop
          i = i + 1
      else:
        pass
    elif "ERROR SUMMARY:" in line:
      if error_chk is not False:
        # get error summary thresholds: <max errors>,<max contexts>
        tevalue, tcvalue = error_chk.split(',', 2)
        # total errors
        value1 = re.search(r'[0-9]*\,?[0-9]* errors', line)
        value1, _ = value1.group().split(' ', 2)
        value1 = value1.replace(',','')
        # compare total errors to threshold
        if int(value1) > int(tevalue):
          log_data("Binary %s: Error threshold exceeded for max total errors: Cur %s Max %s" % (str(path_chk), str(value1), str(tevalue)))
        else:
          pass
        # total contexts
        value2 = re.search(r'[0-9]*\,?[0-9]* contexts', line)
        value2, _ = value2.group().split(' ', 2)
        value2 = value2.replace(',','')
        # compare total contexts to threshold
        if int(value2) > int(tcvalue):
          log_data("Binary %s: Error threshold exceeded for max total contexts: Cur %s Max %s" % (str(path_chk), str(value2), str(tcvalue)))
        else:
          pass
      else:
        pass
    else:
      pass

