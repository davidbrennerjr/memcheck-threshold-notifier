#!/usr/bin/python3.5

################################################################################
# memcheck_threshold_notifier.py - Notify when memcheck errors exceed thresholds
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
#
# Usage
# ./memcheck_threshold_notifier.py /path/to/binary <options>
#
# Configuration Options
# --log-file          /path/to/log
# --fd-threshold      <max file descriptors>
# --heap-threshold    <max allocs>,
#                     <max frees>
# --leak-threshold    <max definitely lost bytes>,
#                     <max indirectly lost bytes>,
#                     <max possibly lost bytes>,
#                     <max reachable bytes>,
#                     <max suppressed bytes>
# --error-threshold   <max errors>,
#                     <max contexts>
################################################################################ 

if __name__ == "__main__":
  # import required modules 
  try:
    import sys
    import library
  except ImportError:
    print("FAILURE: Failed to import required library module")
    sys.exit()
  library.run_memcheck()
  library.parse_report()
  sys.exit()

