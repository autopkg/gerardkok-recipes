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

from autopkglib import Processor


__all__ = ["SuffixSelector"]


class SuffixSelector(Processor):
    description = "Selects the suffix that matches OS_VERSION."
    input_variables = {
        "OS_VERSION": {
            "required": False,
            "default": '10.13',
            "description": (
                "Outputs the GPGMail_core pkg name for this OS_VERSION. Possible values:"
                "'10.9', '10.10', '10'.11', 10.12', '10.13'."
                "Defaults to '10.13'"),
        },
    }
    output_variables = {
        "suffix": {
            "description": "Suffix used in the GPGMail_Core package.",
        }
    }

    __doc__ = description


    def main(self):
        release = self.env.get('OS_VERSION', '10.13')
        switcher = {
            '10.12': "_12",
            '10.13': "_13",
            '10.14': '_14'
        }
        self.env['suffix'] = switcher.get(release, "")

if __name__ == '__main__':
    processor = SuffixSelector()
    processor.execute_shell()
