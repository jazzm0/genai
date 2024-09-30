class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not isinstance(key, int):
            raise ValueError("Invalid input. Key must be an integer.")

        if self.root is None:
            self.root = TreeNode(key)
        else:
            current = self.root
            while True:
                if key < current.val:
                    if current.left is None:
                        current.left = TreeNode(key)
                        break
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = TreeNode(key)
                        break
                    else:
                        current = current.right

    def inorder(self):
        if self.root is None:
            return

        stack = []
        current = self.root
        done = False

        while not done:
            if current is not None:
                stack.append(current)
                current = current.left
            else:
                if stack:
                    current = stack.pop()
                    print(current.val, end=' ')
                    current = current.right
                else:
                    done = True


# Example usage
bt = BinaryTree()
bt.insert(8)
bt.insert(8)
bt.insert(3)
bt.insert(3)
bt.insert(10)
bt.insert(1)
bt.insert(6)
bt.insert(4)
bt.insert(7)

print("Inorder traversal of the binary tree:")
bt.inorder()
