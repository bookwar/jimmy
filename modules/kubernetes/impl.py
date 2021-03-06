# -*- coding: utf-8 -*-

#  Copyright 2017 Mirantis, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import subprocess
from lib.api import BaseGroovyModule
from string import Template


class Kubernetes(BaseGroovyModule):
    source_tree_path = 'jenkins.kubernetes'

    def update_dest(self, source, jenkins_url, jenkins_cli_path, **kwargs):
        data = self._tree_read(source, self.source_tree_path)
        for cloud in data['clouds']:
            with open(self.groovy_path) as groovy_template:
                groovy_script = Template(groovy_template.read()).substitute(
                    {'cloud_config': cloud}
                )
            try:
                cli_call = subprocess.Popen(["java",
                                             "-jar", jenkins_cli_path,
                                             "-s", jenkins_url,
                                             "groovy",
                                             '='
                                             ], stdin=subprocess.PIPE,
                                            shell=False)
                cli_call.communicate(input=groovy_script)
            except OSError:
                self.logger.exception('Could not find java')
