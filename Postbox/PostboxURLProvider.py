#!/usr/bin/env python
#
# Copyright 2013 Gerard Kok
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

import re
import urllib
import urllib2

from autopkglib import Processor, ProcessorError


__all__ = ["PostboxURLProvider"]

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.28.10 (KHTML, like Gecko) Version/6.0.3 Safari/536.28.10'
MAIN_DOWNLOAD_URL = "http://www.postbox-inc.com/download_success/mac"

re_dmg_url = re.compile(r'download_url = \"(?P<dmg_url>/php/download.php\?a=[0-9]+m)\"')

class PostboxURLProvider(Processor):
    """Provides a download URL for the latest Postbox"""
    input_variables = {
        "base_url": {
            "required": False,
            "description": "The Postbox download site",
        },
    }
    output_variables = {
        "url": {
            "description": "URL to the latest Postbox release.",
        },
    }
    description = __doc__
    
    def parse_dmg_url(self, base_url):
        """Returns the URL"""
        try:
            headers = { 'User-Agent' : USER_AGENT }
            req = urllib2.Request(base_url, None, headers)
            html = urllib2.urlopen(req).read()
        except BaseException as e:
            raise ProcessorError("Can't download %s: %s" % (base_url, e))

        m = re_dmg_url.search(html)

        if not m:
            raise ProcessorError(
                "Couldn't find link in %s" % base_url)
        
        relative_url = m.group("dmg_url")
        dmg_url = "http://postbox-inc.com" + relative_url
        self.output("Dmg link is %s" % dmg_url)
        return dmg_url
    
    
    def get_Postbox_dmg_url(self, base_url):
        """Find and return a download URL"""
        
        dmg_url = self.parse_dmg_url(base_url)
        
        return dmg_url
    
    
    def main(self):
        base_url = self.env.get("base_url", MAIN_DOWNLOAD_URL)
        self.env["url"] = self.get_Postbox_dmg_url(base_url)
        self.output("Found URL %s" % self.env["url"])


if __name__ == "__main__":
    processor = PostboxURLProvider()
    processor.execute_shell()
