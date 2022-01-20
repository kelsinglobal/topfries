# -*-  coding: utf-8 -*-
import json
import requests
from odoo import http
from odoo.http import Response, request
from xmlrpc import client

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
    
  
     #*******************************************************************************************************
     # -*- API Odoo*- 
     #*******************************************************************************************************
    
    @http.route('/topfries/api/apitestconn', auth='public', type="json", methods=['POST'], website=True)
    def apitestconn(self,**kw):
        url =str(kw.get('url','N/A'))
   
        common = client.ServerProxy("{}/xmlrpc/2/common".format(url))

        return common.version()

    @http.route('/topfries/api/apiauth', auth='public', type="json", methods=['POST'], website=True)
    def apiauth(self,**kw):
        url =str(kw.get('url','N/A'))
        db =str(kw.get('db','N/A'))
        username =str(kw.get('username','N/A'))
        password =str(kw.get('password','N/A'))
        
        common = client.ServerProxy("{}/xmlrpc/2/common".format(url))
        uid = common.authenticate(db, username, password, {})

        return uid

    @http.route('/topfries/api/apiaccrightsv1', auth='public', type="json", methods=['POST'], website=True)
    def apiaccrightsv1(self,**kw):
        url =str(kw.get('url','N/A'))
        db =str(kw.get('db','N/A'))
        uid =int(kw.get('uid',0))
        model =str(kw.get('model','N/A'))
        access =str(kw.get('access','N/A'))
        apikey =str(kw.get('apikey','N/A'))
        
        models = client.ServerProxy("{}/xmlrpc/2/object".format(url))

        model_access = models.execute_kw(db, uid, apikey,
                                model,'check_access_rights',
                                [access], {'raise_exception' : False})

        return model_access

    
    @http.route('/topfries/api/apiaccrightsv2', auth='public', type="json", methods=['POST'], website=True)
    def apiaccrightsv2(self,**kw):
        url =str(kw.get('url','N/A'))
        db =str(kw.get('db','N/A'))
        username =str(kw.get('username','N/A'))
        password =str(kw.get('password','N/A'))
        model =str(kw.get('model','N/A'))
        access =str(kw.get('access','N/A'))
        apikey =str(kw.get('apikey','N/A'))
        
        
        headers = {'Content-Type': 'application/json'}
        data ={
            "jsonrpc": "2.0", 
            "params": {
                "url": url,
                "db": db,
                "username": username,
                "password": password
            }
        }
        
        data_json = json.dumps(data)
        
        url_auth = url + '/topfries/api/apiauth'
        r = requests.post(url=url_auth, data=data_json, headers=headers)
        y =  json.loads(r.content )
        uid = y["result"]
        
        models = client.ServerProxy("{}/xmlrpc/2/object".format(url))

        model_access = models.execute_kw(db, uid, apikey,
                                model,'check_access_rights',
                                [access], {'raise_exception' : False})

        return model_access
    
    
    
    @http.route('/topfries/api/apigetfields', auth='public', type="json", methods=['POST'], website=True)
    def apigetfields(self,**kw):
        url =str(kw.get('url','N/A'))
        db =str(kw.get('db','N/A'))
        uid =int(kw.get('uid',0))
        model =str(kw.get('model','N/A'))
        apikey =str(kw.get('apikey','N/A'))
        
        models = client.ServerProxy("{}/xmlrpc/2/object".format(url))

        fields = models.execute_kw(db, uid, apikey,
                                   model,'fields_get',
                                   [],{'attributes': ['string', 'type', 'required']})

        return fields
    
    @http.route('/topfries/api/apisearch_read', auth='public', type="json", methods=['POST'], website=True)
    def apisearch_read(self,**kw):
        url =str(kw.get('url','N/A'))
        db =str(kw.get('db','N/A'))
        uid =int(kw.get('uid',0))
        model =str(kw.get('model','N/A'))
        apikey =str(kw.get('apikey','N/A'))
        
        models = client.ServerProxy("{}/xmlrpc/2/object".format(url))

        info = models.execute_kw(db, uid, apikey,
                            model,'search_read',[])


        return info
    

    #https://www.odoo.com/es_ES/forum/ayuda-1/send-parameters-to-a-controller-from-a-form-action-147463
    @http.route('/topfries/api/apisearch_saleorder/<string:name>', auth='public', type="json", methods=['POST'], website=True)
    def apisearch_saleorder(self,name,**kw):
        url =str(kw.get('url','N/A'))
        db =str(kw.get('db','N/A'))
        uid =int(kw.get('uid',0))
        model =str(kw.get('model','N/A'))
        apikey =str(kw.get('apikey','N/A'))
        
        response = request.jsonrequest
            
        models = client.ServerProxy("{}/xmlrpc/2/object".format(url))

        info = models.execute_kw(db, uid, apikey,
                            model,'search_read',
                            [[['name', '=', name]]])


        return info


    @http.route('/topfries/api/apisearch_saleorderv2/<string:name>', auth='public', type="json", methods=['POST'], website=True)
    def apisearch_saleorderv2(self,name,**kw):
        url =str(kw.get('url','N/A'))
        db =str(kw.get('db','N/A'))
        uid =int(kw.get('uid',0))
        model =str(kw.get('model','N/A'))
        apikey =str(kw.get('apikey','N/A'))
        
       
        #Retorna todo el Body
        response = request.jsonrequest
        
        #Extrae solo el contenido de params
        response2 =  http.request.params
        
        #https://www.odoo.com/es_ES/forum/ayuda-1/how-to-get-json-data-in-an-odoo-controller-using-type-json-166743
        
        #Retorna todo el Body
        reqdata= request.httprequest.data
        
        #Retorna JSON de los argumentos (Query String)
        reqargs= request.httprequest.args
        
        models = client.ServerProxy("{}/xmlrpc/2/object".format(url))

        #info = models.execute_kw(db, uid, apikey,
        #                    model,'search_read',
        #                    [[['name', '=', name]]])


        return response2
    