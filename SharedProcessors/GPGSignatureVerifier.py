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


def check_for_goodsig(string):
    return re.search("^\\[GNUPG:\\] GOODSIG ([0-9A-F]{8,})", string, re.M)


class GPGSignatureVerifier(Processor):
    """Verifies a gpg signature. Succeeds if gpg is not installed, or if the signature is good. Fails otherwise."""
    description = __doc__
    input_variables = {
        "gpg_path": {
            "required": False,
            "default": '/usr/local/bin/gpg',
            "description": "location of the gpg binary"
        },
        "public_key_id": {
            "required": True,
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
        "pathname": {
            "description": "path to the distribution file."
        }
    }
    

    def gpg_found(self):
        gpg_version_cmd = [self.env['gpg_path'], '--version']
        try:
            with open(os.devnull, "w") as devnull:
                subprocess.call(gpg_version_cmd, stdout=devnull, stderr=devnull)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                return False
            else:
                raise ProcessorError("Finding gpg executable failed")
        return True
    
    
    def import_key(self):
        gpg_import_cmd = [self.env['gpg_path'], '--recv-keys', self.env['public_key_id']]
        try:
            with open(os.devnull, "w") as devnull:
                subprocess.call(gpg_import_cmd, stdout=devnull, stderr=devnull)
        except OSError as e:
            raise ProcessorError("Importing public key failed")
        
        
    def verify(self):
        gpg_verify_cmd = [self.env['gpg_path'], '--status-fd', '1', '--verify', self.env['signature_file'], self.env['distribution_file']]
        try:
            proc = subprocess.Popen(gpg_verify_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (output, error) = proc.communicate()
            if proc.returncode:
                raise ProcessorError("Verifying signature failed")
            return check_for_goodsig(output)
        except:
            raise ProcessorError("Verifying signature failed")

    
    def main(self):
        self.env['pathname'] = self.env['distribution_file']
        if self.gpg_found():
            self.import_key()
            if self.verify():
                self.output("Good signature for %s" % self.env['distribution_file'])
            else:
                raise ProcessorError("Bad signature")
        else:
            self.output("gpg executable not found, therefore assuming signature for %s is good" % self.env['distribution_file'])


if __name__ == '__main__':
    processor = GPGSignatureVerifier()
    processor.execute_shell()
    