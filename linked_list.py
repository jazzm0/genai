import threading


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self, max_size=None):
        self.head = None
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
            else:
                last = self.head
                while last.next:
                    last = last.next
                last.next = new_node
            self.size += 1

    def __delitem__(self, data):
        with self.lock:
            if self.head is None:
                return
            else:
                last = self.head
                while last.next:
                    if self.head.data == data:
                        self.head = self.head.next
                        self.size -= 1
                    elif last.next.data == data:
                        last.next = last.next.next
                        self.size -= 1
                    else:
                        last = last.next

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next
        print("\n")


# Example usage
list = LinkedList(max_size=1000)  # Set maximum size limit
list.append("Data 3")
list.append("Data 2")
list.append("Data 3")
list.append("Data 4")
list.append("Data 5")
list.append("Data 3")
list.print_list()

del list["Data 3"]
list.print_list()
