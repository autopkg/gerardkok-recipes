#!/usr/bin/python
#
# Copyright 2021 Gerard kok
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
import urllib.parse

from autopkglib import Processor, ProcessorError, URLGetter

BASE_URL = "https://dotnet.microsoft.com/download/dotnet/"

__all__ = ["DotNetURLProvider"]


class DotNetURLProvider(URLGetter):
    """Returns url where latest download url of .NET can be found."""
    description = __doc__
    input_variables = {
        "release": {
            "required": False,
            "description": "Major version. Valid values are:"
                            "- a version X.Y (e.g. '5.0'), or"
                            "- a status: 'Preview', 'Current' or 'LTS'",
            "default": "Current",
        },
    }
    output_variables = {
        "release_url": {
            "description": "Url where download url of this release can be found.",
        },
    }


    def get_status_release(self, status):
        raw_html = self.download("https://dotnet.microsoft.com/download/dotnet", text=True)

        release_re = rf'<a href="/download/dotnet/(\d\.\d).*?<span class="badge badge-([a-z]+)">'
        for (release, badge) in re.findall(release_re, raw_html, re.DOTALL):
            if badge == status:
                return release
        
        raise ProcessorError('Unable to find .DotNet status.')


    def get_release_url(self, release):
        m = re.match(r'^\d.\d$', release)
        if m:
            return urllib.parse.urljoin(BASE_URL, release)

        status = release.lower()
        status_release = self.get_status_release(status)
        return urllib.parse.urljoin(BASE_URL, status_release)
    
    
    def main(self):
        release = self.env["release"]
        release_re = r'^(\d\.\d|preview|current|lts)$'
        m = re.match(release_re, release, re.IGNORECASE)
        if m:
            self.env["release_url"] = self.get_release_url(release)
        else:
            raise ProcessorError('Unable to parse .DotNet release.')


if __name__ == '__main__':
    processor = DotNetURLProvider()
    processor.execute_shell()
