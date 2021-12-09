# -*-  coding: utf-8 -*-

from odoo import http

class TopFries(http.Controller) :
    @http.route('/topfries/', auth='public', website=True)
    def index(self,**kw):
        return "Hello, world"
