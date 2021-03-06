# Copyright 2018 Geoff Lee
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
"""Processor to build a python distutils project"""
import os
from zipfile import ZipFile
from subprocess import check_call
# Pylint can't load autopkglib, so stop it moaning
#pylint: disable=locally-disabled,import-error
from autopkglib import Processor, ProcessorError


__all__ = ["PythonBDistBuilder"]

#pylint: disable=locally-disabled,too-few-public-methods
class PythonBDistBuilder(Processor):
    """Build a python disttools project, ready for packaging"""
    description = __doc__
    input_variables = {
        "source_path": {
            "required": True,
            "description": "Path to the source directory of the package.",
        },
    }
    output_variables = {
    }

#pylint: disable=

    def main(self):
        """Do it"""
        try:
            os.chdir(self.env['source_path'])
            check_call(['/usr/bin/python', 'setup.py',
                        'bdist', '-p', 'macOS', '--formats', 'zip'])
            self.output("Built dist at %s" % self.env['source_path'])
        except BaseException, err:
            raise ProcessorError("Can't build dist at %s: %s"
                                 % (self.env['source_path'], err))

        cwd = os.getcwd()
        pkgroot = cwd + '../pkg_root'
        try:
            zipped = ZipFile('./dist/' + self.env['NAME'] +
                             '-' + self.env['RELEASE'] + '.macOS.zip')
            zipped.extractall(path=pkgroot)
            self.output("Unzipped package root at %s" % self.env['source_path'])
        except BaseException, err:
            raise ProcessorError("Can't extract package root at %s: %s"
                                 % (pkgroot, err))

if __name__ == '__main__':
    PROCESSOR = PythonBDistBuilder()
    PROCESSOR.execute_shell()
