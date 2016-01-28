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

import os
import shutil
import subprocess
import re

from autopkglib import Processor, ProcessorError

__all__ = ["SVNUpdater"]


def is_working_copy(path):
    return os.path.isdir(path) and os.path.isdir(os.path.join(path, '.svn'))


def create_dir(path):
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)
    
    
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
        "updated": {
            "description": "if the working copy has been updated"
        },
        "revision": {
            "description": "the revision the working copy is updated to"
        }
    }

    
    REVISION_RE = re.compile('^Revision:\s+(\d+)')

    
    def run_svn_cmd(self, params, working_copy_dir):
        svn_cmd = ['/usr/bin/svn', '--non-interactive']
        if trust_server_cert():
            svn_cmd.extend(['--trust-server-cert'])
        svn_cmd.extend(params)
        p = subprocess.Popen(svn_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=working_copy_dir)
        return p.communicate()
    
    
    def get_working_copy_dir(self):
        if 'working_copy_dir' in self.env:
            return self.env['working_copy_dir']
        else:
            return os.path.join(self.env.get('RECIPE_CACHE_DIR'), 'downloads')
        
        
    def trust_server_cert(self):
        if 'trust_server_cert' in self.env:
            return self.env['trust_server_cert']
        else:
            return True
        
        
    def get_latest_rev(self):
        (out, err) = self.run_svn_cmd(['info', '-r', 'HEAD'])
        match = REVISION_RE.search(out)
        return match.group(match.lastindex or 0)
    
    
    def get_current_ref(self):
        (out, err) = self.run_svn_cmd(['info'])
        match = REVISION_RE.search(out)
        return match.group(match.lastindex or 0)
    
    
    def update_working_copy(self, working_copy_dir):
        self.run_svn_cmd(['update'], working_copy_dir)
        
        
    def checkout_working_copy(self, working_copy_dir):    
        self.run_svn_cmd(['checkout'], working_copy_dir)


    def main(self):
        source = self.env['source']
        working_copy_dir = self.get_working_copy_dir()
        if is_working_copy(working_copy_dir):
            latest_rev = self.get_latest_rev()
            current_rev = self.get_current_rev()
            if latest_rev > current_rev:
                self.update_working_copy(working_copy_dir)
                self.env['updated'] = True
            else:
                self.env['updated'] = False
        else:
            create_dir(working_copy_dir)
            self.checkout_working_copy(working_copy_dir)
            self.env['updated'] = True
 
                
if __name__ == '__main__':
    processor = SVNUpdater()
    processor.execute_shell()
    