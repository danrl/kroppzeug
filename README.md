kroppzeug
=========

Helps you to manage your server kindergarten!


About
-----

Kroppzeug helps you to manage your server kindergarten by parsing your
SSH config file and providing shortcuts for connecting to a server or
updating one or all servers. Kroppzeug is perfect for managing a few to
a dozent servers but may be no fun when you have to orchestrate hundreds
or thousands of servers. It requires that you use a terminal multiplexer
like screen or tmux after connecting to a server.
Trivia: 'Kroppzeug' is an often lovingly and sometimes snidely used
low-german term for ones offspring.


Configuration
-------------

Just annotate you SSH config file with comments starting with '#kroppzeug_'.

* ``#kroppzeug_description`` A description of the server. Optional.
* ``#kroppzeug_update`` Commands to execute when using the update function.
* ``#kroppzeug_autocmd`` Commands to execute after the connection has been made.
* ``#kroppzeug_managed`` Set to 'true' to allow kroppzeug to list this server.


````
Host cloud
    Hostname                cloud.nonattached.net
    User                    user1
    Port                    2222
    #kroppzeug_description  OwnCloud Server
    #kroppzeug_update       apt-get update; apt-get upgrade
    #kroppzeug_autocmd      tmux attach || tmux
    #kroppzeug_managed      true
````

Commands
--------

To connect to a server just type the coresponding [server name].
To update a server use 'update [server name]' or 'update all' to update
all servers. If you are unsure from which host you are connecting, e.g.
because you own too many computers, type 'whereami' to toggle the hostname
in the title area.


Screenshot
----------
````
                     ┬┌─┬─┐┌─┐┌─┐┌─┐┌─┐┌─┐┬ ┬┌─┐
                     ├┴┐├┬┘│ │├─┘├─┘┌─┘├┤ │ ││ ┬
                     ┴ ┴┴└─└─┘┴  ┴  └─┘└─┘└─┘└─┘
─────────────────────────────────────────────────────────────────────
     nan-gw Gateway Frankfurt         nan-vpn VPN Terminator IPMI
     puppet Puppet Master                  ns Nameserver (master)
       dns1 RDNSS 1                      dns2 RDNSS 2
       mail Mailserver                    www Webserver
     nethop Shell                         gws Gateway E.
    storage Storage E.                sealand Backup Server
        irc IRC Server                  cloud OwnCloud Server
        git GIT Repository                jmp VPN server
   workshop IPv6-Workshop

─────────────────────────────────────────────────────────────────────

$
````

License
-------

Copyright 2012-2014 Dan Luedtke <mail@danrl.de>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
