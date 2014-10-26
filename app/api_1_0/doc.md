Android API
====

register
----
    URL:
        /api/v1.0/register?&password=&mobile=&identity=&email=
    method:
        get
    parameters:
        password
        mobile
        email
        identity: mobile + uuid + 0
    json:
        {"status": 0, "user": {"username": "", "mobile": "", "identity": "", "email": ""}}
        
        status: 0 for success, 1002 for existing mobile, 1004 for existing username, 5000 for SQL exception
        username
        mobile
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
        identity: mobile + uuid + 0
    json:
        {"status": 0,
         "user": {"username": "", "mobile": "", "email": "", "identity": ""}}
             
        status: 0 for success, 1000 for login failed
        username: if login fail, username, mobile, email, identity won't return
        mobile
        email
        identity
        
organization_filter
---
    URL:
        /api/v1.0/organization_filter?city=&district=&page=
        /api/v1.0/organization_filter?city=&profession=&page=  
        /api/v1.0/organization_filter?distance=&latitude=&longitude=&page=
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
         "organization": {"id": "", "name": "", "city": "", "district": "", "photo": "", "logo": "", "intro": "",
            "address": "", "mobile": "", "comments_count": "", "stars": "", "traffic": ""}}
         
        status: 0 for success, 2000 for organization not exist
        organization
            id
            name
            city
            district
            photo: url of photo
            logo: url of logo
            intro
            address
            mobile
            comments_count
            stars: a float number for stars
            traffic
    
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
         "organization_comments": [{"comment": "", "created": "", "stars": "", "username": ""}]}
        
        status: 0 for success, 2000 for organization not exist, 5001 for parameter error
        organization_comments: a list of organization_comments
            comment
            stars
            created
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
         "classes": [{"id": "", "name": "", "age": "", "price": "", "days": ""}]}
        
        status: 0 for success
        classes: a list of classes
            id
            name
            age
            price
            days
    
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
         "class": {"id": "", "name": "", "age": "", "price": "", "intro": "", "is_tastable": "", "consult_time": "",
            "comments_count": "", "days": ""}}
        
        status: 0 for success, 2001 for class not exist
        class: a dict of class
            id
            name
            age
            price
            intro
            is_tastable
            consult_time
            start_time
            end_time
            comments_count
            days
    
class_sign_up
---
    URL:
        /api/v1.0/class_sign_up?class=&username=&name=&mobile=&age=&sex=&address=&remark=&email=&time=
    method:
        get
    parameters:
        class: id of class
        username
        name
        mobile
        age
        sex
        address
        remark
        email
        time: seconds since 1970
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
         "class_comments": [{"comment": "", "created": "", "stars": "", "username": ""}]}
        
        status: 0 for success, 2001 for class not exist, 5001 for parameter error
        class_comments: a list of class_comments
            comment
            stars
            created
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
            is_tastable
            consult_time
            start_time
            end_time
            comments_count

activity_sign_up
---
    URL:
        /api/v1.0/activity_sign_up?class=&username=&name=&mobile=&age=&sex=&address=&remark=&email=
    method:
        get
    parameters:
        class: id of class
        username
        name
        mobile
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
         "activity_comments": [{"comment": "", "created": "", "stars": "", "username": ""}]}
        
        status: 0 for success, 2002 for activity not exist, 5001 for parameter error
        activity_comments: a list of activity_comments
            comment
            stars
            created
            username
            
order_list
---
    URL:
        /api/v1.0/order_list?username=&mobile=&page=
    method:
        get
    parameters:
        username
        mobile
        page
    json:
        {"status": 0,
         "orders": [{"class_order_id": "", "created": "", "class_name": "", "org_name": ""},
            {"activity_order_id": "", "created": "", "activity_name", "", "org_name": ""}]}
         
         status: 0 for success, 1003 for user not exist
         class_order_id/activity_order_id
         class_name/activity_name
         created
         org_name
         
class_order_detail
---
    URL:
        /api/v1.0/order_list?username=&mobile=&class_order=
    method:
        get
    parameters:
        username
        mobile
        class_order
    json:
        {"status": 0,
         "class": [{"time": "", "created": "", "class_name": "", "org_name": "", "name": "", "age": "", "sex": "",
             "mobile": "", "address": "", "remark": ""}]}
         
        status: 0 for success, 1003 for user not exist, 1005 for access restricted, 1006 for order not exist
        activity
            created: created time of this order
            time: the taste time of class
            class_name
            name: user's name
            age
            sex
            mobile
            email
            address: user's address
            remark: user's remark of this class
    
activity_order_detail
---
    URL:
        /api/v1.0/order_list?username=&mobile=&activity_order=
    method:
        get
    parameters:
        username
        mobile
        activity_order
    json:
        {"status": 0,
         "activity": [{"created": "", "activity_name": "", "org_name": "", "name": "", "age": "", "sex": "",
             "mobile": "", "email": "", "address": "", "remark": ""}]}
         
        status: 0 for success, 1003 for user not exist, 1005 for access restricted, 1006 for order not exist
        activity
            created: created time of this order
            activity_name
            name: user's name
            age
            sex
            mobile
            email
            address: user's address
            remark: user's remark of this activity
    
requirement_list
---
    URL:
        /api/v1.0/requirement_list?page=
    method:
        get
    parameters:
        page
    json:
        {"status": 0, "registers": [{"name": "", "mobile": "", "need": "", "time": ""}]}
        
        status: 0 for success, 5001 for parameter error
        registers: a list of registers
            name
            mobile
            need
            time

requirement_sign_up
---
    URL:
        /api/v1.0/requirement_sign_up?name=&mobile=&need=&city=&district=
    method:
        get
    parameters:
        username
        mobile
        need
        city
        district
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
    