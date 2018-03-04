# Python lightblue library

[![codecov.io](https://codecov.io/gh/Allda/python-lightblue/coverage.svg?branch=master)](https://codecov.io/gh/Allda/python-lightblue?branch=master)

[![Build Status](https://travis-ci.org/Allda/python-lightblue.svg?branch=master)](https://travis-ci.org/Allda/python-lightblue)

This is python library for [Lightblue][lightblue] database. It can be used as API 
interface.

## Example of usage
Levels of abstraction (from low to high):

### 1) LightBlueEntity and LightBlueService
Basic modules to query a LightBlue on a level of the request.

### 2) LightBlueQuery
Class that represents a query to LB in time
(both non-executed and executed states).
Has a relation to the LightBlueEntity.

Usage example:

```python
LightBlueQuery(_id='hash').find()
a = LightBlueQuery(('foo', '$neq', 'value'), bar='value2')
a._add_to_projection('foo', recursive=['bar'])
a._add_to_update(unset='foobar')
a.update()
LightBlueQuery.insert({'key': 'item'})
```

Why _add_to_projection() is private?
Because we have another level of abstraction...

### 3) LightBlueGenericSelection
- inherits LightBlueQuery and extends the functionality with post-processing,
so you can call:

```python
LightBlueGenericSelection(foo='value').find(
    check_response=True,
    selector='/processed/0/bar/',
    count=(1, 2),
    fallback=None,
    postprocess=lambda x: x.split('.')[-1])
```

so the query above will select documents with a specific foo value,
it will check the successful query of a LB response and count of response
documents of min 1 and max 2, with a fallback if it is out of range.
It will select 'bar' from the first response item and will process it with
the provided lambda.

That level of abstraction is generic because it is not specific to an entity.

## Dependencies
 - [BeanBag][beanbag]
 - [Dpath][dpath]


[lightblue]: https://www.lightblue.io/
[beanbag]: https://github.com/ajtowns/beanbag
[dpath]: https://github.com/akesterson/dpath-python
