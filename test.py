from .limiter import TokenBucket
from .storage import InMemoryStorage
import time
import sys
import random

MAX_RPS = 100
BURST_RPS = 300


# ======= 1. single batch requests

# 1.1 post 80 requests, return True, rate limit will not be triggered (normal case)
def single_batch_80():
    token_bucket = TokenBucket(InMemoryStorage(MAX_RPS, BURST_RPS))
    token_bucket.acquire(80)
    print(sys._getframe().f_code.co_name + " passed" + '\n')


# 1.2 post 300 requests, return True, rate limit will not be triggered (burst case)
def single_batch_300():
    token_bucket = TokenBucket(InMemoryStorage(MAX_RPS, BURST_RPS))
    token_bucket.acquire(300)
    print(sys._getframe().f_code.co_name + " passed" + '\n')

# 1.3 post 500 requests, return False, rate limit will be triggered (> burst case)
# this should never happen!!!!!
def single_batch_500():
    token_bucket = TokenBucket(InMemoryStorage(MAX_RPS, BURST_RPS))
    token_bucket.acquire(500)
    # no tokens will be consumed
    assert token_bucket._storage.fetch_tokens() == 300
    print(sys._getframe().f_code.co_name + " passed" + '\n')


# ======= 2. multi batch requests

# 2.1 post [80, 80, 80, 80] requests, return [True, True, True, False]
def multi_batch_80_80_80_80():
    token_bucket = TokenBucket(InMemoryStorage(MAX_RPS, BURST_RPS))
    token_bucket.acquire(80)
    token_bucket.acquire(80)
    token_bucket.acquire(80)

    token_bucket.acquire(80)
    print("remaining tokens: " + str(token_bucket._storage.fetch_tokens()))

    print(sys._getframe().f_code.co_name + " passed" + '\n')


# 2.1 post [80, 80, 80, 80, wait 1s, 80, 80] requests
def multi_batch_80_80_80_80_1s_80_80():
    token_bucket = TokenBucket(InMemoryStorage(MAX_RPS, BURST_RPS))
    token_bucket.acquire(80)
    token_bucket.acquire(80)
    token_bucket.acquire(80)

    token_bucket.acquire(80)

    token_bucket.acquire(80)

    token_bucket.acquire(80)

    print("remaining tokens: " + str(token_bucket._storage.fetch_tokens()))

    print(sys._getframe().f_code.co_name + " passed" + '\n')


def app():
    token_bucket = TokenBucket(InMemoryStorage(MAX_RPS, BURST_RPS))
    i = 0
    while i < 100:
        random_request_num = random.randint(30, 200)
        token_bucket.acquire(random_request_num)
        # DO SOMETHING.....
        print("request {} tokens, remain {} tokens in bucket.".format(random_request_num, token_bucket._storage.fetch_tokens()))
        i += 1


# single_batch_80()
# single_batch_300()
# single_batch_500()

# multi_batch_80_80_80_80()
# multi_batch_80_80_80_80_1s_80_80()

app()