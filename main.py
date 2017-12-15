#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Message


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
        liste = Message.query().fetch()
        parameters = {
            "nachrichten": liste
        }
        return self.render_template("hello.html", params=parameters)
    def post(self):
        name = self.request.get("name")
        email = self.request.get("email")
        nachricht = self.request.get("nachricht")
        message = Message(name=name,email=email,nachricht=nachricht)
        message.put()
        messages = Message.query().fetch()
        parameters = {
            "msg": message,
            "nachrichten": messages
        }
        return self.render_template("hello.html", params=parameters)

class DetailsHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))
        parameters = {
            "id" : message_id,
            "message": message
        }
        return self.render_template("details.html", params=parameters)
    def post(self,message_id):
        message = Message.get_by_id(int(message_id))
        message.name=self.request.get("name")
        message.email = self.request.get("email")
        message.nachricht = self.request.get("nachricht")
        message.put()
        return self.redirect_to("startseite")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="startseite"),
    webapp2.Route('/message/<message_id:\d+>', DetailsHandler)
], debug=True)
