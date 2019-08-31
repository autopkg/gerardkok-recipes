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


from __future__ import absolute_import
from autopkglib import Processor, ProcessorError
import subprocess
import re


__all__ = ["JenkinsURLProvider"]


def get_location(str):
    result = re.search(r'^Location:\s+(\S+)', str, re.MULTILINE)
    if result:
        return result.group(1)
    else:
        return None
    
    
def get_version(str):
    result = re.search(r'^http.+/jenkins-([0-9\.]+)\.pkg', str)
    if result:
        return result.group(1)
    else:
        return None


class JenkinsURLProvider(Processor):
    description = "Returns url to the latest Jenkins package."
    input_variables = {
        "base_url": {
            "required": False,
            "default": "http://mirrors.jenkins-ci.org/osx/latest",
            "description": "Url redirecting to actual download Url. Defaults to 'http://mirrors.jenkins-ci.org/osx/latest'.",
        },
        "CURL_PATH": {
            "required": False,
            "default": "/usr/bin/curl",
            "description": "Path to curl binary. Defaults to /usr/bin/curl."
        }
    }
    output_variables = {
        "url": {
            "description": "download URL.",
        },
        "version": {
            "description": "version."
        }
    }
    
    __doc__ = description
    
    
    def get_redirect_url(self, base_url):
        try:
            cmd = [self.env['CURL_PATH'], '-I', '--location']
            cmd.append(base_url)
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (content, stderr) = proc.communicate()
            if proc.returncode:
                raise ProcessorError(
                    'Could not retrieve URL %s: %s' % (url, stderr))
        except OSError:
            raise ProcessorError('Could not retrieve URL: %s' % url)
        return get_location(content)

    
    def main(self):
        base_url = self.env['base_url']
        redirect_url = self.get_redirect_url(base_url)  
        version = get_version(redirect_url)
        self.env['url'] = redirect_url
        self.env['version'] = version
   

if __name__ == '__main__':
    processor = JenkinsURLProvider()
    processor.execute_shell()
