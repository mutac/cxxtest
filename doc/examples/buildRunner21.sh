#!/bin/bash -v

. GetGlobals.sh
export PATH=$CXXTEST/bin:$PATH

# @main:
cxxtestgen --error-printer -o runner.cpp MyTestSuite11.h
# @:main

# @compile:
g++ -o runner -I$CXXTEST -I. runner.cpp
# @:compile

./runner

