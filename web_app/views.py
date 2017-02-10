from web_app.models import AuthToken
from web_app import admin

from flask_admin.contrib.mongoengine import ModelView
from flask_admin.actions import action


class AuthTokenView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.api_key = str(model.api_key).strip()




        # @action('start', 'Start', 'Are you sure you want to start?')
        # def action_start(self, ids):
        #     for id in ids:
        #         job = Job.objects.get(pk=id)
        #         if not job.started:
        #             job.start()


# TODO default auth_token uuid

# admin.add_view(ModelView(AuthToken, name='AuthTokens'))
admin.add_view(AuthTokenView(AuthToken, name='AuthTokens'))
