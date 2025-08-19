import remote_server


class Session:
    """
    TipTop viewing session.

    Task 2.1 requirements:
    - Store the user who started the session
    - Store the initial TipTop (3D array)
    - Store the per-session viewing limit (max_tiptops_in_session)
    - Provide get_current_tiptop() to return the currently open TipTop

    Notes:
    - We set up minimal nav/blueness state now to make 2.2+ trivial.
    """
    def __init__(self, username, starting_tiptop, max_tiptops_in_session):
        """
        Analyse your time complexity of this method.
        """
        # who is viewing
        self._user = username

        # the TipTop currently open in this session (3D array)
        self._current = starting_tiptop

        # dynamic session limit provided by the app
        self._max_tiptops = max_tiptops_in_session

        # Tracks the record of how many unique TipTops have been opened in a particulary session.
        self._opened_count = 1

        # --- Minimal blueness state (will be used in 2.3) ---
        # We’ll track per-TipTop blueness later; for 2.1 we just initialise counters.
        self._blueness_median_cached = None  # placeholder for O(1) median in 2.3
    
    def get_current_tiptop(self):
        """
        Return the TipTop currently open in this session.

        Time complexity: O(1)
        """
        return self._current

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

