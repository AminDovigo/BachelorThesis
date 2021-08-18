#!/usr/bin/env python

class Library(object):
    def __init__(self, books, signup, rate):
            super(Library, self).__init__()
            self.books = books
            self.signup = signup
            self.rate = rate

class Instance(object):
    def __init__(self, days, books, libraries):
            super(Instance, self).__init__()
            self.days = days
            self.books = books
            self.libraries = libraries

def loadInstance(filename):
    with open(filename) as fp:
            # read metadata
            nbooks, nlibs, ndays = [int(x) for x in fp.readline().split()]
            assert(nbooks >= 1 and nbooks <= 100000)
            assert(nlibs >= 1 and nlibs <= 100000)
            assert(ndays >= 1 and ndays <= 100000)
            # read books
            books = [int(x) for x in fp.readline().split()]
            assert(len(books) == nbooks)
            for b in books:
                assert(b >= 0 and b <= 1000)
            # read libraries
            libraries = []
            for l in range(nlibs):
                nb, signup, rate = [int(x) for x in fp.readline().split()]
                assert(nb >= 1 and nb <= 100000)
                assert(signup >= 1 and signup <= 100000)
                assert(rate >= 1 and rate <= 100000)
                libbooks = [int(x) for x in fp.readline().split()]
                assert(len(libbooks) == nb)
                for b in libbooks:
                    assert(b >= 0 and b < nbooks)
                libraries.append(Library(libbooks, signup, rate))
            print("Read instance with %i books %i libraries and %i days" % (nbooks, nlibs, ndays))
            return Instance(ndays, books, libraries)

class Order(object):
    def __init__(self, libID, books):
            super(Order, self).__init__()
            self.libID = libID
            self.books = books

class Solution(object):
    def __init__(self, orders):
            super(Solution, self).__init__()
            self.orders = orders

def loadSolution(filename):
    with open(filename) as fp:
            # read metadata
            nlibs = int(fp.readline())
            assert(nlibs >= 0 and nlibs <= 100000)
            # read orders
            orders = []
            for l in range(nlibs):
                libID, nb = [int(x) for x in fp.readline().split()]
                assert(libID >= 0 and libID < 100000)
                assert(nb >= 1 and nb <= 100000)
                books = [int(x) for x in fp.readline().split()]
                assert(len(books) == nb)
                orders.append(Order(libID, books))
            print("Read solution with %i libraries" % nlibs)
            return Solution(orders)

def checkSolution(instance, solution):
    for order in solution.orders:
            assert(order.libID < len(instance.libraries))
            booksInLibrary = set(instance.libraries[order.libID].books)
            booksInOrder = set(order.books)
            assert(booksInOrder.issubset(booksInLibrary))

def evaluateSolution(instance, solution):
    scannedBooks = set()
    daysLeft = instance.days
    for order in solution.orders:
        library = instance.libraries[order.libID]
        daysLeft -= library.signup
        # stop if no time left
        if daysLeft <= 0:
            break
        # compute how many books we can actually scan from the order
        maxBooks = min(daysLeft*library.rate, len(order.books))
        # add them to set of books to scan
        for b in range(maxBooks):
            scannedBooks.add(order.books[b])
    # compute total score of scanned books
    score = 0
    for b in scannedBooks:
        score += instance.books[b]
    return score

if __name__ == '__main__':
    import sys
    instance = loadInstance(sys.argv[1])
    solution = loadSolution(sys.argv[2])
    checkSolution(instance, solution)
    print("Solution value =", evaluateSolution(instance, solution))
