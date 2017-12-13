#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2

#           "GC_GET2/templates"
#       "GC_GET2"
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class PretvornikHandler(BaseHandler):
    def get(self):
        return self.render_template("pretvornik razdalj.html")

    def post(self):
        km = self.request.get("vnos")
        milje = self.request.get("vnos2")

        if km:
            try:
                km = float(km)
                racun = km * 0.62
                return self.write("{} milj".format(racun))
            except ValueError:
                return self.write("Vnesi številko, ne '{}'".format(km))
        elif milje:
            try:
                milje = float(milje)
                racun2 = milje / 0.62
                return self.write("{} km".format(racun2))
            except ValueError:
                return self.write("Vnesi številko, ne '{}'".format(milje))


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/pretvornik', PretvornikHandler)
], debug=True)
