Android API
====

register
----
    URL:
        /api/v1.0/register?&password=&cellphone=&identity=&email=
    method:
        get
    parameters:
        password
        cellphone
        email
        identity: cellphone + uuid + 0
    json:
        {"status": ["0"], "user": {"username": "", "cellphone": "", "identity": "", "email": ""}}
        
        status: 0 for success, 1002 for existing cellphone, 1004 for existing username, 5000 for SQL exception
        username
        cellphone
        identity
        email
        
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
         "user": {"username": "", "cellphone": "", "email": "", "identity": ""}}
             
        status: 0 for success, 1000 for login failed
        username: if login fail, username, cellphone, email, identity won't return
        cellphone
        email
        identity
        
filter_organization
---
    URL:
        /api/v1.0/filter_organization?city=&district=&city=&district=&city=&district=&page=
        /api/v1.0/filter_organization?property=&property=&property=&page=  
        /api/v1.0/filter_organization?condition=&page=
        /api/v1.0/filter_organization?distance=&latitude=&longitude=&page=
    method:
        get
    parameters:
        city: name of a city
        district: name of a district
        property: property id
        condition: condition id
        distance
        latitude
        longitude
        page
        location and property can repeat, but condition can't repeat
        distance can coexist with another parameter (location OR property OR condition)
    json:
        {"status": 0,
         "organizations": [{"id": "", "name": "", "city": "", "district": "", "photo": "", "intro": "", "view_count"/"comments_count"/"orders_count": ""}]}
         
        status: 0 for success
        organizations: a list of organizations
            id
            name
            city
            district
            photo: url of photo
            intro
            view_count/comments_count/order_count
        
organization_detail
---
    URL:
        /api/v1.0/organization_detail?organization=&content=&page=
    method:
        get
    parameters:
        organization: id of organization
        page
        content: 0 for organization detail, 1 for classes list, 2 for activities list
    json:
        {"status": 0,
         "organization": {"id": "", "name": "", "city": "", "district": "", "photo": "", "intro": "", "address": "",
            "cellphone": "", "comments_count": ""},
         "classes": [{"id": "", "name": "", "age": "", "price": "", "start_time": "", "end_time": ""}],
         "activities": [{"id": "", "name": "", "age": "", "price": "", "start_time": "", "end_time": ""}]}
         
        status: 0 for success, 2000 for organization not exist
        organization
            id
            name
            city
            district
            photo: url of photo
            intro
            address
            cellphone
            comments_count
        classes/activities: a list of classes/activities
            id
            name
            age
            price
            start_time
            end_time
    
order_list
---
    URL:
        /api/v1.0/order_list?username=&cellphone=&page=
    method:
        get
    parameters:
        username
        cellphone
        page
    json:
        {"status": 0,
         "orders": [{"class_order_id": "", "timestamp": "", "class_name": "", "org_name": ""},
            {"activity_order_id": "", "timestamp": "", "activity_name", "", "org_name": ""}]}
         
         status: 0 for success, 1003 for user not exist
         class_order_id/activity_order_id
         class_name/activity_name
         timestamp
         org_name
         
order_detail
---
    URL:
        /api/v1.0/order_list?username=&cellphone=&class_order=&activity_order=
    method:
        get
    parameters:
        username
        cellphone
        class_order/activity_order
    json:
        {"status": 0,
         "class": [{"time": "", "timestamp": "", "class_name": "", "org_name": "", "name": "", "age": "", "sex": "",
             "cellphone": "", "address": "", "remark": ""}],
         "activity": [{"timestamp": "", "activity_name": "", "org_name": "", "name": "", "age": "", "sex": "",
             "cellphone": "", "address": "", "remark": ""}]}
         
        status: 0 for success, 1003 for user not exist, 1005 for access restricted, 1006 for order not exist
        class/activity
        timestamp: timestamp of order
        time: ONLY included in classes, the try time of class
        class_name/activity_name
        name: user's name
        age
        sex
        cellphone
        address: user's address
        remark: user's remark of a class or activity
    
register_requirement
---
    URL:
        /api/v1.0/register_requirement?name=&cellphone=&need=&page=&method=
    method:
        get
    parameters:
        method: 0 for get, 1 for post
        username
        cellphone
        need
        page
    json:
        {"status": 0}
        {"status": 0, "registers": [{"name": "", "cellphone": "", "need": "", "time": ""}]}
        registers: a list of registers
            name
            cellphone
            need
            time
            
CONSTANTS
---
    SUCCESS = 0
    
    LOGIN_FAILED = 1000
    CELLPHONE_NOT_EXISTS = 1001
    CELLPHONE_EXISTS = 1002
    USER_NOT_EXISTS = 1003
    USERNAME_EXISTS = 1004
    ACCESS_RESTRICTED = 1005
    ORDER_NOT_EXISTS = 1006
    
    ORGANIZATION_NOT_EXISTS = 2000
    
    SQL_EXCEPTION = 5000
    PARAMETER_ERROR = 5001
    
    VIEW_COUNT = 0
    COMMENTS_COUNT = 1
    ORDER_COUNT = 2
    
    PER_PAGE = 10
    
    ORGANIZATION_DETAIL = 0
    CLASSES_LIST = 1
    ACTIVITIES_LIST = 2
    
    GET = 0
    POST = 1
    