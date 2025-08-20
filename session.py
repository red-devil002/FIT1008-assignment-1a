import remote_server
from data_structures import ArrayR    
from data_structures import ArrayStack

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
        Increases the brightness of pixels based on distance from the pinch point.
        
        The pixel at (row, col) increases by intensity, and surrounding pixels 
        increase by max(intensity - distance, 0) where distance is Manhattan distance.
        
        RGB values are capped at 255 for R and G, and 200 for B.
        
        Args:
            row: The row index of the pinch point
            col: The column index of the pinch point  
            intensity: The intensity of the pinch (>= 0)
        """
        if intensity == 0:
            return
        
        current_tiptop = self.get_current_tiptop()
        rows = len(current_tiptop)
        cols = len(current_tiptop[0]) if rows > 0 else 0
        
        # Calculate old blueness before making changes
        old_blueness = self._calculate_tiptop_blueness(current_tiptop)
        
        # Calculate the range of pixels that will be affected
        # Only need to check pixels within distance (intensity - 1) from the pinch point
        min_row = max(0, row - (intensity - 1))
        max_row = min(rows - 1, row + (intensity - 1))
        min_col = max(0, col - (intensity - 1))
        max_col = min(cols - 1, col + (intensity - 1))
        
        # Apply brightness increase to affected pixels
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                # Calculate Manhattan distance
                distance = abs(r - row) + abs(c - col)
                
                # Calculate brightness increase for this pixel
                brightness_increase = max(intensity - distance, 0)
                
                if brightness_increase > 0:
                    pixel = current_tiptop[r][c]
                    
                    # Increase RGB values with proper capping
                    pixel[0] = min(255, pixel[0] + brightness_increase)  # Red cap at 255
                    pixel[1] = min(255, pixel[1] + brightness_increase)  # Green cap at 255  
                    pixel[2] = min(200, pixel[2] + brightness_increase)  # Blue cap at 200
        
        # Calculate new blueness and update tracking if needed
        new_blueness = self._calculate_tiptop_blueness(current_tiptop)
        
        if new_blueness != old_blueness:
            # Update the blueness tracking for this TipTop
            # This assumes we have a blueness tracking system from task 2.3
            self._update_current_tiptop_blueness(old_blueness, new_blueness)

    def _calculate_tiptop_blueness(self, tiptop):
        """
        Helper method to calculate the blueness (number of unique blue values) of a TipTop.
        Uses a simple O(P^2) approach since we can't use sets or built-in collections.
        """
        rows = len(tiptop)
        if rows == 0:
            return 0
        
        cols = len(tiptop[0])
        if cols == 0:
            return 0
        
        # Since we can't use sets or lists, we'll use a simple O(P^2) approach
        # to count unique blue values by checking each pixel against all previous pixels
        unique_count = 0
        
        for r in range(rows):
            for c in range(cols):
                blue_value = tiptop[r][c][2]
                is_unique = True
                
                # Check if we've seen this blue value before
                for prev_r in range(rows):
                    for prev_c in range(cols):
                        # Stop checking when we reach the current pixel
                        if prev_r == r and prev_c == c:
                            break
                        if prev_r > r or (prev_r == r and prev_c >= c):
                            break
                            
                        if tiptop[prev_r][prev_c][2] == blue_value:
                            is_unique = False
                            break
                    if not is_unique:
                        break
                
                if is_unique:
                    unique_count += 1
        
        return unique_count

    def _update_current_tiptop_blueness(self, old_blueness, new_blueness):
        """
            Helper method to update the blueness tracking when the current TipTop's blueness changes.
            This needs to be integrated with whatever blueness tracking system is implemented in task 2.3.
        """
        # This is a placeholder - the actual implementation depends on how blueness is tracked
        # from task 2.3. You would need to:
        # 1. Find the current TipTop in your blueness tracking structure
        # 2. Update its blueness value from old_blueness to new_blueness
        # 3. Recalculate the median if needed
        pass

    def post_comment(self, comment_length, comment_retriever):
        """
        Checks if a comment is a palindrome and posts it if valid.
        
        A palindrome reads the same forward and backward (ignoring spaces).
        This method uses an iterator to read characters one by one and stops
        as soon as it can determine if the string is or isn't a palindrome.
        
        We use a two-pointer approach conceptually, but since we can only read forward,
        we read all characters into ArrayR and then check palindrome property.
        
        Args:
            comment_length: Length of the comment (excluding spaces)  
            comment_retriever: Iterator that yields characters one by one
        
        Returns:
            True if comment is a palindrome and was posted, False otherwise
        """
        
        # Read all characters into an ArrayDeque since we need to access both ends
        chars = ArrayStack(comment_length)
        
        # Read all characters from the iterator
        for i in range(comment_length):
            char = next(comment_retriever)
            chars.append_right(char)
        
        # Now check if it's a palindrome by comparing from both ends
        # We only need to check half the characters
        chars_to_check = comment_length // 2
        
        for i in range(chars_to_check):
            # Get character from the left end
            left_char = chars.peek_left()
            chars.serve_left()
            
            # Get character from the right end  
            right_char = chars.peek_right()
            chars.serve_right()
            
            # If characters don't match, it's not a palindrome
            if left_char != right_char:
                return False
        
        # If we get here, it's a palindrome
        # Call the remote server to post the comment
        from remote_server import post_comment
        post_comment(self.user, self.get_current_tiptop())
        return True


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

