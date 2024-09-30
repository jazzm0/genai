import threading


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None


class DoublyLinkedList:
    def __init__(self, max_size=None):
        self.head = None
        self.last = None
        self.size = 0
        self.max_size = max_size  # Maximum size limit for the linked list
        self.lock = threading.Lock()  # Lock for concurrency control

    def append(self, data):
        # Validate input data
        if len(data) > 1000:  # Example: Limit data size to prevent excessively large payloads
            raise ValueError("Data size exceeds maximum limit")

        with self.lock:
            # Rate limiting mechanism can be implemented here
            if self.max_size is not None and self.size >= self.max_size:
                raise ValueError("Linked list is full")

            new_node = Node(data)
            if self.head is None:
                self.head = new_node
                self.last = self.head
            else:
                self.last.next = new_node
                new_node.previous = self.last
                self.last = new_node
            self.size += 1

    def remove(self, data):
        with self.lock:
            current = self.head
            while current:
                if current.data == data:
                    if current.previous:
                        current.previous.next = current.next
                    if current.next:
                        current.next.previous = current.previous
                    if current == self.head:
                        self.head = current.next
                    if current == self.last:
                        self.last = current.previous
                    if self.head is None:
                        self.last = None
                    self.size -= 1
                current = current.next

    def print_list(self):
        current = self.head

        while current:
            print(current.data, end=" ")
            current = current.next

        print("\n")

    def print_list_reverse(self):
        last = self.last

        while last:
            print(last.data, end=" ")
            last = last.previous
        print("\n")


# Example usage
list = DoublyLinkedList(max_size=1000)  # Set maximum size limit
list.append("Data 3")
list.append("Data 2")
list.append("Data 3")
list.append("Data 4")
list.append("Data 5")
list.append("Data 3")
list.print_list()
list.print_list_reverse()

list.remove("Data 3")
list.print_list()
list.print_list_reverse()
