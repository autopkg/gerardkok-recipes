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


__all__ = ["GPGSignatureVerifier"]


class GPGSignatureVerifier(Processor):
    """Verifies a gpg signature."""
    description = __doc__
    input_variables = {
        "gpg_path": {
            "required": False,
            "default": '/usr/local/bin/gpg',
            "description": "location of the gpg binary"
        },
        "public_key_id": {
            "required": False,
            "description": "public key id to import"
        },
        "distribution_file": {
            "required": True,
            "description": "file to verify"
        },
        "signature_file": {
            "required": True,
            "description": "file with signature"
        }
    }
    output_variables = {
    }

    
    def main(self):
        gpg_import_cmd = [self.env['gpg_path'], '--recv-keys', self.env['public_key_id']]
        gpg_verify_cmd = [self.env['gpg_path'],
                    '--status-fd', '1', '--verify',
                    self.env['signature_file'],
                    self.env['distribution_file']]
        try:
            subprocess.call(gpg_import_cmd)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                self.output("No gpg executable found, exiting without checking integrity")
                exit(0)
            else:
                raise ProcessorError("Importing public key failed")
        try:
            proc = subprocess.Popen(gpg_verify_cmd,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (output, error) = proc.communicate()
            if (output.find('GOODSIG') < 0):
                raise ProcessorError("Verifying signature failed")
        except:
            raise ProcessorError("Verifying signature failed")
            
 
                
if __name__ == '__main__':
    processor = GPGSignatureVerifier()
    processor.execute_shell()
    