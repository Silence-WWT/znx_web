Android API
====

register
----
    URL:
        /api/v1.0/register?&password=&cellphone=&identity=
    method:
        get
    parameters:
        password
        cellphone
        identity: cellphone + uuid + 0
    json:
        {"status": 0, "username": "", "cellphone": "", "identity": ""}
        
        status: 0 for success, 1004 for existing username, 5000 for SQL exception
        username
        cellphone
        identity
        
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
        {"status": 0,
         "user": {"username": "", "cellphone": "", "email": "", "identity": ""},
         "classes": [{"time": "", "timestamp": "", "class_name": "", "org_name": "", "name": "", "age": "", "sex": "",
             "cellphone": "", "address": "", "remark": ""}],
         "activities": [{"timestamp": "", "activity_name": "", "org_name": "", "name": "", "age": "", "sex": "",
             "cellphone": "", "address": "", "remark": ""}]}
             
        status: 0 for success, 1000 for login failed
        username: if login fail, username, cellphone, email, identity won't return
        cellphone
        email
        identity
        classes: a list of classes
        activities: a list of activities
        timestamp: timestamp of order
        time: ONLY included in classes try time of class
        class_name/activity_name
        org_name:
        name: name of user
        age
        sex
        cellphone
        address
        remark: user's remark of a class or activity
        
        
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
        {"status": 0,
         "organizations": [{"id": "", "name": "", "location": "", "photo": "", "intro": ""}]}
         
        status: 0 for success
        organizations: a list of organizations
        id
        name
        photo: url of photo
        intro
        