import endpoints
from protorpc import remote

# TODO: need to refine method name
# TODO: allow user to override/insert method

def _default_insert(self, model):
    model.put()
    return model

def _default_list(self, query):
    return query

def _default_update(self, model):
    model.put()
    return model

def _default_get(self, model):
    return model

def _default_delete(self, model):
    return model.key.delete()

def bind(func, name, doc):
    func.__name__ = name
    func.__doc__ = doc
    return func

class EndpointRestBuilder(object):
    def __init__(self, cls):
        self.cls = cls
        self.name = self.cls.__name__.lower()

        self._methods = {}

        self.set_insert(bind(_default_insert, "insert", "%s insert" % self.name))
        self.set_delete(bind(_default_delete, "delete", "%s delete" % self.name))
        self.set_update(bind(_default_update, "update", "%s update" % self.name))
        self.set_get(bind(_default_get, "get", "%s get" % self.name))
        self.set_list(bind(_default_list, "list", "%s list" % self.name))

    def set_method(self, func, method_name, **kwargs):
        self._methods[method_name] = self.cls.method(**kwargs)(func)

    def set_query_method(self, func, method_name, **kwargs):
        self._methods[method_name] = self.cls.query_method(**kwargs)(func)

    def set_get(self, func, **kwargs):
        self.set_method(
            func,
            "get",
            path="%s/{id}"% self.name,
            http_method="GET",
            name="%s.get" % self.name,
            **kwargs
        )

    def set_delete(self, func, **kwargs):
        self.set_method(
            func,
            "delete",
            path="%s/{id}" % self.name,
            http_method="DELETE",
            name="%s.delete" % self.name,
            **kwargs
        )

    def set_update(self, func, **kwargs):
        self.set_method(
            func,
            "update",
            path="%s/{id}"% self.name,
            http_method="PUT",
            name="%s.update" % self.name,
            **kwargs
        )

    def set_insert(self, func, **kwargs):
        self.set_method(
            func,
            "insert",
            path="%s" % self.name,
            http_method="POST",
            name="%s.insert" % self.name,
            **kwargs
        )

    def set_list(self, func, **kwargs):
        self.set_query_method(
            func,
            "list",
            path='%s/list' % self.name ,
            http_method='GET',
            name="%s.list" % self.name,
            query_fields=('limit', 'pageToken'),
            **kwargs
        )

    def build(self, api_name, **kwargs):
        return endpoints.api(**kwargs)(
            type(
                api_name,
                (remote.Service, ),
                self._methods
            )
        )
