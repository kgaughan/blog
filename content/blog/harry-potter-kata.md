Title: Harry Potter Kata
Date: 2008-12-31 00:44
Category: Coding
Status: published

I did the [Harry Potter Kata](http://codingdojo.org/kata/Potter/) earlier because I was feeling a little bored. Here's the result. I use cents rather than euros as my unit of currency here.

I'd a start when I was thinking about how I'd solve the problem. I thought that being greedy and trying to make the biggest sets would do the trick, but the first example test case given soon managed to disabuse me of that notion.

Then I got the idea of turning things around 90 degrees by creating a set of buckets within the basket and distributing the sets between them. However, given the sample test case, I realised that the maximum discount could come from an obscure distribution of books, so I took the brute force route and decided to enumerate all the possible ways to distribute all the books of a certain volume, tracking which combination gave the greatest discount, and did this iteratively for each volume.

I already had the intuition to eliminate the larger groups of volumes sooner than the smaller ones, and I knew that the important thing was the number of books of each volume there were rather than what the particular volumes were, so sorting basket by volume made sense and avoided the need to do any backtracking later.

I looked at other implementations after I'd finished, and mine seems to be sorter and more general--though not purposely so--than most, but I'm still pretty sure there's a much more elegant way to find an ideal distribution of volumes than the brute force method I used, though I've yet to think of one. Here's the code:

```python
#!/usr/bin/env python

import doctest
import itertools


def sum_basket(basket, unit_price, discount_pcs):
    """
    Gets the sum price of the books in the basket.

    basket - list of number of each book
    unit_price - price of a book
    discount_pcs - percentage discount to apply for each additional book in a set

    >>> price = 800
    >>> discount_pcs = [0, 0, 5, 10, 20, 25]
    >>> sum_basket([0, 0, 0, 0, 0], price, discount_pcs)
    0
    >>> sum_basket([0, 1, 0, 0, 0], price, discount_pcs)
    800
    >>> sum_basket([0, 3, 0, 0, 0], price, discount_pcs)
    2400
    >>> sum_basket([1, 1, 0, 0, 0], price, discount_pcs)
    1520
    >>> sum_basket([2, 1, 2, 1, 0], price, discount_pcs)
    4080
    >>> sum_basket([2, 1, 1, 1, 1], price, discount_pcs)
    3800
    >>> sum_basket([2, 2, 2, 1, 1], price, discount_pcs)
    5120
    >>> sum_basket([1, 1, 2, 2, 2], price, discount_pcs)
    5120
    >>> sum_basket([5, 5, 4, 5, 4], price, discount_pcs)
    14120
    """
    buckets = get_basket_buckets(basket)
    result = 0

    for books in sorted(basket, reverse=True):
        best = None
        for patterns in bitmap_combinations(books, len(buckets)):
            attempt = [x + y for x, y in itertools.izip(buckets, patterns)]
            attempt_sum = 0
            for bucket in attempt:
                attempt_sum += sum_bucket(bucket, unit_price, discount_pcs)
            if best is None or attempt_sum < result:
                best = attempt
                result = attempt_sum
        buckets = best

    return result


def sum_bucket(bucket, unit_price, discount_pcs):
    """
    Gets the sum cost of a set of books.

    bucket - number of unique books in a set.
    unit_price - price of a book
    discount_pcs - percentage discount to apply for each additional book in a set

    >>> price = 800
    >>> discount_pcs = [0, 0, 5, 10, 20, 25]
    >>> sum_bucket(0, price, discount_pcs)
    0
    >>> sum_bucket(1, price, discount_pcs)
    800
    >>> sum_bucket(2, price, discount_pcs)
    1520
    >>> sum_bucket(3, price, discount_pcs)
    2160
    >>> sum_bucket(4, price, discount_pcs)
    2560
    >>> sum_bucket(5, price, discount_pcs)
    3000
    """
    return bucket * unit_price * (100 - discount_pcs[bucket]) / 100


def bitmap_combinations(ones, length):
    if length == 0:
        yield []
    else:
        if ones < length:
            for tail in bitmap_combinations(ones, length - 1):
                yield itertools.chain([0], tail)
        if ones > 0:
            for tail in bitmap_combinations(ones - 1, length - 1):
                yield itertools.chain([1], tail)


def get_basket_buckets(basket):
    """
    Creates enough basket buckets to hold the maximum number of unique book sets in
    the basket.

    >>> get_basket_buckets([0])
    []
    >>> get_basket_buckets([0, 0])
    []
    >>> get_basket_buckets([1, 0])
    [0]
    >>> get_basket_buckets([0, 1])
    [0]
    >>> get_basket_buckets([0, 2])
    [0, 0]
    >>> get_basket_buckets([1, 2])
    [0, 0]
    >>> get_basket_buckets([1, 2, 3, 5, 2])
    [0, 0, 0, 0, 0]
    """
    return [0 for i in range(max(basket))]


def _test():
    doctest.testmod()


if __name__ == '__main__':
    _test()
```
