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


__all__ = ["Sha1sumVerifier"]


class Sha1sumVerifier(Processor):
    description = "Verifies sha1sum of package against a given SHA1 checksum. Throws a ProcessorError on mismatch."
    input_variables = {
        "pkgpath": {
            "required": True,
            "description": "Package to checksum.",
        },
        "expected_sha1sum": {
            "required": True,
            "description": "Expected SHA1 checksum.",
        },
    }
    output_variables = {
    }
    
    __doc__ = description
    
    
    def sha1sum_from_pkg(self, pkgpath):
        sha1 = hashlib.sha1()
        f = open(pkgpath, 'rb')
        try:
            sha1.update(f.read())
        finally:
            f.close()
        return sha1.hexdigest()
    
    
    def main(self):
        pkgpath = self.env['pkgpath']
        self.output('Using pkgpath %s' % pkgpath)
        expected = self.env['expected_sha1sum']
        self.output('Using expected SHA1 checksum %s' % expected)

        sha1sum_from_pkg = self.sha1sum_from_pkg(pkgpath)
        self.output('SHA1 for %s: %s' % (pkgpath, sha1sum_from_pkg))
        if sha1sum_from_pkg == expected:
            self.output("SHA1 checksum matches")
        else:
            raise ProcessorError("SHA1 checksum mismatch")
   

if __name__ == '__main__':
    processor = Sha1sumVerifier()
    processor.execute_shell()
    