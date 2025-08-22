import remote_server
from data_structures import ArrayR


class User:
    def __init__(self, username, password):
        """
        Analyse your time complexity of this method.
        """
        # Code From Task 1.1
        self.username = username
        self.password = password # Password is stored as a string using password attribute.

        self.swtp_old_password = ArrayR(1) # Taking this because of the size given in the problem is max <= 50 starts from 1
        self.swtp_old_password[0] = password
        self.swtp_pass_count = 1 # Custom counter to keep track of the number of times the user has changed their password

        # Code From Task 1.3
        self._swtp_preview_cap = 3
        self.swtp_bufferImage = ArrayR(self._swtp_preview_cap)  # capacity == current cap
        self.swtp_head = 0     # index of oldest
        self._swtp_size = 0    # number of items currently stored

    def change_password(self, new_password):
        """
        Variable i = number of stored passwords.
        :complexity: Best case is O(1) where i is the number of previously used passwords.
        The best case happens when the new password is equal to the very first element in the used passwords array, so we detect the copy immediately and raise an ValueError without scanning further.

        Worst case is O(i) where i is the number of previously used passwords.
        The worst case happens when the new password is not found in any of the previous passwords, so the loop scans through all i entries before inserting the new one.
        However, since i is capped at 51 (50 changes + the initial password), as per our assumptions, the practical worst case is still O(1) in terms of time complexity.
        """
        # Checking Condition - Check if the new password is same as the current password
        for i in range(self.swtp_pass_count):
            if self.swtp_old_password[i] == new_password:
                raise ValueError("Password already used. Please choose a different password.")

        # Update the current password
        self.password = new_password
        remote_server.user_password_changed(self.username, new_password)
    
    def post_tiptop(self, tiptop):
        """
        :complexity: Best and worst case are both O(P), where P = rows * cols is the number of pixels.
        For each output pixel (r, c), we compute its source position (R-1-r, C-1-c) and copy three channel values, capping only the blue channel with a min() operation. This is a constant amount of work per pixel, so total time is linear in the number of pixels.
        """

        # Original - Creating 3D array to store the tiptop
        _inputval_R = len(tiptop)  # Number of rows
        _inputval_C = len(tiptop[0])     # Number of columns

        # Creating the new 3D array to store the tiptop.
        # The new 3D array will have the same dimensions as the original tiptop.
        swtp_flipped_tiptop = ArrayR(_inputval_R)
        for row in range(_inputval_R):
            swtp_row_array = ArrayR(_inputval_C)
            swtp_flipped_tiptop[row] = swtp_row_array
            for col in range(_inputval_C):
                swtp_inverted_pixel = ArrayR(3)
                swtp_row_array[col] = swtp_inverted_pixel

        # fill flipped with rotated + blue-capped pixels
        for row in range(_inputval_R):
            for col in range(_inputval_C):
                swtp_fli_row_tiptop = _inputval_R - 1 - row  # flip vertically
                swtp_fli_col_tiptop = _inputval_C - 1 - col # flip horizontally

                swtp_posted_image_px = tiptop[row][col]      # [R,G,B]
                swtp_red = swtp_posted_image_px[0]
                swtp_green = swtp_posted_image_px[1]
                swtp_blue = swtp_posted_image_px[2]
                if swtp_blue > 200:
                    swtp_blue = 200

                swtp_flipped_tiptop[swtp_fli_row_tiptop][swtp_fli_col_tiptop][0] = swtp_red
                swtp_flipped_tiptop[swtp_fli_row_tiptop][swtp_fli_col_tiptop][1] = swtp_green
                swtp_flipped_tiptop[swtp_fli_row_tiptop][swtp_fli_col_tiptop][2] = swtp_blue

        # send to server
        remote_server.post_tiptop(self.username, swtp_flipped_tiptop)

    
    # Instade of new function this pasrt of cde helps in task 1.3.
        if self._swtp_size == self._swtp_preview_cap:
            self.swtp_bufferImage[self.swtp_head] = swtp_flipped_tiptop
            self.swtp_head = (self.swtp_head + 1) % self._swtp_preview_cap
        else:
            img_tail = (self.swtp_head + self._swtp_size) % self._swtp_preview_cap
            self.swtp_bufferImage[img_tail] = swtp_flipped_tiptop
            self._swtp_size += 1

    def get_preview(self):
        """
        :complexity: Best case is O(1) when K = 0, where K is the current number of stored previews. We may allocate a new buffer but copy 0 elements and return quickly.

        Typical case without reallocation is O(K), because we construct the return structure by copying K items from newest to oldest.

        Worst case is O(K) as well when capacity growth is required: we first realign the ring buffer by copying K elements into a new ArrayR, then copy the same K elements into the return structure.
        """
        swtp_buff_prv_result = ArrayR(self._swtp_size)

        # if cap increased beyond current buffer capacity, reallocate buffer
        if self._swtp_preview_cap > len(self.swtp_bufferImage):
            new_buf = ArrayR(self._swtp_preview_cap)
            for i in range(self._swtp_size):
                swtp_src = (self.swtp_head + i) % len(self.swtp_bufferImage)
                new_buf[i] = self.swtp_bufferImage[swtp_src]
            self.swtp_bufferImage = new_buf
            self.swtp_head = 0  # oldest now at index 0


        if self._swtp_size > 0:
            swtp_pvt_cap_now = len(self.swtp_bufferImage)  # equal to self._swtp_preview_cap at this time
            # newest index is (head + size - 1) % cap
            for i in range(self._swtp_size):
                swtp_idxx = (self.swtp_head + self._swtp_size - 1 - i) % swtp_pvt_cap_now
                swtp_buff_prv_result[i] = self.swtp_bufferImage[swtp_idxx]

        # grow preview cap for NEXT time
        self._swtp_preview_cap += 1


        return swtp_buff_prv_result

    def generate_feed(self, users_tiptops):
        """
        1054 Only - 1008/2085 welcome to attempt if you're up for a challenge, but no marks are allocated.
        Analyse your time complexity of this method.
        """
        pass
    
    def __str__(self):
        return f"User(username={self.username})"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    # Write tests for your code here...
    # We are not grading your tests, but we will grade your code with our own tests!
    # So writing tests is a good idea to ensure your code works as expected.
    
    def to_array(lst):
        """
        You may find this function useful for testing your code. It converts a Python list to an array.
        It also works with nested lists. You don't need to understand how it works, but you're welcome
        to use it (only in testing), and to copy it to the testing section of other files if you need it.

        Try passing it [[1,2], [3,4]].
        """
        from data_structures import ArrayR
        lst = [to_array(item) if isinstance(item, list) else item for item in lst]
        return ArrayR.from_list(lst)

    # Here are a couple of easy tests to get you started...
    user = User("test_user", "password123")
    assert user.username == "test_user"

    sample_tiptop = to_array([
        [[123, 100, 0], [0, 255, 0]],
        [[255, 255, 0], [0, 255, 255]],
    ])
    
    user.post_tiptop(sample_tiptop)
    preview = user.get_preview()
    assert len(preview) == 1

    # I want to make sure the blue is reduced to 200, so I'm going to print the TipTop in preview
    print("Preview TipTop:", preview[0])

    # That wasn't quite the 2x2 format I wanted, let me make that print statement a bit clearer
    print("Preview TipTop:")
    for row in preview[0]:
        print("  ", row)

    # That's better! Continue testing your code here...

