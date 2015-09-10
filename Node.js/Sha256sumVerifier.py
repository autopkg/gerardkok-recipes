#!/usr/bin/python
#
# Copyright 2015 Gerard kok
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


from autopkglib import Processor, ProcessorError
import hashlib


__all__ = ["Sha256sumVerifier"]


class Sha256sumVerifier(Processor):
    description = "Verifies sha256sum of package against a given SHA256 checksum. Throws a ProcessorError on mismatch."
    input_variables = {
        "pkgpath": {
            "required": True,
            "description": "Package to checksum.",
        },
        "expected_sha256sum": {
            "required": True,
            "description": "Expected SHA256 checksum.",
        },
    }
    output_variables = {
    }
    
    __doc__ = description
    
    
    def sha256sum_from_pkg(self, pkgpath):
        sha256 = hashlib.sha256()
        f = open(pkgpath, 'rb')
        try:
            sha256.update(f.read())
        finally:
            f.close()
        return sha256.hexdigest()
    
    
    def main(self):
        pkgpath = self.env['pkgpath']
        self.output('Using pkgpath %s' % pkgpath)
        expected = self.env['expected_sha256sum']
        self.output('Using expected SHA256 checksum %s' % expected)

        sha256sum_from_pkg = self.sha256sum_from_pkg(pkgpath)
        self.output('SHA256 for %s: %s' % (pkgpath, sha256sum_from_pkg))
        if sha256sum_from_pkg == expected:
            self.output("SHA256 checksum matches")
        else:
            raise ProcessorError("SHA256 checksum mismatch")
   

if __name__ == '__main__':
    processor = Sha256sumVerifier()
    processor.execute_shell()
    
