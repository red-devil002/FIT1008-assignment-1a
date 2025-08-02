import remote_server


class Session:
    def __init__(self, username, starting_tiptop, max_tiptops_in_session):
        """
        Analyse your time complexity of this method.
        """
        self.username = username
    
    def get_current_tiptop(self):
        pass

    def swipe_up(self, new_tiptop):
        """
        Analyse your time complexity of this method.
        """
        pass
    
    def swipe_right(self):
        """
        Analyse your time complexity of this method.
        """
        pass

    def swipe_left(self):
        """
        Analyse your time complexity of this method.
        """
        pass
    
    def get_blueness(self):
        pass
    
    def pinch_out(self, row, col, intensity):
        """
        Analyse your time complexity of this method.
        """
        pass

    def post_comment(self, comment_length, comment_retriever):
        """
        Analyse your time complexity of this method.
        """
        pass


if __name__ == "__main__":
    # Write tests for your code here...
    # We are not grading your tests, but we will grade your code with our own tests!
    # So writing tests is a good idea to ensure your code works as expected.

    def comment_generator(comment):
        """
        This generates a sequence of characters. You may find it useful for testing your post_comment method.
        Use it like this:
        session.post_comment(8, comment_generator("abcddcba"))
        """
        call_counter = 0
        for char in comment:
            if char == ' ':
                continue
            call_counter += 1
            print(f"Generating character {call_counter}: {char}")
            yield char

