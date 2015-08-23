#!/usr/bin/python
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


from autopkglib import Processor, ProcessorError


__all__ = ["VersionFixer"]


class VersionFixer(Processor):
    description = "Extracts version from version strings like '<pkg>-<version>'."
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
    
    __doc__ = description
    
    
    def main(self):
        version = self.env["version"]
        self.env["fixedversion"] = version.split('-')[1]
   

if __name__ == '__main__':
    processor = VersionFixer()
    processor.execute_shell()
    