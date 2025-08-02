from unittest import TestCase, mock
import ast
import inspect

from tests.helper import CollectionsFinder

from data_structures import ArrayR
from user import User


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


class TestTask1Setup(TestCase):

    def setUp(self) -> None:
        self.user = User("test_user", "password123")


class TestTask1(TestTask1Setup):
    def test_user_basics(self):
        """
        #name(User class basic functionality)
        #hurdle
        """
        self.assertEqual(self.user.username, "test_user")
        self.assertEqual(self.user.password, "password123")

        # Mock the remote server
        with mock.patch('remote_server.user_password_changed') as mock_user_password_changed:
            self.user.change_password("new_password123")
            self.assertEqual(self.user.password, "new_password123")

            # Check that the remote server was called
            mock_user_password_changed.assert_called_once_with("test_user", "new_password123")
        
    
    def test_posting_tiptop_calls_remote_server(self):
        """
        #name(Posting tiptop calls remote server)
        #hurdle
        """
        sample_tiptop = [
            [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
            [[255, 255, 0], [0, 255, 255], [255, 0, 255]]
        ]

        # Mock the remote server
        with mock.patch('remote_server.post_tiptop') as mock_post_tiptop:
            self.user.post_tiptop(to_array(sample_tiptop))

            # Check that the remote server was called
            mock_post_tiptop.assert_called_once()


class TestTask1Approach(TestTask1Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        """
        import user
        modules = [user]

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