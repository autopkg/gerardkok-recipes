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
import subprocess
import os


__all__ = ["ProductBuilder"]


class ProductBuilder(Processor):
    description = "Build a package using productbuild."
    input_variables = {
        "distribution": {
            "required": True,
            "description": "path to the Distribution file.",
        },
        "resources": {
            "required": True,
            "description": "path to the Resources folder.",
        },
        "identifier": {
            "required": True,
            "description": "package identifier.",
        },
        "package_path": {
            "required": True,
            "description": "path to packages to include.",
        },
        "output_path": {
            "required": True,
            "description": "path to the package that is created.",
        },

    }
    output_variables = {
    }
    
    __doc__ = description
    
    
    def productbuild(self, distribution, resources, identifier, package_path, output_path):
        if os.path.exists('/usr/bin/productbuild'):
             pkgbuildcmd = ['/usr/bin/productbuild',
                            '--distribution', distribution,
                            '--resources', resources,
                            '--identifier', identifier,
                            '--package-path', package_path,
                            output_path]
             p = subprocess.Popen(pkgbuildcmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
             (out, err) = p.communicate()
             if p.returncode != 0:
                 raise ProcessorError("productbuild of %s failed: %s"
                                     % (pkgpath, err))
        else:
             raise ProcessorError(
                 "Can't find binary %s: %s" % ('/usr/bin/pkgbuild', e.strerror))
    
    
    def main(self):
        distribution = self.env["distribution"]
        resources = self.env["resources"]
        identifier = self.env["identifier"]
        package_path = self.env["package_path"]
        output_path = self.env["output_path"]
        self.productbuild(distribution, resources, identifier, package_path, output_path)
   

if __name__ == '__main__':
    processor = ProductBuilder()
    processor.execute_shell()
    
