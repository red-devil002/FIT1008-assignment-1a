import remote_server
from data_structures import ArrayR


class User:
    def __init__(self, username, password):
        """
        Analyse your time complexity of this method.
        """
        self.username = username
        self.password = password

        self.old_password = ArrayR(1) # Taking this because of the size given in the problem is max <= 50 (Resizable Array) starts from 1
        self.old_password[0] = password
        self.count = 1 # Custom counter to keep track of the number of times the user has changed their password

    def change_password(self, new_password):
        """
        Analyse your time complexity of this method.
        """
        # Check if the new password is different from the old password
        for i in range(self.count):
            if self.old_password[i] == new_password:
                raise ValueError("Password already used. Please choose a different password.")
            
        # If the new password is different, add it to the old_password arrayR
        if self.count == len(self.old_password):
            # Resize the array if needed
            new_array = ArrayR(len(self.old_password) * 2)
            for i in range(len(self.old_password)):
                new_array[i] = self.old_password[i]
            self.old_password = new_array
        self.old_password[self.count] = new_password
        self.count += 1

        # Update the current password
        self.password = new_password
        remote_server.user_password_changed(self.username, new_password)
    
    def post_tiptop(self, tiptop):
        """
        Analyse your time complexity of this method.
        """

        # Creating 3D array to store the tiptop
        R = len(tiptop)  # Number of rows
        C = len(tiptop[0])     # Number of columns

        """
        Creating the new 3D array to store the tiptop.
        The new 3D array will have the same dimensions as the original tiptop.
        """
        flipped_tiptop = ArrayR(R)
        for _ in range(R):
            row_array = ArrayR(C)
            flipped_tiptop[_] = row_array
            for _ in range(C):
                pixel = ArrayR(3)
                row_array[_] = pixel

        # fill flipped with rotated + blue-capped pixels
        for r in range(R):
            for c in range(C):
                dest_r = R - 1 - r
                dest_c = C - 1 - c

                src_pixel = tiptop[r][c]      # [R,G,B]
                Rv = src_pixel[0]
                Gv = src_pixel[1]
                Bv = src_pixel[2]
                if Bv > 200:
                    Bv = 200

                flipped_tiptop[dest_r][dest_c][0] = Rv
                flipped_tiptop[dest_r][dest_c][1] = Gv
                flipped_tiptop[dest_r][dest_c][2] = Bv

        # send to server
        remote_server.post_tiptop(self.username, flipped_tiptop)
    
    def get_preview(self):
        """
        Analyse your time complexity of this method.
        """
        pass
    
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

