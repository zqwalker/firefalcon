import falcon


class Authorize(object):
    def __init__(self, responder=None):
        self._responder = responder

    def __call__(self, req, resp, resource, params):
        if resource.allowed is None:
            return
        
        if not req.context.token:
            return
        
        if not req.context.token.get("role") == 'admin':
            if self._responder not in resource.allowed:
                msg = "User not authorized."
                raise falcon.HTTPUnauthorized("Unauthorized", msg)
        return
