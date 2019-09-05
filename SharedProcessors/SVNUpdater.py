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
import shutil
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["SVNUpdater"]


def is_working_copy(path):
    return os.path.isdir(path) and os.path.isdir(os.path.join(path, '.svn'))


def get_rev(str):
    result = re.search(r'^Revision:\s+(\d+)', str, re.MULTILINE)
    if result:
        return result.group(1)
    else:
        return 0
    
    
class SVNUpdater(Processor):
    """Keeps an svn working copy up to date."""
    description = __doc__
    input_variables = {
        "source": {
            "required": True,
            "description": "svn repository url"
        },
        "working_copy_dir": {
            "required": False,
            "description": "path to working copy"
        },
        "trust_server_cert": {
            "required": False,
            "description": "whether to trust the server certificate"
        }
    }
    output_variables = {
        "download_changed": {
            "description": "whether the working copy has been updated"
        },
        "revision": {
            "description": "the revision the working copy is updated to"
        },
        "svn_updater_summary_result": {
            "description": "interesting results"
        }
    }

    
    def run_svn_cmd(self, params, working_copy_dir=None):
        svn_cmd = ['/usr/bin/svn', '--non-interactive']
        if self.trust_server_cert():
            svn_cmd.extend(['--trust-server-cert'])
        svn_cmd.extend(params)
        p = subprocess.Popen(svn_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=working_copy_dir)
        return p.communicate()
    
    
    def get_working_copy_dir(self, source):
        if 'working_copy_dir' in self.env:
            return self.env['working_copy_dir']
        else:
            return os.path.join(self.env.get('RECIPE_CACHE_DIR'), 'downloads', os.path.basename(source))
       
        
    def trust_server_cert(self):
        if 'trust_server_cert' in self.env:
            return self.env['trust_server_cert']
        else:
            return True
        
        
    def get_latest_rev(self, source):
        (out, err) = self.run_svn_cmd(['info', '-r', 'HEAD', source])
        return get_rev(out)
        
        
    def get_current_rev(self, working_copy_dir):
        (out, err) = self.run_svn_cmd(['info', working_copy_dir])
        return get_rev(out)
        
        
    def main(self):
        source = self.env['source']
        working_copy_dir = self.get_working_copy_dir(source)
        self.env['revision'] = self.get_latest_rev(source)
        if is_working_copy(working_copy_dir):
            current_rev = self.get_current_rev(working_copy_dir)
            self.run_svn_cmd(['update'], working_copy_dir)
            self.env['download_changed'] = self.env['revision'] > current_rev
        else:
            # is working_copy_dir is not a working copy, make sure it's out of the way
            shutil.rmtree(working_copy_dir, ignore_errors=True)
            self.run_svn_cmd(['checkout', source, working_copy_dir])
            self.env['download_changed'] = True
        if self.env['download_changed']:
            self.env['svn_updater_summary_result'] = {
                'summary_text': 'The following working copy was updated:',
                'data': {
                    'working_copy_path': working_copy_dir,
                }
            }
 
                
if __name__ == '__main__':
    processor = SVNUpdater()
    processor.execute_shell()
