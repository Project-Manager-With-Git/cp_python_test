import unittest
from pathlib import Path
from typing import Dict, Any

from cp_python_test_cli import CpPythonTestClient, MultiCall
from subprocess import Popen, PIPE


class QueryTest(unittest.TestCase):
    backprocess: Popen

    @classmethod
    def setUpClass(cls) -> None:
        cls.backprocess = Popen(["python", "app"], shell=True, stdout=PIPE, cwd=Path(__file__).parent.parent)
        print("后台启动rpc服务")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.backprocess.kill()
        print("关闭rpc服务")

    def setUp(self):
        url = "http://localhost:5000"
        self.cli = CpPythonTestClient(url)
        print("section start")

    def tearDown(self):
        print("section end")

    def test_multi(self) -> None:
        with self.cli:
            multi = MultiCall(self.cli)
            multi.add(1, 2)
            multi.hello("qwe")
            result = multi()
            for i in result:
                print(i)
        self.assertSequenceEqual([3, "hello qwe"], result)

    def test_query(self) -> None:
        with self.cli:
            assert self.cli.add(1, 2) == 3
            assert self.cli.hello("qwe") == "hello qwe"
            
