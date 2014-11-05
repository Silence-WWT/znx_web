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
    for age_id in query:
        age = Age.query.get(age_id)
        age_list.append(age.age)
    return age_list


def get_professions(obj):
    profession_list = []
    if isinstance(obj, Organization):
        query = OrganizationProfession.query.filter_by(organization_id=obj.id)
        for profession_id in query:
            profession = Profession.query.get(profession_id)
            profession_list.append(profession.profession)
    return profession_list