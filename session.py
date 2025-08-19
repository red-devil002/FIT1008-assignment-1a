import remote_server
from data_structures import ArrayR


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
        self.username = username

        # the TipTop currently open in this session (3D array)
        self._current = starting_tiptop

        # dynamic session limit provided by the app
        self._max_tiptops = max_tiptops_in_session

        # Tracks the record of how many unique TipTops have been opened in a particulary session.
        self._opened_count = 1

        # --- Minimal nav state (ready for Task 2.2) ---
        # Back and forward stacks using ArrayR (no Python lists)
        self._back_stack = ArrayR(1) 
        self._back_size = 0

        self._fwd_stack = ArrayR(1)  
        self._fwd_size = 0

        # ----- 2.3 blueness state -----
        # histogram for blueness values (0..201)
        self._blue_hist = ArrayR(202)
        for i in range(202):
            self._blue_hist[i] = 0
        # number of *distinct* tiptops that have contributed to stats
        self._n_viewed = 0
        # cached median (float or int)
        self._median_value = 0.0

        # add the initial tiptop’s blueness
        b0 = self._compute_blueness(self._current)
        self._blue_hist[b0] += 1
        self._n_viewed = 1
        self._recompute_median()
    
    def get_current_tiptop(self):
        """
        Return the TipTop currently open in this session.

        Time complexity: O(1)
        """
        return self._current

    def swipe_up(self, new_tiptop):
        """
        Open a NEW TipTop.
        - Push current into back stack.
        - Clear forward stack (can't redo after opening something new).
        - Set current to new_tiptop.
        Time: Amortized O(1)
        """
        # push current onto back stack
        if self._back_size == len(self._back_stack):
            # grow back stack
            new_cap = max(1, len(self._back_stack) * 2)
            bigger = ArrayR(new_cap)
            for i in range(self._back_size):
                bigger[i] = self._back_stack[i]
            self._back_stack = bigger
        self._back_stack[self._back_size] = self._current
        self._back_size += 1

        # clear forward stack (do not shrink capacity)
        self._fwd_size = 0

        # set current to the new tiptop
        self._current = new_tiptop

        # opened unique tiptop count (assumption guarantees we won't exceed max)
        self._opened_count += 1

        """
        2.3: update blueness stats for this NEW tiptop
        """
        b = self._compute_blueness(new_tiptop)
        self._blue_hist[b] += 1
        self._n_viewed += 1
        self._recompute_median()
    
    def swipe_right(self):
        """
        Go BACK by one TipTop (like browser Back).
        - If there is no back history, do nothing.
        - Otherwise: push current to forward stack, pop from back stack to current.
        Time: Amortized O(1)
        """
        if self._back_size == 0:
            return  # nothing to go back to

        # push current onto forward stack
        if self._fwd_size == len(self._fwd_stack):
            new_cap = max(1, len(self._fwd_stack) * 2)
            bigger = ArrayR(new_cap)
            for i in range(self._fwd_size):
                bigger[i] = self._fwd_stack[i]
            self._fwd_stack = bigger
        self._fwd_stack[self._fwd_size] = self._current
        self._fwd_size += 1

        # pop from back stack
        self._back_size -= 1
        self._current = self._back_stack[self._back_size]

    def swipe_left(self):
        """
        Go FORWARD by one TipTop (undo a Back).
        - Only works if a previous swipe_right created forward history.
        - If there is no forward history, do nothing.
        Time: Amortized O(1)
        """
        if self._fwd_size == 0:
            return  # nothing to go forward to

        # push current onto back stack
        if self._back_size == len(self._back_stack):
            new_cap = max(1, len(self._back_stack) * 2)
            bigger = ArrayR(new_cap)
            for i in range(self._back_size):
                bigger[i] = self._back_stack[i]
            self._back_stack = bigger
        self._back_stack[self._back_size] = self._current
        self._back_size += 1

        # pop from forward stack
        self._fwd_size -= 1
        self._current = self._fwd_stack[self._fwd_size]
    
    def get_blueness(self):
        """
        Return the session blueness (median of blueness over all viewed TipTops).
        Must be O(1): we return a cached value updated on changes.
        """
        # If there are no viewed tiptops (shouldn’t happen), return 0
        if self._n_viewed == 0:
            return 0
        return self._median_value
    
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


    """
        private utilities for 2.3
    """

    def _recompute_median(self):
        """
        Recompute and cache the median from the histogram.
        Domain is fixed (0..201), so this is O(202) = O(1) constant time.
        """
        imput_n = self._n_viewed
        # odd → the (n+1)//2 -th item; even → average of n//2 and n//2 + 1
        if imput_n <= 0:
            self._median_value = 0.0
            return

        if (imput_n % 2) == 1:
            target = (imput_n + 1) // 2
            cum = 0
            for v in range(202):
                cum += self._blue_hist[v]
                if cum >= target:
                    # exact value
                    self._median_value = float(v)
                    return
        else:
            t1 = imput_n // 2
            t2 = t1 + 1
            cum = 0
            m1 = None
            m2 = None
            for v in range(202):
                cum += self._blue_hist[v]
                if (m1 is None) and (cum >= t1):
                    m1 = v
                if cum >= t2:
                    m2 = v
                    break
            # average; e.g., may produce .5 like 2.5 (matches example)
            self._median_value = (m1 + m2) / 2.0

    def _compute_blueness(self, tiptop):
        """
        Count unique Blue values (index 2) across all pixels.
        Blue values in sessions are capped at 200, so domain = 0..200.

        Time: O(P) where P is pixels in the tiptop.
        """
        # seen[0..200] = 0/1
        seen = ArrayR(201)
        for i in range(201):
            seen[i] = 0

        R = len(tiptop)
        C = len(tiptop[0])

        count_unique = 0
        for row in range(R):
            for col in range(C):
                ans_gurr = tiptop[row][col][2]      # 0..200 guaranteed per spec
                if seen[ans_gurr] == 0:
                    seen[ans_gurr] = 1
                    count_unique += 1
        return count_unique

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

