#!/usr/bin/env python

import sys, os, pstats
exc_info = sys.exc_info()
print 'Content-Type: text/plain\n'
p=pstats.Stats('cProfile.out')
p.strip_dirs().sort_stats('time').print_stats()