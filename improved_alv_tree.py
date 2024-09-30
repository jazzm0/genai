import threading


class AVLNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self.tree_lock = threading.Lock()

    def insert(self, key):
        with self.tree_lock:
            self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)

        if key < node.val:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        return self._rebalance(node, key)

    def delete(self, key):
        with self.tree_lock:
            self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.val:
            node.left = self._delete(node.left, key)
        elif key > node.val:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._get_min_value_node(node.right)
            node.val = temp.val
            node.right = self._delete(node.right, temp.val)

        return self._get_balance(node)

    def _get_min_value_node(self, node):
        current = node
        while current and current.left is not None:
            current = current.left
        return current

    def search(self, key):
        with self.tree_lock:
            return self._search(self.root, key)

    def _search(self, node, key):
        if not node or node.val == key:
            return node

        if key < node.val:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def print_in_order(self):
        output = []
        self._print_in_order(self.root, output)
        return output

    def _print_in_order(self, node, output):
        if node:
            self._print_in_order(node.left, output)
            output.append(node.val)
            self._print_in_order(node.right, output)

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rebalance(self, node, key):
        balance = self._get_balance(node)

        if balance > 1:
            if key < node.left.val:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

        if balance < -1:
            if key > node.right.val:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y
