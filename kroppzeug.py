#!/usr/bin/python3
# -*- coding: utf-8 -*-

# kroppzeug: Helps you to manage your server kindergarten!
#
# Copyright 2012-2014 Dan Luedtke <mail@danrl.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import string
import os
import time
import signal
import sys
from subprocess import call

# global variables
hosts           = []
error_message   = False
hostname        = False
ssh_config_file = os.getenv("HOME") + '/.ssh/config'

# colors, control sequences
TERM_RED        = '\033[91m'
TERM_GREEN      = '\033[92m'
TERM_YELLOW     = '\033[93m'
TERM_BLUE       = '\033[94m'
TERM_MAGENTA    = '\033[95m'
TERM_BOLD       = '\033[1m'
TERM_RESET      = '\033[0m'

# catch SIGINT (e.g. ctrl+c)
def signal_handler(signal, frame):
    os.system('clear')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# get terminal size
def get_termsize():
    global TERM_SIZEY, TERM_SIZEX
    y, x = os.popen('stty size', 'r').read().split()
    TERM_SIZEY = int(y)
    TERM_SIZEX = int(x)
    return

# read ssh hosts from config file
def parse_hosts(filename):
    i = -1
    inputfile = open(filename, 'r')
    for line in inputfile.readlines():
        # strip whitespaces
        line = line.strip()
        # extract options
        line = line.split(None, 1)
        # parse options
        if len(line) < 2:
            continue
        option = line[0]
        value = line[1]
        if option.lower() == 'host':
            shortcut = value
            description = ''
            update = False
            autocmd = False
            i += 1
        elif option.lower() == '#kroppzeug_description':
            description = value
        elif option.lower() == '#kroppzeug_update' and len(value) > 0:
            update = value
        elif option.lower() == '#kroppzeug_autocmd':
            autocmd = value
        elif option.lower() == '#kroppzeug_managed' and value.lower() == 'true':
            hosts.append([shortcut, description, update, autocmd])
    inputfile.close()


# print horizontal line
def print_hline():
    print(TERM_BOLD + TERM_GREEN + '─' * TERM_SIZEX + TERM_RESET)

# print header
def print_header():
    os.system('clear')
    print(TERM_BOLD + TERM_RED, end='')
    if hostname == True:
        print()
        print(os.getenv('HOSTNAME').center(TERM_SIZEX))
        print()
    else:
        print('┬┌─┬─┐┌─┐┌─┐┌─┐┌─┐┌─┐┬ ┬┌─┐'.center(TERM_SIZEX))
        print('├┴┐├┬┘│ │├─┘├─┘┌─┘├┤ │ ││ ┬'.center(TERM_SIZEX))
        print('┴ ┴┴└─└─┘┴  ┴  └─┘└─┘└─┘└─┘'.center(TERM_SIZEX))
    print_hline()

# print a list of available hosts
def print_hosts():
    shortcut_width = 11
    about_width = (TERM_SIZEX - 23) // 2
    i = -1
    for host in hosts:
        i += 1
        host_shortcut = host[0][:shortcut_width]
        if host[1] is not False:
            host_about = ' ' + host[1][:about_width]
        else:
            host_about = ' '
        out = ''
        out = out + TERM_BOLD + TERM_BLUE + host_shortcut.rjust(shortcut_width)
        out = out + TERM_RESET + host_about.ljust(about_width)
        if i % 2 == 0:
            print(out, end='')
        else:
            print(out)


def print_cmd():
    global error_message

    # position
    if error_message is not False:
        posx = str(TERM_SIZEY - 3)
    else:
        posx = str(TERM_SIZEY - 2)
    print('\033[' + posx + ';0f')
    print_hline()

    # error message
    if error_message is not False:
        print(TERM_BOLD + TERM_RED + error_message)
        error_message = False

    # command prompt
    print(TERM_BOLD + TERM_YELLOW + '(kroppzeug)$ ' + TERM_RESET, end='')


def connect_host(i):
    auto_command = hosts[i][3]
    shortcut = hosts[i][0]
    # craft shell command
    shell_command = 'ssh -v ' + shortcut
    if auto_command is not False:
        shell_command += ' -t "' + auto_command + '"'
    os.system('clear')
    print(TERM_YELLOW + shell_command + TERM_RESET)
    call(shell_command, shell=True)


def update_host(i):
    update_command = hosts[i][2]
    shortcut = hosts[i][0]
    # craft shell command
    shell_command = 'ssh -v ' + shortcut
    if update_command is not False:
        shell_command += ' -t "' + update_command + '"'
        os.system('clear')
        print(TERM_YELLOW + shell_command + TERM_RESET)
        call(shell_command, shell=True)


def shortcut_to_id(shortcut):
    i = -1
    for host in hosts:
        i += 1
        if host[0] == shortcut:
            return i
    return False



parse_hosts(ssh_config_file)

while True:
    # build screen
    get_termsize()
    print_header()
    print_hosts()
    print_cmd()

    # input
    try:
        cmd = input('')
    except EOFError:
        cmd = '!exit'

    # execute
    cmds = cmd.split(None, 1)
    if len(cmd) < 1:
        pass
    elif cmd == '!exit':
        os.system('clear')
        quit()
    elif cmd == '!hostname':
        hostname = not hostname
    elif cmd == '!update-all':
        for i in range(len(hosts)):
            update_host(i)
            print_hline()
    elif cmd.startswith('!update') and len(cmds) <= 1:
        error_message = 'Oh no, missing server name!'
    elif cmd.startswith('!update') and len(cmds) > 1:
        i = shortcut_to_id(cmds[1])
        if i is not False:
            update_host(i)
            time.sleep(3)
        else:
            error_message = 'Sorry, don\'t know that server name!'
    elif cmd.startswith('!'):
        error_message = 'Try \'!hostname\', \'!update\', ' + \
        '\'!update-all\' or \'!exit\'...'
    else:
        i = shortcut_to_id(cmd)
        if i is not False:
            connect_host(i)
            time.sleep(1)
        else:
            error_message = 'Sorry, don\'t know that server name!'


