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
        {"status": 0, "user": {"username": "", "cellphone": "", "identity": "", "email": ""}}
        
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
        /api/v1.0/filter_organization?city=&district=&page=
        /api/v1.0/filter_organization?profession=&page=  
        /api/v1.0/filter_organization?distance=&latitude=&longitude=&page=
    method:
        get
    parameters:
        city: name of a city
        district: name of a district
        profession: name of  profession
        distance
        latitude
        longitude
        page
        distance can coexist with another parameter (location OR profession)
    json:
        {"status": 0,
         "organizations": [{"id": "", "name": "", "city": "", "district": "", "photo": "", "intro": ""}]}
         
        status: 0 for success, 5001 for parameter error
        organizations: a list of organizations
            id
            name
            city
            district
            photo: url of photo
            intro
        
organization_detail
---
    URL:
        /api/v1.0/organization_detail?organization=
    method:
        get
    parameters:
        organization: id of organization
    json:
        {"status": 0,
         "organization": {"id": "", "name": "", "city": "", "district": "", "photo": "", "intro": "", "address": "",
            "cellphone": "", "comments_count": "", "stars": ""}}
         
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
            stars: a float number for stars
    
organization_comment
---
    URL:
        /api/v1.0/organization_comment?organization=&username&comment=&stars=
    method:
        get
    parameters:
        organization: id of organization
        username
        comment
        stars
    json:
        {"status": 0}
        
        status: 0 for success, 2000 for organization not exist, 5000 for sql exception, 5001 for parameter error

organization_comment_list
---
    URL:
        /api/v1.0/organization_comment_list?organization=&page=
    method:
        get
    parameters:
        organization: id of organization
        page
    json:
        {"status": 0,
         "organization_comments": [{"comment": "", "timestamp": "", "stars": "", "username": ""}]}
        
        status: 0 for success, 2000 for organization not exist, 5001 for parameter error
        organization_comments: a list of organization_comments
            comment
            stars
            timestamp
            username
        
class_list
---
    URL:
        /api/v1.0/class_list?organization=&page=
    method:
        get
    parameters:
        organization: id of organization
        page
    json:
        {"status": 0,
         "classes": [{"id": "", "name": "", "age": "", "price": "", "start_time": "", "end_time": ""}]}
        
        status: 0 for success
        classes: a list of classes
            id
            name
            age
            price
            start_time
            end_time
    
class_detail
---
    URL:
        /api/v1.0/class_detail?class=
    method:
        get
    parameters:
        class: id of class
    json:
        {"status": 0,
         "class": {"id": "", "name": "", "age": "", "price": "", "intro": "", "try": "", "consult_time": "",
            "start_time": "", "end_time": "", "comments_count": "", "course_count": ""}}
        
        status: 0 for success, 2001 for class not exist
        class: a dict of class
            id
            name
            age
            price
            intro
            try
            consult_time
            start_time
            end_time
            comments_count
            course_count
    
class_sign_up
---
    URL:
        /api/v1.0/class_sign_up?class=&username=&name=&cellphone=&age=&sex=&address=&remark=&email=&time=
    method:
        get
    parameters:
        class: id of class
        username
        name
        cellphone
        age
        sex
        address
        remark
        email
        time: YYYY-mm-dd
    json:
        {"status": 0}
        
        status: 0 for success, 5002 for lack of parameters
    
class_comment
---
    URL:
        /api/v1.0/class_comment?class=&username&comment=&stars=
    method:
        get
    parameters:
        class: id of class
        username
        comment
        stars
    json:
        {"status": 0}
        
        status: 0 for success, 2001 for class not exist, 5000 for sql exception, 5001 for parameter error

class_comment_list
---
    URL:
        /api/v1.0/class_comment_list?class=&page=
    method:
        get
    parameters:
        class: id of class
        page
    json:
        {"status": 0,
         "class_comments": [{"comment": "", "timestamp": "", "stars": "", "username": ""}]}
        
        status: 0 for success, 2001 for class not exist, 5001 for parameter error
        class_comments: a list of class_comments
            comment
            stars
            timestamp
            username
            
activity_list
---
    URL:
        /api/v1.0/activity_list?organization=&page=
    method:
        get
    parameters:
        organization: id of organization
        page
    json:
        {"status": 0,
         "activities": [{"id": "", "name": "", "age": "", "price": "", "start_time": "", "end_time": ""}]}
        
        status: 0 for success
        activities: a list of activities
            id
            name
            age
            price
            start_time
            end_time

activity_detail
---
    URL:
        /api/v1.0/activity_detail?activity=
    method:
        get
    parameters:
        activity: id of activity
    json:
        {"status": 0,
         "activity": {"id": "", "name": "", "age": "", "price": "", "intro": "", "start_time": "", "end_time": "",
            "comments_count": ""}}
        
        status: 0 for success, 2002 fot activity not exist
        activity: a dict of activity
            id
            name
            age
            price
            intro
            try
            consult_time
            start_time
            end_time
            comments_count

activity_sign_up
---
    URL:
        /api/v1.0/activity_sign_up?class=&username=&name=&cellphone=&age=&sex=&address=&remark=&email=
    method:
        get
    parameters:
        class: id of class
        username
        name
        cellphone
        age
        sex
        address
        remark
        email
    json:
        {"status": 0}
        
        status: 0 for success, 5002 for lack of parameters
    
activity_comment
---
    URL:
        /api/v1.0/activity_comment?activity=&username&comment=&stars=
    method:
        get
    parameters:
        activity: id of activity
        username
        comment
        stars
    json:
        {"status": 0}
        
        status: 0 for success, 2002 for activity not exist, 5000 for sql exception, 5001 for parameter error

activity_comment_list
---
    URL:
        /api/v1.0/activity_comment_list?activity=&page=
    method:
        get
    parameters:
        activity: id of activity
        page
    json:
        {"status": 0,
         "activity_comments": [{"comment": "", "timestamp": "", "stars": "", "username": ""}]}
        
        status: 0 for success, 2002 for activity not exist, 5001 for parameter error
        activity_comments: a list of activity_comments
            comment
            stars
            timestamp
            username
            
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
    
requirement_list
---
    URL:
        /api/v1.0/requirement_list?page=
    method:
        get
    parameters:
        page
    json:
        {"status": 0, "registers": [{"name": "", "cellphone": "", "need": "", "time": ""}]}
        
        status: 0 for success, 5001 for parameter error
        registers: a list of registers
            name
            cellphone
            need
            time

requirement_sign_up
---
    URL:
        /api/v1.0/requirement_sign_up?name=&cellphone=&need=&page=
    method:
        get
    parameters:
        username
        cellphone
        need
        page
    json:
        {"status": 0}
        
        status: 0 for success, 5000 for sql exception 5001 for parameter error
        
get_location_profession
---
    URL:
        /api/v1.0/get_location_profession?city=
    method:
        get
    parameters:
        city
    json:
        {"status": 0, "districts": [""], "professions": [""]}
        
        status: 0 for success, 3000 for city not exist
        districts: a list of districts in city
        professions: a list of professions

CONSTANTS
---
    SUCCESS = 0
    
    LOGIN_FAILED = 1000
    CELLPHONE_NOT_EXIST = 1001
    CELLPHONE_EXIST = 1002
    USER_NOT_EXIST = 1003
    USERNAME_EXIST = 1004
    ACCESS_RESTRICTED = 1005
    ORDER_NOT_EXIST = 1006
    
    ORGANIZATION_NOT_EXIST = 2000
    CLASS_NOT_EXIST = 2001
    ACTIVITY_NOT_EXIST = 2002
    
    CITY_NOT_EXIST = 3000
    PROFESSION_NOT_EXIST = 3001
    
    SQL_EXCEPTION = 5000
    PARAMETER_ERROR = 5001
    LACK_OF_PARAMETER = 5002
    
    PER_PAGE = 10
    EARTH_CIRCUMFERENCE = 40000
    