import time

from app import db

from app.models import *


def get_ages(obj):
    if isinstance(obj, Organization):
        query = OrganizationAge.query.filter_by(organization_id=obj.id).all()
    elif isinstance(obj, Class):
        query = ClassAge.query.filter_by(class_id=obj.id).all()
    elif isinstance(obj, Activity):
        query = ActivityAge.query.filter_by(activity_id=obj.id).all()
    else:
        query = []
    age_list = []
    for item in query:
        age = Age.query.get(item.age_id)
        age_list.append(age.age)
    return age_list


def get_professions(obj):
    profession_list = []
    if isinstance(obj, Organization):
        query = OrganizationProfession.query.filter_by(organization_id=obj.id)
        for item in query:
            profession = Profession.query.get(item.profession_id)
            profession_list.append(profession.profession)
    return profession_list


def get_unified(user_id, mobile_key):
    unified = UnifiedId.query.filter_by(user_id=user_id, mobile_key=mobile_key).first()
    if not unified:
        unified = UnifiedId(
            user_id=user_id,
            mobile_uuid=mobile_key,
            web_uuid='',
            created=time.time()
        )
        db.session.add(unified)
        db.session.commit()
    return unified