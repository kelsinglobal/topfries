# -*-  coding: utf-8 -*-
import json
import requests
from odoo import http
from odoo.http import Response, request

class TopFries(http.Controller) :
    @http.route('/topfries/api', auth='public', website=True)
    def index(self,**kw):
        return "Hello, world"

    # -*-  obtener Querystring de peticion get
    # https://www.odoo.com/es_ES/forum/ayuda-1/send-parameters-to-a-controller-from-a-form-action-147463 -*-
    @http.route('/topfries/api/get_querystring', auth='public', website=True)
    def get_querystring(self,**kw):
        nombre =str(kw.get('nombre','N/A'))
        direccion =str(kw.get('direccion','N/A'))
        telefono =str(kw.get('telefono','N/A'))
        result ={
            'success': True,
            'status': 'OK',
            'code': 200,
            'nombre': nombre, 
            'direccion': direccion,  
            'telefono': telefono
        }
        #return "nombre= " + nombre + "  direccion= " + direccion + "  telefono= " + telefono
        return Response(json.dumps(result), 
                        content_type='application/json;charset=utf-8',
                        status=200)
                
    # -*-  https://stackoverflow.com/questions/58470669/how-to-make-a-controller-on-odoo-for-custom-value -*-
    @http.route('/topfries/api/get_parameter/<string:str_val>', auth='public', website=True)
    def get_string(self,str_val):
        result = str_val
        return Response(json.dumps(result), 
                        content_type='application/json;charset=utf-8',
                        status=200)
    
    
   # -*- https://www.odoo.com/es_ES/forum/ayuda-1/get-data-from-post-request-144931
   #     para realizar la peticion post enviar en el cuerpo Json vacio '{}'*- 
    @http.route('/topfries/api/post_test', auth='public', type="json", methods=['POST'], website=True)
    def post_test(self,**kw):
       return {
           'success': True,
           'status': 'OK',
           'code': 200
       }


    # -*- Obtener parametros de la peticion POST*- 
    # https://www.odoo.com/es_ES/forum/ayuda-1/get-post-parameters-from-an-incoming-request-to-a-controller-182785       
    # https://www.programmerall.com/article/16251046087/
    @http.route('/topfries/api/post_read_arguments', auth='public', type="json", methods=['POST'], website=True)
    def post_read_arguments(self,**kw):
        # POST data
        response = request.jsonrequest
        x=json.dumps(response)
        nombre = kw.get('nombre', False)
        return nombre

    
     #*******************************************************************************************************
     # -*- Autenticacion de Usuario*- 
     #*******************************************************************************************************
    
    
    # -*- Autenticacion de Usuario*- 
    
    @http.route('/topfries/api/obtener_session_id', auth='public',type="json", methods=['POST'], website=True)
    def obtener_session_id(self,**kw):
        db = kw.get('db', False)
        login = kw.get('login', False)
        password = kw.get('password', False)
        base_url = kw.get('base_url', False)
        resource = kw.get('resource', False)
        
        url = base_url + resource
      
    
        headers = {'Content-Type': 'application/json'}
        #data ={
            #"jsonrpc": "2.0", 
            #"params": {
            #    "db": db,
            #    "login": login,
            #    "password": password
            #}
        #}
        
        data ={
             "db": db,
             "login": login,
             "password": password
        }
        
        
        data_json = json.dumps(data)
        
        session_details  = requests.post(url=url, data=data_json, headers=headers)
        
        session_id = str(session_details.cookies.get('session_id'))
        
        return session_id
    
    
    @http.route('/topfries/api/auth_user', auth='user', website=True)
    def auth_user(self,**kw):
        return "Hello, world"
    
    
    @http.route('/topfries/api/call_auth_user', auth='public', website=True)
    def call_auth_user(self,**kw):
        
        session_id = str(kw.get('s_id','N/A')) 
   
        cookies = {
            'session_id': session_id 
        }
        
        url_get = "https://kelsinglobal-topfries-dev-3998292.dev.odoo.com/topfries/api/auth_user"
        res = requests.get(url_get, cookies=cookies)
        
        return res.text
    
  