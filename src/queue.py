class Queue:
    def __init__(self):
        self.queue = []

    def push(self, value):
        self.queue.append(value)

    def pop(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def front(self):
        if not self.is_empty():
            return self.queue[0]
        return None

    def back(self):
        if not self.is_empty():
            return self.queue[-1]
        return None

    def is_empty(self):
        return len(self.queue) == 0
