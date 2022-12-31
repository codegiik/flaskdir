def handler(**params):
    print("Scoped Middleware", params)
    
    if 'name' in params and params['name'] == 'pasc4le':
        return "Bad Request", 400
