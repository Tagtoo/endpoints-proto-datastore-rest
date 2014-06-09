endpoints-proto-datastore-rest
==============================

a RESTful api generator for endpoints proto datastore


### Usage

```python
# generate restful api in one line
BigDataLab = EndpointRestBuilder(GPCode).build(
    api_name="BigDataLab",
    name="bigdatalab",
    version="v1",
    description="My Little Api"
)

# Customize api

builder = EndpointRestBuilder(GPCode)

# change the default list behavior
builder.set_list(func)

# add a endpoint api
builder.set_method(func, 'trigger')




```
