# -*- coding: utf-8 -*-

__all__ = ('wrappers', 'Wrapper')

class WrappersSingleton(object):
    _wrappers = {}

    def __new__(cls):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it

    def register(self, name, wrapper, override=False):
        """
            Register the given wrapper
        """
        if not isinstance(wrapper(None, None), Wrapper):
            raise TypeError(u"You can only register a Wrapper not a {item|r}".format(item=wrapper))

        if name in self._wrappers and not override:
            raise AttributeError(u"{name} is already a valid wrapper type, try a new name".format(name=name))

        self._wrappers[name] = wrapper

    def copy(self):
        return dict(**self._wrappers)

    def __contains__(self, value):
        return value in self._wrappers

    def __getitem__(self, name):
        return self._wrappers.get(name)

    def __setitem__(self, *args):
        raise AttributeError

wrappers = WrappersSingleton()

class Wrapper(object):

    def __init__(self, errors, result):
        if isinstance(errors, basestring):
            errors = [errors,]
        self.errors = errors

        if self.errors:
            assert isinstance(self.errors, (list, tuple))

        self.result = result

    def build(self):
        raise NotImplemented

class DefaultWrapper(Wrapper):

    def build(self):
        result = {}
        if self.errors:
            result['success'] = False
        else:
            result['success'] = True
        if self.errors:
            result['errors'] = self.errors
        if self.result:
            result['result'] = self.result
        return result

class ExtJSFormWrapper(Wrapper):

    def build(self):
        result = {}
        if self.errors:
            result['success'] = False
        else:
            result['success'] = True
        if self.errors:
            errmsg, errors = self.errors[0], self.errors[1]
            assert isinstance(errmsg, basestring)
            assert isinstance(errors, dict)

            result['errormsg'] = errmsg
            result['errors'] = errors
        if self.result:
            result['data'] = self.result
        return result

wrappers.register('default', DefaultWrapper)
wrappers.register('extjsform', ExtJSFormWrapper)