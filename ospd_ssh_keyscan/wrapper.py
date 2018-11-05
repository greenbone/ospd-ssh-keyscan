# -*- coding: utf-8 -*-
# Description:
# Setup for the OSP ssh-keyscan Server
#
# Authors:
# Jan-Oliver Wagner <Jan-Oliver.Wagner@greenbone.net>
#
# Copyright:
# Copyright (C) 2015 Greenbone Networks GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.

from ospd.ospd import OSPDaemon
from ospd.misc import main as daemon_main
from ospd_ssh_keyscan import __version__
import subprocess

OSPD_DESC = """
This scanner runs the tool 'ssh-keyscan' to scan the target hosts.
The target port list is ignored, instead the ssh port is given as
a explicit scan configuration parameter.

This tool is available for most operating systems as part of the OpenSSH package.
It gathers the public ssh host keys of a number of hosts.

The current version of ospd-ssh-keyscan is a very simple one, collecting the
keys as host details. Optionally, the keys are additionally dumped in log results.
"""

OSPD_PARAMS = {
    'sshport': {
        'type': 'integer',
        'name': 'SSH Port',
        'default': 22,
        'mandatory': 1,
        'description': 'The SSH Port to connect to on the remote hosts.',
    },
    'sshkeyaslog': {
        'type': 'boolean',
        'name': 'Dump keys as log results',
        'default': 0,
        'mandatory': 0,
        'description': 'Whether to create log results with key details.',
    },
}


class OSPDsshkeyscan(OSPDaemon):

    """ Class for ospd-ssh-keyscan daemon. """

    def __init__(self, certfile, keyfile, cafile):
        """ Initializes the ospd-ssh-keyscan daemon's internal data. """
        super(OSPDsshkeyscan, self).__init__(certfile=certfile, keyfile=keyfile,
                                             cafile=cafile)
        self.server_version = __version__
        self.scanner_info['name'] = 'ssh-keyscan'
        self.scanner_info['version'] = 'Not available'
        self.scanner_info['description'] = OSPD_DESC
        for name, param in OSPD_PARAMS.items():
            self.add_scanner_param(name, param)

    def check(self):
        """ Checks that ssh-keyscan command line tool is found and is executable. """

        try:
            subprocess.check_output(['ssh-keyscan'], stderr=subprocess.STDOUT)
        except OSError:
            # the command is not available
            return False
        except subprocess.CalledProcessError:
            # the command is there, it is just unhappy without a parameter
            pass

        return True

    def exec_scan(self, scan_id, target):
        """ Starts the ssh-keyscan scanner for scan_id scan. """

        options = self.get_scan_options(scan_id)
        port = options.get('sshport')
        result = subprocess.check_output(['ssh-keyscan', '-p %d' % port, target],
                                         stderr=subprocess.STDOUT)

        if result is None:
            self.add_scan_error(scan_id, host=target,
                                value="A problem occurred trying to execute 'ssh-keyscan'.")
            self.add_scan_error(scan_id, host=target,
                                value="The result of 'ssh-keyscan' was empty.")
            return 2

        # initialize the key data collector
        key_data = []

        # initialize the parse error lines
        parse_errors = []

        # parse the output of the ssh-keyscan command
        for line in result.splitlines():
            if line[0] == '#':
                continue
            try:
                host, keytype, key = line.split()
            except ValueError:
                parse_errors.append(line)
                continue

            self.add_scan_host_detail(scan_id, host=host, name="ssh-key",
                                      value='%d %s %s' % (port, keytype, key))
            key_data.append(line)

        # Create a general log entry about executing ssh-keyscan
        # It is important to send at least one result, else
        # the host details won't be stored.
        self.add_scan_log(scan_id, host=target, name='ssh-keyscan summary',
                          value='Via ssh-keyscan %d public ssh keys were found at port %d.' % (len(key_data), port))

        # In case parse errors occurred, report them a error message
        if len(parse_errors) > 0:
            self.add_scan_error(scan_id, host=target,
                                value='The following lines caused parse errors:\n\n%s' % '\n'.join(parse_errors))

        if options.get('sshkeyaslog'):
            self.add_scan_log(scan_id, host=target, name='ssh-keyscan key dump',
                              value='Via ssh-keyscan found keys:\n\n%s' % '\n'.join(key_data))

        return 1


def main():
    """ OSP ssh-keyscan main function. """
    daemon_main('OSPD - ssh-keyscan wrapper', OSPDsshkeyscan)
