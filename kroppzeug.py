#!/usr/bin/env python3
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
from socket import gethostname

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
    y, x = os.popen('stty size', 'r').read().split()
    return int(x), int(y)

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
        elif option.lower() == '#kf_description':
            description = value
        elif option.lower() == '#kf_update' and len(value) > 0:
            update = value
        elif option.lower() == '#kf_autocmd':
            autocmd = value
        elif option.lower() == '#kf_managed' and value.lower() == 'true':
            hosts.append([shortcut, description, update, autocmd])
    inputfile.close()


# print horizontal line
def print_hline():
    termx, termy = get_termsize()
    print(TERM_BOLD + TERM_GREEN + '-' * termx + TERM_RESET)


# print header
def print_header():
    global hostname
    termx, termy = get_termsize()

    os.system('clear')
    print(TERM_BOLD + TERM_RED, end='')
    print()
    if hostname is True:
        print(gethostname().center(termx))
    else:
        print('K R O P P Z E U G'.center(termx))
    print()
    print_hline()


# print a list of available hosts
def print_hosts():
    termx, termy = get_termsize()

    # shortcut length
    swidth = 16

    # description length
    dwidth = (termx - ((swidth + 3) * 2)) // 2

    # print the hosts as 2 columns
    i = -1
    for host in hosts:
        i += 1
        shortcut = host[0][:swidth]
        if host[1] is not False:
            desription = ' ' + host[1][:dwidth]
        else:
            desription = ' '
        out = ''
        out = out + TERM_BOLD + TERM_BLUE + shortcut.rjust(swidth)
        out = out + TERM_RESET + desription.ljust(dwidth)
        if i % 2 == 0:
            print(out, end='')
        else:
            print(out)


def print_prompt():
    global error_message
    termx, termy = get_termsize()

    # position
    if error_message is not False:
        posx = str(termy - 3)
    else:
        posx = str(termy - 2)
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
    print_header()
    print_hosts()
    print_prompt()

    # input
    try:
        cmd = input('')
    except EOFError:
        cmd = '!exit'

    # execute
    cmds = cmd.split(None, 1)
    if len(cmd) < 1:
        pass

    elif cmd == '!e' or cmd == '!exit':
        os.system('clear')
        quit()

    elif cmd == '!h' or cmd == '!hostname':
        hostname = not hostname

    elif cmd == '!ua' or cmd == '!update-all':
        for i in range(len(hosts)):
            update_host(i)
            print_hline()

    elif cmds[0] == '!update' or cmds[0] == '!u':
        if len(cmds) <= 1:
            error_message = 'Oh no, missing server name!'
        else:
            i = shortcut_to_id(cmds[1])
            if i is False:
                error_message = 'Sorry, don\'t know that server name!'
            else:
                update_host(i)
                time.sleep(3)

    elif cmd.startswith('!'):
        error_message = 'Try \'!hostname\', \'!update\', ' + \
        '\'!update-all\' or \'!exit\'...'

    else:
        i = shortcut_to_id(cmd)
        if i is False:
            error_message = 'Sorry, don\'t know that server name!'
        else:
            connect_host(i)
            time.sleep(1)
