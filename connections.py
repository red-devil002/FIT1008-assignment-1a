from data_structures import ArrayStack
from data_structures.linked_list import LinkedList
from data_structures.referential_array import ArrayR

class Connections:
    """
    Handles user connections and friendships in the TipTop platform.
    """
    
    def __init__(self, usernames, connections):
        """
        Initialize the Connections system.
        
        Args:
            usernames: Array containing usernames of all users
            connections: 2D array where connections[i] contains friends of usernames[i]
        """
        # Store the number of users
        self.num_users = len(usernames)
        
        # Store usernames and connections arrays directly
        self.usernames = usernames
        self.connections = connections
    
    def _get_user_index(self, username: str) -> int:
        """
        Helper method to find the index of a username.
        Linear search through usernames array.
        
        Args:
            username: Username to find
            
        Returns:
            Index of the username in the usernames array
        """
        for i in range(len(self.usernames)):
            if self.usernames[i] == username:
                return i
        return -1  # Should not happen based on assumptions
    
    def mutual_friends(self, username1: str, username2: str) -> bool:
        """
        Check if two users are mutual friends.
        
        Args:
            username1: First user's username
            username2: Second user's username
            
        Returns:
            True if they are mutual friends, False otherwise
        """
        # Get indices of both users
        index1 = self._get_user_index(username1)
        index2 = self._get_user_index(username2)
        
        # Check if username1 is in username2's friends list
        user1_follows_user2 = False
        for friend in self.connections[index1]:
            if friend == username2:
                user1_follows_user2 = True
                break
        
        # Check if username2 is in username1's friends list  
        user2_follows_user1 = False
        for friend in self.connections[index2]:
            if friend == username1:
                user2_follows_user1 = True
                break
                
        # They are mutual friends only if both follow each other
        return user1_follows_user2 and user2_follows_user1
    
    def get_ai_clusters_1008_2085(self):
        """
        Find AI clusters for FIT1008/2085.
        
        An AI cluster is formed when a user (bot) is mutual friends with ALL of their connections.
        The cluster includes the bot and all their friends.
        
        Returns:
            Collection of collections, where each inner collection contains users in one cluster
            with the bot (cluster center) as the first element.
        """
        # Track which users have already been included in clusters using ArrayR
        included_in_cluster = ArrayR(self.num_users)
        for i in range(self.num_users):
            included_in_cluster[i] = False
            
        # Store the clusters
        clusters = LinkedList()
        
        # Check each user to see if they're a bot (center of a cluster)
        for i in range(self.num_users):
            username = self.usernames[i]
            
            # Skip if this user is already in a cluster
            if included_in_cluster[i]:
                continue
                
            # Check if this user is a bot
            if self._is_bot(username):
                # Create a new cluster with this bot as center
                cluster = LinkedList()
                cluster.prepend(username)  # Bot is first in cluster
                included_in_cluster[i] = True
                
                # Add all friends of the bot to the cluster (if not already in other clusters)
                for friend_username in self.connections[i]:
                    friend_index = self._get_user_index(friend_username)
                    if not included_in_cluster[friend_index]:
                        cluster.append(friend_username)
                        included_in_cluster[friend_index] = True
                
                # Add this cluster to our collection of clusters
                clusters.append(cluster)
        
        return clusters
    
    def _is_bot(self, username: str) -> bool:
        """
        Helper method to determine if a user is a bot.
        
        A user is a bot if they are mutual friends with ALL of their connections
        AND has no one-sided incoming connections.
        
        Args:
            username: Username to check
            
        Returns:
            True if user is a bot, False otherwise
        """
        user_index = self._get_user_index(username)
        user_friends = self.connections[user_index]
        
        # Check if user is mutual friends with ALL their connections
        for friend_username in user_friends:
            if not self.mutual_friends(username, friend_username):
                return False
        
        # Also check if anyone follows this user that they don't follow back
        for i in range(self.num_users):
            other_username = self.usernames[i]
            if other_username != username:
                # Check if other_username follows this user
                for friend in self.connections[i]:
                    if friend == username:
                        # other_username follows this user
                        # Check if this user follows back
                        follows_back = False
                        for user_friend in user_friends:
                            if user_friend == other_username:
                                follows_back = True
                                break
                        if not follows_back:
                            return False
        
        return True
    
    def get_ai_clusters_1054(self):
        """
        Find AI clusters for FIT1054.
        
        An AI cluster is a group where all users are mutual friends with each other
        and have no connections outside the group.
        
        Returns:
            Collection of collections, where each inner collection contains users in one cluster.
        """
        # Track which users have been visited using ArrayR
        visited = ArrayR(self.num_users)
        for i in range(self.num_users):
            visited[i] = False
            
        clusters = LinkedList()
        
        # Use BFS-like approach to find connected components
        for i in range(self.num_users):
            if not visited[i]:
                cluster = self._find_cluster_1054(i, visited)
                if cluster is not None:
                    clusters.append(cluster)
                    
        return clusters
    
    def _find_cluster_1054(self, start_index: int, visited):
        """
        Helper method to find a cluster starting from a given user index for FIT1054.
        
        Uses BFS to find all mutually connected users with no external connections.
        """
        # Use a queue for BFS
        stack = ArrayStack(self.num_users)
        cluster = LinkedList()
        
        stack.append_right(start_index)
        visited[start_index] = True
        cluster.append(self.usernames[start_index])
        
        while not stack.is_empty():
            current_index = stack.serve_left()
            current_user = self.usernames[current_index]
            
            # Check all friends of current user
            for friend_username in self.connections[current_index]:
                friend_index = self._get_user_index(friend_username)
                if not visited[friend_index]:
                    # Check if this friend should be in the same cluster
                    if self._should_be_in_same_cluster_1054(current_user, friend_username):
                        visited[friend_index] = True
                        stack.append_right(friend_index)
                        cluster.append(friend_username)
        
        # Verify the cluster is valid (all pairs are mutual friends and no external connections)
        if self._is_valid_cluster_1054(cluster):
            return cluster
        else:
            return None
    
    def _should_be_in_same_cluster_1054(self, user1: str, user2: str) -> bool:
        """
        Check if two users should be in the same cluster for FIT1054.
        """
        return self.mutual_friends(user1, user2)
    
    def _is_valid_cluster_1054(self, cluster) -> bool:
        """
        Verify that a cluster is valid for FIT1054:
        - All pairs in the cluster are mutual friends
        - No one in the cluster has connections outside the cluster
        """
        # Check all pairs are mutual friends and no external connections
        current = cluster.head
        while current is not None:
            username = current.item
            user_index = self._get_user_index(username)
            
            # Check all connections of this user
            for friend_username in self.connections[user_index]:
                # Check if friend is in the cluster
                friend_in_cluster = False
                cluster_current = cluster.head
                while cluster_current is not None:
                    if cluster_current.item == friend_username:
                        friend_in_cluster = True
                        break
                    cluster_current = cluster_current.link
                
                # Friend should be in the cluster
                if not friend_in_cluster:
                    return False
                    
                # Should be mutual friends
                if not self.mutual_friends(username, friend_username):
                    return False
            
            current = current.link
        
        return True