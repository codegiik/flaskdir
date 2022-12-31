BANNED_NAMES = ['vacwm', 'pasc4le']

def handler(**params):
    print("Scoped Middleware", params)
    
    if 'name' in params and params['name'] in BANNED_NAMES:
        return "Bad Request", 400
