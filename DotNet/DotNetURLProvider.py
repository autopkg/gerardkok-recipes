#!/usr/local/autopkg/python
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

from autopkglib import Processor, ProcessorError, URLGetter

BASE_URL = "https://dotnet.microsoft.com"

__all__ = ["DotNetURLProvider"]


class DotNetURLProvider(URLGetter):
    """Returns url where latest download url of .NET can be found."""
    description = __doc__
    input_variables = {
        "release": {
            "required": False,
            "description": "Major version. Valid values are:"
                            "- a version X.Y (e.g. '5.0'), or"
                            "- a status: 'Preview', 'LTS' or 'Maintenance'",
            "default": "LTS",
        },
        "language_code": {
            "required": False,
            "description": "Language code to use in urls",
            "default": "en-us"
        },
    }
    output_variables = {
        "release_url": {
            "description": "Url where download url of this release can be found.",
        },
    }


    def status_release(self, status, url_path):
        base_url = f"{BASE_URL}/{url_path}"
        raw_html = self.download(base_url, text=True)

        release_re = rf'<a href="/{url_path}/(\d\.\d).*?<span class="badge badge-([a-z]+)">'
        for (release, badge) in re.findall(release_re, raw_html, re.DOTALL):
            if badge == status:
                return release
        
        raise ProcessorError('Unable to find .DotNet status.')


    def release(self, release, url_path):
        release_re = r'^(\d\.\d|preview|lts|maintenance)$'
        m = re.match(release_re, release, re.IGNORECASE)
        if not m:
            raise ProcessorError('Unable to parse .DotNet release.')

        n = re.match(r'^\d.\d$', m.group())
        if n:
            return m.group()
       
        status = release.lower()
        return self.status_release(status, url_path)



    def release_url(self, release, url_path):
        return f"{BASE_URL}/{url_path}/{self.release(release, url_path)}"
   
    
    def main(self):
        language_code = self.env["language_code"]
        url_path = f"{language_code}/download/dotnet"
        release = self.env["release"]
        self.env["release_url"] = self.release_url(release, url_path)


if __name__ == '__main__':
    processor = DotNetURLProvider()
    processor.execute_shell()
