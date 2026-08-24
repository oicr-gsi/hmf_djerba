#! /usr/bin/env bash

# 'source' this file to run tests

# if HMF_DJERBA_SOURCE_DIR not set
if [ -z "${HMF_DJERBA_SOURCE_DIR}" ]; then
    # set source dir based on script location; see https://stackoverflow.com/a/246128
    HMF_DJERBA_SOURCE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )/../.." &> /dev/null && pwd )
fi

# do sanity checking, then export the test variables
if [ ! -d "${HMF_DJERBA_SOURCE_DIR}" ]; then
    echo "HMF_DJERBA_SOURCE_DIR '$HMF_DJERBA_SOURCE_DIR' does not exist"
elif [ ! -d "${HMF_DJERBA_TEST_DIR}" ]; then
    echo "HMF_DJERBA_TEST_DIR '$HMF_DJERBA_TEST_DIR' does not exist"
elif [ -z "${HMF_DJERBA_ROOT}" ]; then
    echo "Must load the hmf-djerba environment module; first update MODULEPATH if necessary"
else
    # export variables for running tests on the source code
    export PYTHONPATH=${HMF_DJERBA_SOURCE_DIR}/src/lib:$PYTHONPATH
fi
