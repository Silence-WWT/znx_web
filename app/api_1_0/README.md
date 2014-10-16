Android API
====

register
----
    URL:
        domain/api/v1.0/register?username=&password=&cellphone=
    method:
        get
    parameters:
        username
        password
        cellphone
    json:
        {"status": 0}
        status: 0 for success, 1004 for existing username, 5000 for SQL exception
        
login
----
    URL:
        domain/api/v1.0/login?username=&password=&uuid=
    method:
        get
    parameters:
        username
        password
        uuid
    json:
        {"status": 0}
        status: 0 for success, 1000 for login failed
        
confirm_cellphone
----
    URL:
        domain/api/v1.0/login?cellphone=
    method:
        get
    parameters:
        cellphone
    json:
        {"status": 0}
        status: 0 for success, 1002 for existing cellphone
        