from web_app.models import AuthToken, User
from web_app import admin

from flask_admin.contrib.mongoengine import ModelView
from flask_admin.actions import action
from flask import flash, redirect, Response

from web_app import basic_auth


class AuthTokenView(ModelView):
    can_export = True

    def on_model_change(self, form, model, is_created):
        model.api_key = str(model.api_key).strip()

    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


        # @action('start', 'Start', 'Are you sure you want to start?')
        # def action_start(self, ids):
        #     for id in ids:
        #         job = Job.objects.get(pk=id)
        #         if not job.started:
        #             job.start()


class UserView(ModelView):
    can_export = True

    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

    # TODO add action to delete user from LDAP
    @action('add_to_ldap', 'Add To LDAP', 'Are you sure you want add these users?')
    def action_add_to_ldap(self, user_pks):
        from helper.tasks import add_user, make_data_dirs, email_user
        for user_pk in user_pks:
            user_object = User.objects(pk=user_pk).first()
            if user_object is not None:
                real_username, uid_number, pwd = add_user(user_object.full_name, user_object.username,
                                                          user_object.email,
                                                          pk=user_pk)
                make_data_dirs(real_username, uid_number)
                user_object.has_ldap_account = True
                user_object.save()

                email_user(real_username, pwd, user_object.email, user_object.full_name)

                flash("( {0}, {1}, {2}, {3} )has been added successfully!".format(user_object.full_name, real_username,
                                                                                  uid_number, pwd
                                                                                  ))

    @action('email_user_creds', 'Email User Creds', 'Are you sure you want to send them ANOTHER email?')
    def action_email_user_creds(self, user_pks):
        from helper.tasks import email_user
        for user_pk in user_pks:
            user_object = User.objects(pk=user_pk).first()
            if user_object is not None:
                email_user(user_object.username, user_object.password, user_object.email, user_object.full_name)

                flash("( {0}, {1}, {2}, {3} )has been added successfully!".format(user_object.full_name,
                                                                                  user_object.username,
                                                                                  user_object.uid_number,
                                                                                  user_object.password
                                                                                  ))
    @action('delete_from_ldap', 'Delete from LDAP', 'Are you sure you want to delete these users?')
    def action_delete_to_ldap(self, user_pks):
        from helper.tasks import delete_user
        for user_pk in user_pks:
            user_object = User.objects(pk=user_pk).first()
            if user_object is not None:
                ok = delete_user(user_object.username) 
                
                user_object.has_ldap_account = False
                user_object.uid_number = None
                user_object.password = None
                user_object.save()
               
                if ok:

                    flash("{0} has been deleted successfully!".format(user_object.username))
                else:
                    flash("{0} was not found on LDAP database.".format(user_object.username, "error"))


    @action('delete', 'Delete from LDAP/Storage', 'Are you sure you want to purge these users?')
    def action_delete(self, user_pks):
        from helper.tasks import delete_user, delete_user_dirs
        import inspect
        for user_pk in user_pks:
            user_object = User.objects(pk=user_pk).first()
            if user_object is not None:
                _ = delete_user(user_object.username) 
                delete_user_dirs(user_object.username)
                user_object.delete()
                flash("{0} has been purged successfully!".format(user_object.username))



# TODO default auth_token uuid

# admin.add_view(ModelView(AuthToken, name='AuthTokens'))
admin.add_view(AuthTokenView(AuthToken, name='AuthTokens'))
admin.add_view(UserView(User, name='Users'))

from werkzeug.exceptions import HTTPException


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))
