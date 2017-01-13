# Memcheck Threshold Notifier #

An application wrapper of Valgrind's Memcheck that sends detailed error messages to rsyslog when the memcheck errors of a C/C++ binary exceed specified thresholds.

## Features ##

* __Threshold Checks__

  * Memory heap checking of maximum number of allocations via malloc()
  * Memory heap checking of maximum number of deallocations via free()
  * Memory leak checking of maximum number of definitely lost bytes
  * Memory leak checking of maximum number of indirectly lost bytes
  * Memory leak checking of maximum number of possibly lost bytes
  * Memory leak checking of maximum number of reachable bytes
  * Memory leak checking of maximum number of suppressed bytes
  * Error summary checking of maximum number of total errors
  * Error summary checking of maximum number of total contexts 

* __Notifications__

  * Detailed messages sent to rsyslog service
  * Timestamped detailed messages sent to "logs/memcheck" whenever rsyslog is unavailable
  * Message format can be customized inline to include
    * Absolute path to the C/C++ binary that memcheck analyzes
    * Absolute path to the log file memcheck generates for the binary (for further analysis) 
    * Custom error message that indicates what caused the notification
    * Specific values used in current/max thresholds

* __Builtin Features__

  * Traces into sub-processes of multi-process programs
  * Shows each file descriptor with a stack backtrace of any details relating to the file descriptor
  * Searches for memory leaks when the C/C++ binary is finished running
  * Shows possible memory leaks as lost bytes per block
  * Enables all leak check heuristics to determine whether interior pointers of blocks are reachable
  * Marks partially loaded addresses of bytes as illegal-address errors 
  * Traces origins of all uninitialized value errors to heap blocks, stack allocations, client requests, or miscellaneous other sources 

## Usage ##

Memcheck Threshold Notifier requires that the user specify the absolute path to the binary memcheck should analyze for memory errors and the absolute path to the log file memcheck should use to save its memory error report. Its default behavior is analyzing the specified binary and saving the error report to the specified log file, without checking thresholds and sending notification. It supports additional options for checking the maximum number of various possible memory errors. 

__`./memcheck_threshold_notifier.py /path/to/binary --log-file /path/to/log <options>`__

## Options ##

__`--fd-threshold <max file descriptors>`__

Checks the maximum number of file descriptors. The value of this option must be one whole number.


__`--heap-threshold <max allocs>,<max frees>`__

Checks both the maximum number of heap allocations and the maximum number of heap deallocations. The value of this option must be two whole numbers in order separated by a single comma. 


__`--leak-threshold <max definitely lost bytes>,<max indirectly lost bytes>,<max possibly lost bytes>,<max reachable bytes>,<max suppressed bytes>`__

Checks the following list of maximum numbers of possible memory leaks. The value of this option must be a list of five whole numbers in order separated by commas.


__`--error-threshold <max errors>,<max contexts>`__

Checks both the maximum number of reported errors and the maximum number of reported error contexts. The value of this option must be two whole numbers in order separated by a single comma.


## Notifications ##

When a threshold is exceeded a detailed error message is sent to the local rsyslog service. If the rsyslog service hasn't been installed or the rsyslog service isn't running, the error message is sent to a timestamped file in the directory "logs/memcheck".

