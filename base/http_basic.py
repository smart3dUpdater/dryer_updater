from tornado import web
from tornado import concurrent

class BasicHandler(web.RequestHandler):

    executor = concurrent.futures.ThreadPoolExecutor(5)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    
    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def render(self, template_name, **kwargs):
        kwargs.update({'where': self.application.where})
        return super(BasicHandler, self).render(template_name, **kwargs)