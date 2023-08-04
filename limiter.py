class TokenBucket(object):
    def __init__(self, storage):
        self._storage = storage
    
    def acquire(self, required_tokens = 1):
        while True:
            self._storage.replenish()
            if self._storage.acquire(required_tokens):
                break