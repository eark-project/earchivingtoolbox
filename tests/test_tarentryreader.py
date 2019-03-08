#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))  # noqa: E402
import tarfile
import unittest

from earchivingtoolbox import root_dir
from earchivingtoolbox.packaging.tar_entry_reader import ChunkedTarEntryReader


class ChunkedTarEntryReaderTest(unittest.TestCase):

    tar_test_file = None
    entry = None
    tfile = None

    @classmethod
    def setUpClass(cls):
        ChunkedTarEntryReaderTest.tar_test_file = os.path.join(root_dir, "tests/test_resources/storage-test/bar.tar")
        ChunkedTarEntryReaderTest.entry = "739f9c5f-c402-42af-a18b-3d0bdc4e8751/METS.xml"
        ChunkedTarEntryReaderTest.tfile = tarfile.open(ChunkedTarEntryReaderTest.tar_test_file, 'r')

    def test_default_chunk_size(self):
        cter1 = ChunkedTarEntryReader(ChunkedTarEntryReaderTest.tfile)
        self.assertEqual(12, sum([1 for _ in cter1.chunks(ChunkedTarEntryReaderTest.entry)]))
        ChunkedTarEntryReader(ChunkedTarEntryReaderTest.tfile)

    def test_custom_chunk_size(self):
        cter2 = ChunkedTarEntryReader(ChunkedTarEntryReaderTest.tfile, 8192)
        self.assertEqual(1, sum([1 for _ in cter2.chunks(ChunkedTarEntryReaderTest.entry)]))
        ChunkedTarEntryReader(ChunkedTarEntryReaderTest.tfile)


if __name__ == '__main__':
    unittest.main()