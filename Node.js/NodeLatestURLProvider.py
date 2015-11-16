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


__all__ = ["NodeLatestURLProvider"]


class NodeLatestURLProvider(Processor):
    description = "Returns url to the latest Node.js package."
    input_variables = {
        "type": {
            "required": False,
            "description": "type of download; either 'LTS' or 'Stable', default: 'Stable'.",
        }
    }
    output_variables = {
        "url": {
            "description": "download URL.",
        }
    }
    
    __doc__ = description
    
    
    def main(self):
        if self.env["type"] == 'LTS':
            url = 'https://nodejs.org/dist/latest-v4.x'
        else:
            url = 'https://nodejs.org/dist/latest'
        self.env["url"] = url      
   

if __name__ == '__main__':
    processor = NodeLatestURLProvider()
    processor.execute_shell()
    
