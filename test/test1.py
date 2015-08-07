# tests from Perl version of jsonpath: JSONPathTest.pm
# at http://github.com/masukomi/jsonpath-perl/tree/master
# $Id: test1.py,v 1.4 2008/11/11 17:53:32 phil Exp $

import jsonpath
import jsonmatch

tests = 0
def ok():
    global tests
    tests += 1

test = \
{ "store": {
    "book": [ 
      { "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      { "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 12.99
      },
      { "category": "fiction",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 8.99
      },
      { "category": "fiction",
        "author": "J. R. R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    }
  }
}

def test_normalize():
    def check(input, expected):
        got = jsonpath.normalize(input)
        if got != expected:
            raise Exception("got %s expected %s" % (got, expected))
        ok()

    check('$..author', '$;..;author')
    check('$.store.book[*].author', '$;store;book;*;author')
    check('$.store.*', '$;store;*')
    check('$..book[2]', '$;..;book;2')
    check('$..book[(@.length-1)]', '$;..;book;(@.length-1)')
    check('$..book[-1:]', '$;..;book;-1:')
    check('$..book[0,1]', '$;..;book;0,1')
    check('$..book[:2]', '$;..;book;:2')
    check('$..book[?(@.isbn)]', '$;..;book;?(@.isbn)')
    check('$..book[?(@.price<10)]', '$;..;book;?(@.price<10)')
    check('$.store..price', '$;store;..;price')
    check('$..*', '$;..;*')

def test_array_retrieval():
    def check(expr, exp_len):
        result = jsonpath.jsonpath(test, expr)
        assert result != 0
        assert len(result) == exp_len
        ok()
        return result

    check('$.store.book[*].author', 4)
    check('$..author', 4)
    result = check('$..book[?(@.price<10)]', 2)
    expected = [
    	{"category":"reference", "author":"Nigel Rees", "title":"Sayings of the Century", "price":8.95}, 
        {"category":"fiction", "author":"Herman Melville", "title":"Moby Dick", "isbn":"0-553-21311-3", "price":8.99}
    ]
    assert jsonmatch.jsonmatch(result, expected)

    for book in result:
        assert 'category' in book
        assert 'author' in book
        assert 'title' in book
        assert 'price' in book
        if 'isbn' in book:
            # moby dick
            assert 8.99 == book['price']
            assert 'Moby Dick' == book['title']
        else:
            #sayings of the century
            assert 8.95 == book['price']
            assert 'Sayings of the Century' == book['title']

    check('$.store.*', 2)       #book array and one bicycle

    result = check('$.store..price', 5) #the price of everything
    assert jsonmatch.jsonmatch(result, [ 8.95, 12.99, 8.99, 22.99, 19.95 ])

    check('$..book[0,1]', 2)

    check('$..book[:2]', 2)

    check('$..book[?(@.isbn)]', 2)

    check('$.store.!', 2)       #the keys in the store hash 

    check('$..*', 27)

test_normalize()
test_array_retrieval()

print tests, "tests passed"
