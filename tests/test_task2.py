from unittest import TestCase
import ast
import inspect

from tests.helper import CollectionsFinder

from data_structures import ArrayR
from session import Session


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


class TestTask2Setup(TestCase):
    def setUp(self) -> None:
        pass


class TestTask2(TestTask2Setup):
    def test_initialization(self):
        """
        #name(Session class basic functionality)
        #hurdle
        """
        s = Session("test_user", to_array([[[255, 0, 0]]]), 10)
        self.assertEqual(s.username, "test_user")
        self.assertEqual(from_array(s.get_current_tiptop()), [[[255, 0, 0]]])
    
    def test_swipe_up_basic(self):
        """
        #name(Swipe up functionality)
        #hurdle
        """
        s = Session("test_user", to_array([[[255, 0, 0]]]), 10)
        new_tiptop = to_array([[[0, 255, 0]]])
        
        s.swipe_up(new_tiptop)
        self.assertEqual(from_array(s.get_current_tiptop()), [[[0, 255, 0]]])
    


class TestTask2Approach(TestTask2Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        """
        import session
        modules = [session]

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
