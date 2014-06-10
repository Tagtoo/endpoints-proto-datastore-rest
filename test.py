#!/usr/bin/python
import optparse
import sys
# Install the Python unittest2 package before you run this script.
import unittest2
import nose

USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation
TEST_PATH   Path to package containing test modules"""
GAE_SDK = "./google_appengine"

sys.path.insert(0, GAE_SDK)
import dev_appserver
dev_appserver.fix_sys_path()

sys.exit(int(not nose.run()))
