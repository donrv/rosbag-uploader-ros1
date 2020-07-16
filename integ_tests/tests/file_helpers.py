#!/usr/bin/env python
# Copyright (c) 2020, Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import glob
import os
import random
import string
import tempfile

def create_temp_files(total_files):
    temp_file_names = []
    for _ in range(total_files):
        temp_file_names.append(create_temp_file())
    return temp_file_names

def create_temp_file():
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
        file_contents = ''.join(
            [random.choice(string.ascii_letters + string.digits + ' ') for _ in range(64)])
        temp_file.write(file_contents)
    return temp_file.name

def create_large_temp_file(file_size_in_mb):
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
        temp_file.seek(file_size_in_mb * 1024 * 1024 - 1)
        temp_file.write(b'0')
    return temp_file.name

def get_latest_bag_by_regex(directory, regex_pattern):
    bags_list = get_latest_bags_by_regex(directory, regex_pattern, 1)
    if bags_list:
        return bags_list[0]
    else:
        return (None, None)

def get_latest_bags_by_regex(directory, regex_pattern, count=None):
    while True:
        files = glob.iglob(os.path.join(directory, regex_pattern))
        paths = [os.path.join(directory, filename) for filename in files]
        try:
            times = [os.path.getctime(path) for path in paths]
        except OSError:
            continue
        break
    entries = zip(paths, times)
    entries.sort(key=lambda x: x[1], reverse=True)
    if count is None:
        return entries
    else:
        return entries[:count]
