/*
 * Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
#include <fstream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <sys/stat.h>

#include <cstring>
#include <cerrno>
#include <string>
#include <unistd.h>

#include <gtest/gtest.h>

#include <rosbag_cloud_recorders/utils/file_utils.h>

using namespace Aws::Rosbag::Utils;

TEST(DeleteFileTest, TestFileRemovalSucceeds)
{
    std::string path = "./TestRosbagRemovalSuccessfulCase.bag";
    std::ofstream file(path);
    file.close();
    EXPECT_EQ(DeleteFile(path), Aws::Rosbag::RecorderErrorCode::SUCCESS);
}

TEST(DeleteFileTest, TestFileRemovalFailsFileDoesntExist)
{
  EXPECT_EQ(DeleteFile("/I/Am/Nowhere/To/Be/Found.bag"), Aws::Rosbag::RecorderErrorCode::FILE_NOT_FOUND);
}

TEST(DeleteFileTest, TestRemoveDirectoryFails)
{
    char dir_template[] = "/tmp/DeleteFileTestXXXXXX";
    mkdtemp(dir_template);
    EXPECT_EQ(Aws::Rosbag::RecorderErrorCode::FILE_REMOVAL_FAILED, DeleteFile(dir_template));
    rmdir(dir_template);
}