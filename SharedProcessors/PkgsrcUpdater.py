#!/usr/bin/env python
#
# Copyright 2016 Gerard Kok
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

# work in progress, do not use

from __future__ import absolute_import

import os
import re
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["PkgsrcUpdater"]


def is_working_copy(path):
    return os.path.isdir(path) and os.path.isdir(os.path.join(path, '.svn'))


def get_rev(str):
    result = re.search(r'^Revision:\s+(\d+)', str, re.MULTILINE)
    if result:
        return result.group(1)
    else:
        return 0


class PkgsrcUpdater(Processor):
    """Keeps a pkgsrc package up to date."""
    description = __doc__
    input_variables = {
        "pkg": {
            "required": True,
            "description": "pkgsrc package to manage"
        },
    }
    output_variables = {
        "download_changed": {
            "description": "whether the package has been updated"
        },
        "version": {
            "description": "the version the package is updated to"
        },
        "pkgsrc_updater_summary_result": {
            "description": "interesting results"
        }
    }


    def get_installed_version(self, pkg):
        pkg_info_cmd = ['/opt/pkg/bin/pkg_info', '-E', pkg]
        p = subprocess.Popen(pkg_info_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        return out.split('-')[1]


    def is_installed(self, pkg):
        pkg_info_cmd = ['/opt/pkg/bin/pkg_info', '-E', pkg]
        p = subprocess.Popen(pkg_info_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        return p.returncode == 0


    def run_update(self, pkg):
        pkgin_cmd = ['/opt/pkg/bin/pkgin', 'update', '-y', pkg]
        p = subprocess.Popen(pkgin_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        return p.communicate()

    def run_install(self, pkg):
        pkgin_cmd = ['/opt/pkg/bin/pkgin', 'install', '-y', pkg]
        p = subprocess.Popen(pkgin_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        return p.communicate()


    def main(self):
        pkg = self.env['pkg']
        if self.is_installed(pkg):
            current_version = self.get_current_version(pkg)
            self.run_update(pkg)
        else:
            current_version = 0
            self.run_install(pkg)
        self.env['version'] = self.get_current_version(pkg)
        self.env['download_changed'] = self.env['version'] > current_rev
        if self.env['download_changed']:
            self.env['pkgsrc_updater_summary_result'] = {
                'summary_text': 'The following pkg was updated:',
                'data': {
                    'pkg': pkg,
                }
            }


if __name__ == '__main__':
    processor = PkgsrcUpdater()
    processor.execute_shell()
