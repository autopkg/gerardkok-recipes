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
from tempfile import mkstemp
from shutil import move
from os import remove, close, chmod



__all__ = ["PackageInfoVersionFixer"]


class PackageInfoVersionFixer(Processor):
    description = "Sets the correct version in the PackageInfo file of local.pkg."
    input_variables = {
        "packageinfo": {
            "required": True,
            "description": "path to the PackageInfo file to fix the version for.",
        },
        "version": {
            "required": True,
            "description": "Version to set in the PackageInfo file.",
        },
    }
    output_variables = {
    }
    
    __doc__ = description
    
    
    def replace(self, file_path, pattern, subst):
        fh, abs_path = mkstemp()
        with open(abs_path, 'w') as new_file:
            with open(file_path) as old_file:
                for line in old_file:
                    new_file.write(line.replace(pattern, subst))
        close(fh)
        remove(file_path)
        move(abs_path, file_path)
        chmod(file_path, 0644)
    
    
    def main(self):
        version = self.env["version"]
        packageinfo = self.env["packageinfo"]
        self.replace(packageinfo, "version=\"1.0\"", "version=\"" + version + "\"")
   

if __name__ == '__main__':
    processor = PackageInfoVersionFixer()
    processor.execute_shell()
    
