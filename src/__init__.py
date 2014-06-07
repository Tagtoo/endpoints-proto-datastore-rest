import endpoints
from protorpc import remote

# TODO: need to refine method name
# TODO: allow user to override/insert method

class EndpointRestBuilder(object):
    def __init__(self, cls):
        self.cls = cls

    @property
    def name(self):
        return self.cls.__name__.lower()

    def build_model_insert(self, name, doc):
        def func(self, model):
            model.put()
            return model
        func.__name__ = name
        func.__doc__ = doc
        return func

    def build_model_list(self, name, doc):
        def func(self, query):
            return query

        func.__name__ = name
        func.__doc__ = doc
        return func

    def build_model_update(self, name, doc):
        def func(self, model):
            model.put()
            return model
        func.__name__ = name
        func.__doc__ = doc
        return func

    def build_model_get(self, name, doc):
        def func(self, model):
            return model
        func.__name__ = name
        func.__doc__ = doc
        return func

    def build_model_delete(self, name, doc):
        def func(self, model):
            model.key.delete()
        func.__name__ = name
        func.__doc__ = doc
        return func


    def gen_model_list(self):
        return self.cls.query_method(
            path='%s/list' % self.name ,
            http_method='GET',
            name="%s.list" % self.name,
            query_fields=('limit', 'pageToken')
        )(self.build_model_list(self.name, '%s list' % self.name))

    def gen_model_insert(self):
        return self.cls.method(
            path="%s" % self.name,
            http_method="POST",
            name="%s.insert" % self.name
        )(self.build_model_insert(self.name, '%s insert' % self.name))

    def gen_model_update(self):
        return self.cls.method(
            path="%s/{id}"% self.name,
            http_method="PUT",
            name="%s.update" % self.name
        )(self.build_model_update(self.name, '%s update' % self.name))

    def gen_model_get(self):
        return self.cls.method(
            path="%s/{id}"% self.name,
            http_method="GET",
            name="%s.get" % self.name,
        )(self.build_model_get(self.name, '%s get' % self.name))

    def gen_model_delete(self):
        return self.cls.method(
            path="%s/{id}" % self.name,
            http_method="DELETE",
            name="%s.delete" % self.name,
        )(self.build_model_delete(self.name, '%s delete' % self.name))


    def build(self, name, version, description):
        return endpoints.api(name=name.lower(), version=version, description=description)(
            type(
                name,
                (remote.Service, ),
                {
                    "%s_insert" % self.name: self.gen_model_insert(),
                    "%s_list" % self.name: self.gen_model_list(),
                    "%s_get" % self.name: self.gen_model_get(),
                    "%s_update"% self.name: self.gen_model_update(),
                    "%s_delete"%self.name: self.gen_model_delete()
                }
            )
        )
