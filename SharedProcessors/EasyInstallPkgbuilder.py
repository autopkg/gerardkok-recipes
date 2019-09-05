#!/usr/bin/env python
#
# Copyright 2015 Gerard Kok
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

import os
import shutil
import subprocess
import tempfile

from autopkglib import Processor, ProcessorError

__all__ = ["EasyInstallPkgbuilder"]

class EasyInstallPkgbuilder(Processor):
    """Creates a package that installs a python module using easy_install."""
    description = __doc__
    input_variables = {
        "python_pkg_path": {
            "required": True,
            "description": "Path to a python package",
        },
        "identifier": {
            "required": True,
            "description": "Unique identifier for the package created",
        },
        "version": {
            "required": True,
            "description": "Version for the package created",
        },
        "pkgpath": {
            "required": True,
            "description": "Path to the package created",
        }
    }
    output_variables = {
    }

    def pkgbuild(self, scriptsdir, identifier, version, pkgpath):
        if os.path.exists('/usr/bin/pkgbuild'):
            try:
                root = tempfile.mkdtemp()
                pkgbuildcmd = ['/usr/bin/pkgbuild',
                               '--root', root,
                               '--scripts', scriptsdir,
                               '--identifier', identifier,
                               '--version', version,
                               pkgpath]
                p = subprocess.Popen(pkgbuildcmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                (out, err) = p.communicate()
                if p.returncode != 0:
                    raise ProcessorError("pkgbuild of %s failed: %s"
                                         % (pkgpath, err))
            finally:
                shutil.rmtree(root)
        else:
             raise ProcessorError(
                 "Can't find binary %s: %s" % ('/usr/bin/pkgbuild', e.strerror))


    def make_postinstall_script(self, scriptsdir, modulepath):
        modulename = os.path.basename(modulepath)
        shutil.copyfile(modulepath, os.path.join(scriptsdir, modulename))
        postinstall_path = os.path.join(scriptsdir, 'postinstall')
        with open(postinstall_path, 'w') as postinstall_script:
            postinstall_script.write("#!/bin/sh\n\nworking_dir=`/usr/bin/dirname \"${0}\"`\n/usr/bin/easy_install \"${working_dir}/%s\"\n" % modulename)
        os.chmod(postinstall_path, 0o755)


    def main(self):
        python_pkg_path = self.env['python_pkg_path']
        identifier = self.env['identifier']
        version = self.env['version']
        pkgpath = self.env['pkgpath']
        try:
            scriptsdir = tempfile.mkdtemp()
            self.make_postinstall_script(scriptsdir, python_pkg_path)
            self.pkgbuild(scriptsdir, identifier, version, pkgpath)
        finally:
            shutil.rmtree(scriptsdir)


if __name__ == '__main__':
    processor = EasyInstallScriptCreator()
    processor.execute_shell()
