#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

def red(str):
    print('\x1b[31m' + str + '\x1b[39m')

def green(str):
    print('\x1b[32m' + str + '\x1b[39m')

def yellow(str):
    print('\x1b[33m' + str + '\x1b[39m')

def blue(str):
    print('\x1b[34m' + str + '\x1b[39m')

def magenta(str):
    print('\x1b[35m' + str + '\x1b[39m')

def cyan(str):
    print('\x1b[36m' + str + '\x1b[39m')