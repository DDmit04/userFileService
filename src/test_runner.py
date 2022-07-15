import unittest

from test.boto_file_repo_test import BotoFileRepositoryTest
from test.file_record_service_test import FileRecordServiceTest
from test.file_service_facade_test import FileServiceFacadeTest
from test.file_service_test import FileServiceTest
from test.file_sync_service_test import FileSyncServiceTest


def run_tests():
    calcTestSuite = unittest.TestSuite()
    calcTestSuite.addTest(unittest.makeSuite(BotoFileRepositoryTest))
    calcTestSuite.addTest(unittest.makeSuite(FileRecordServiceTest))
    calcTestSuite.addTest(unittest.makeSuite(FileServiceFacadeTest))
    calcTestSuite.addTest(unittest.makeSuite(FileServiceTest))
    calcTestSuite.addTest(unittest.makeSuite(FileSyncServiceTest))
    runner = unittest.TextTestRunner()
    runner.run(calcTestSuite)
