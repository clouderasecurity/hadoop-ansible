#!/bin/bash -x

# Copyright 2014, Gazzang Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Quickly install all prereqs. Custom flags added for OS X Mavericks users.
source ./venv/bin/activate
test `uname` = "Darwin" && ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install $(grep pycrypto requirements.txt)
pip install -r requirements.txt
