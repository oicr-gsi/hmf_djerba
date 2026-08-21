"""Functions to handle environment variables"""

from djerba.util.environment import directory_finder

class hmf_directory_finder(directory_finder):

    # extend the Djerba directory_finder to get HMF Djerba directory paths

    HMF_DJERBA_ROOT_VAR = 'HMF_DJERBA_ROOT'
    HMF_DJERBA_TEST_DIR_VAR = 'HMF_DJERBA_TEST_DIR'

    def get_hmf_root_dir(self):
        return self.get_directory(self.HMF_DJERBA_ROOT_VAR)
    
    def get_hmf_test_dir(self):
        return self.get_directory(self.HMF_DJERBA_TEST_DIR_VAR)
