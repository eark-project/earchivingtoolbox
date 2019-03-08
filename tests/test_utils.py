#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '../'))  # noqa: E402
import shutil
import unittest
from earchivingtoolbox import root_dir

from earchivingtoolbox.utils.fileutils import rec_find_files
from earchivingtoolbox.utils.randomutils import randomword


class TestUtils(unittest.TestCase):
    temp_extract_dir = '/tmp/backend-utils-' + randomword(10)

    @classmethod
    def setUpClass(cls):
        tests_dir = os.path.join(root_dir, 'tests/test_resources/package')
        shutil.copytree(tests_dir, TestUtils.temp_extract_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TestUtils.temp_extract_dir)
        #pass

    def test_recursive_find_files_in_dir(self):

        def check_paths(retrieved_file_list, expected_paths):
            for retrieved_path in retrieved_file_list:
                self.assertTrue(retrieved_path in expected_paths,
                                "Retrieved path %s not in expected list" % retrieved_path)
            for expected_path in expected_paths:
                self.assertTrue(expected_path in retrieved_file_list,
                                "Expected path %s not in retrieved list" % expected_path)

        def check_excluded(retrieved_file_list, excluded_paths):
            for excluded_path in excluded_paths:
                self.assertTrue(excluded_path not in retrieved_file_list,
                                "Excluded path %s appears in retrieved files list" % excluded_path)

        flist = list(rec_find_files(TestUtils.temp_extract_dir, include_files_rgxs=None, exclude_dirsfiles_rgxs=None))

        self.assertEqual(len(flist), 6, "Number of files not as expected")
        check_paths(flist, expected_paths = (
            os.path.join(TestUtils.temp_extract_dir, 'first_level.txt'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/second_level.txt'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/screen.png'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/second_level.csv'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/subsubfolder/third_level.txt'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/subsubfolder/subsubsubfolder/fourth_level.txt'),
        ))
        with self.assertRaises(AssertionError):
            list(rec_find_files(TestUtils.temp_extract_dir, include_files_rgxs="*.txt", exclude_dirsfiles_rgxs=None))

        flist = list(rec_find_files(TestUtils.temp_extract_dir, include_files_rgxs=[r'.*\.txt$'], exclude_dirsfiles_rgxs=None))
        check_paths(flist, expected_paths = (
            os.path.join(TestUtils.temp_extract_dir, 'first_level.txt'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/second_level.txt'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/subsubfolder/third_level.txt'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/subsubfolder/subsubsubfolder/fourth_level.txt'),
        ))
        check_excluded(flist, excluded_paths=(
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/screen.png'),
        ))
        flist = list(rec_find_files(TestUtils.temp_extract_dir, include_files_rgxs=[r'.*\.txt$', r'.*\.csv$'], exclude_dirsfiles_rgxs=None))
        check_paths(flist, expected_paths = (
            os.path.join(TestUtils.temp_extract_dir, 'first_level.txt'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/second_level.txt'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/second_level.csv'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/subsubfolder/third_level.txt'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/subsubfolder/subsubsubfolder/fourth_level.txt'),
        ))
        check_excluded(flist, excluded_paths=(
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/screen.png'),
        ))
        flist = list(rec_find_files(TestUtils.temp_extract_dir, include_files_rgxs=[r'.*\.txt$', r'.*\.csv$'],
                                     exclude_dirsfiles_rgxs=[r'.*/subfolder.*']))
        check_paths(flist, expected_paths=(
            os.path.join(TestUtils.temp_extract_dir, 'first_level.txt'),
        ))

        flist = list(rec_find_files(TestUtils.temp_extract_dir, include_files_rgxs=[r'.*\.txt$'],
                                    exclude_dirsfiles_rgxs=[r'.*first_level.txt$']))
        check_paths(flist, expected_paths=(
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/second_level.txt'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/subsubfolder/third_level.txt'),
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/subsubfolder/subsubsubfolder/fourth_level.txt'),
        ))

        flist = list(rec_find_files(TestUtils.temp_extract_dir, include_files_rgxs=[r'.*\.txt$'],
                                    exclude_dirsfiles_rgxs=[r'.*first_level.txt$', r'.*/subsubfolder.*']))
        check_paths(flist, expected_paths=(
            os.path.join(TestUtils.temp_extract_dir, 'subfolder/second_level.txt'),
        ))


if __name__ == '__main__':
    unittest.main()