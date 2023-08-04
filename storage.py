from abc import ABC
from abc import abstractmethod
import time
import random

class AbstractStorage(ABC):
    @abstractmethod
    def fetch_tokens(self):
        '''
            Fetch the number of reminding tokens in the bucket.
        
            Returns:
                float: The reminding tokens in the bucket.
                (May be a negative result in multi-threaded applications)
        '''
    
    @abstractmethod
    def replenish(self):
        '''
            Replenish tokens.
            The basic idea is replenishing tokens in each time slot.
            But that requirs an extra thread to keep monitoring the bucket.
            If we have thounds of different buckets on the server machine, the CPU and memory resources will be wasted.

            So we use this lazy-method, it only replenish tokens when calling the limiter.
            
            Args:
                null
            Rerturns:
                null
        '''
    
    @abstractmethod
    def acquire(self, required_tokens):
        '''
            Remove the number of token entirely.
            It will wait for generating sufficent tokens.

            Args:
                required_tokens (int): Number of tokens required.
            Returns:
                True if success, False if blocked (need retry)
        '''


class InMemoryStorage(AbstractStorage):
    def __init__(self, rate, capacity):
        # init a full bucket
        self._token_number = capacity
        self._last_timestamp = time.time()
        self._capacity = capacity
        self._rate = rate

    def fetch_tokens(self):
        return self._token_number
    
    def replenish(self):
        now = time.time()

        # mitigate race conditions
        if now <= self._last_timestamp:
            return

        # lazy method, only replenish tokens before calling "acquire"
        self._token_number = min(self._token_number + self._rate * (now - self._last_timestamp), self._capacity)
        self._last_timestamp = now
    
    def acquire(self, required_tokens):
        if required_tokens > self._capacity:
            raise Exception("required_tokens > token bucket capacity")
        
        if self.fetch_tokens() < required_tokens:
            duration = (required_tokens - self.fetch_tokens()) / self._rate + random.random() * 0.3
            print('[Rate Limit trigged] wait for {} seconds.'.format(duration))
            time.sleep(duration)
            return False
        else:
            self._token_number -= required_tokens
            return True
        
