from unittest import TestCase
import ast
import inspect

from tests.helper import CollectionsFinder

from data_structures import ArrayR
from connections import Connections


def to_array(lst):
    """
    Helper function to create an ArrayR from a list.
    """
    lst = [to_array(item) if isinstance(item, list) else item for item in lst]
    return ArrayR.from_list(lst)


def from_array(arr):
    """
    Helper function to convert an ArrayR to a regular list.
    """
    return [from_array(item) if isinstance(item, ArrayR) else item for item in arr]


class TestTask3Setup(TestCase):
    def setUp(self) -> None:
        pass
    


class TestTask3(TestTask3Setup):
    def test_connections_basics(self):
        """
        #name(Connections class basic functionality)
        #hurdle
        """
        usernames = ["alice", "bob", "charlie"]
        connections = [
            ["bob", "charlie"],
            ["alice", "charlie"],
            [],
        ]

        conn = Connections(to_array(usernames), to_array(connections))

        self.assertTrue(conn.mutual_friends("alice", "bob"))
        self.assertTrue(conn.mutual_friends("bob", "alice"))
        self.assertFalse(conn.mutual_friends("alice", "charlie"))
        self.assertFalse(conn.mutual_friends("charlie", "bob"))
    


class TestTask3Approach(TestTask3Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        """
        import connections
        modules = [connections]

        for f in modules:
            # Get the source code
            f_source = inspect.getsource(f)
            filename = f.__file__
            
            tree = ast.parse(f_source)
            visitor = CollectionsFinder(filename)
            visitor.visit(tree)
            
            # Report any failures
            for failure in visitor.failures:
                self.fail(failure[3])
