Android API
====

register
----
    URL:
        /api/v1.0/register?username=&password=&cellphone=&identity=
    method:
        get
    parameters:
        username
        password
        cellphone
        identity: cellphone + uuid + 0
    json:
        {"status": 0}
        status: 0 for success, 1004 for existing username, 5000 for SQL exception
        
login
----
    URL:
        /api/v1.0/login?username=&password=&identity=
    method:
        get
    parameters:
        username
        password
        identity: cellphone + uuid + 0
    json:
        {"status": 0, "username": "", "cellphone": "", "email": "", "identity": "", "location": "", "class_order": "", "activity": ""}
        status: 0 for success, 1000 for login failed
        username: if login fail, username, cellphone, email, identity won't return
        cellphone
        email
        identity
        location: location id
        class_order: class id
        activity: activity id
        
confirm_cellphone
----
    URL:
        /api/v1.0/confirm_cellphone?cellphone=
    method:
        get
    parameters:
        cellphone
    json:
        {"status": 0}
        status: 0 for success, 1002 for existing cellphone
        
filter_organization
---
    URL:
        /api/v1.0/filter_organization?location=&property=&condition=
    method:
        get
    parameters:
        location: location id
        property: property id 
        condition: condition id
        location and property can repeat, but condition can't repeat
    json:
        {"status": 0, "organization": [{"id": "", "name": "", "location": "", "photo": "", "introduction": ""}, {"id": "", "name": "", "location": "", "photo": "", "introduction": ""}]}
        status: 0 for success
        id: 
        name: 
        photo: url of photo
        introduction
        