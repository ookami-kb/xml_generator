# -*- coding: utf-8 -*-

class AllowCrossDomainMiddleware(object):
    def process_response(self, request, response):
        if request.path.startswith('/api'):
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'X-Prototype-Version, X-Requested-With, Content-type, Accept'
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, PATCH'
        return response