#!/usr/local/autopkg/python
#
# Copyright 2014 Gerard kok
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


from __future__ import absolute_import

from autopkglib import Processor, ProcessorError

__all__ = ["VersionFixer"]


class VersionFixer(Processor):
    """Extracts proper version from strings like '<pkg>-<version>'. If the original can't be split, return the original."""
    description = __doc__
    input_variables = {
        "version": {
            "required": True,
            "description": "Original version.",
        },
    }
    output_variables = {
        "fixedversion": {
            "description": "Fixed version.",
        },
    }
    
    
    def main(self):
        version = self.env["version"]
        try:
            self.env["fixedversion"] = version.split('-')[1]
        except IndexError:
            self.env["fixedversion"] = version
   

if __name__ == '__main__':
    processor = VersionFixer()
    processor.execute_shell()
