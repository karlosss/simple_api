class BookDB:
    def __init__(self, id, page_count, title):
        self.id = id
        self.page_count = page_count
        self.title = title


class BookWithIsbnDB:
    def __init__(self, id, page_count, title, isbn=None):
        self.id = id
        self.page_count = page_count
        self.title = title
        self.isbn = isbn


class NodeDB:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next
