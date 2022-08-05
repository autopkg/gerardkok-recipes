#!/usr/local/autopkg/python
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

import re
from distutils.version import LooseVersion

from autopkglib import Processor, ProcessorError, URLGetter

__all__ = ["JenkinsURLProvider"]


class JenkinsURLProvider(URLGetter):
    description = "Returns url to the latest Jenkins package."
    input_variables = {
        "base_url": {
            "required": False,
            "default": "http://mirrors.jenkins-ci.org/osx/",
            "description": "URL that lists all available versions of Jenkins for macOS. "
                           "Defaults to: 'http://mirrors.jenkins-ci.org/osx/'.",
        },
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

    def get_latest_version(self, base_url):
        '''Given a base URL, determine the "highest" or "latest" available Jenkins version.'''

        raw_html = self.download(base_url, text=True)
        version_pattern = r'href="jenkins-([\d\.]+)\.pkg"'
        all_versions = re.findall(version_pattern, raw_html)
        if not all_versions:
            raise ProcessorError('Unable to parse available Jenkins versions.')

        return max(all_versions, key=LooseVersion)

    def main(self):
        base_url = self.env['base_url']
        version = self.get_latest_version(base_url)
        self.env['url'] = 'http://mirrors.jenkins-ci.org/osx/jenkins-%s.pkg' % version
        self.env['version'] = version


if __name__ == '__main__':
    PROCESSOR = JenkinsURLProvider()
    PROCESSOR.execute_shell()
