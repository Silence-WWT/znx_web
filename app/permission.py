# -*- coding: utf-8 -*-
from flask.ext.principal import RoleNeed, Permission, identity_loaded, Denial

user_permission = Permission(RoleNeed('user'))
org_permission = Permission(RoleNeed('org'))
anonymous_permission = Denial(RoleNeed('user'), RoleNeed('org'))


def config_identity(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        if identity.id:
            if u'o' in identity.id:
                identity.provides.add(RoleNeed('org'))

            elif u'u' in identity.id:
                identity.provides.add(RoleNeed('user'))
