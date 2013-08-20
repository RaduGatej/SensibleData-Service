from django.conf.urls import patterns, include, url

urlpatterns = patterns('connectors.connector_raw',
         url(r'^v1/location/', 'location.location'),
         url(r'^v1/bluetooth/', 'bluetooth.bluetooth'),
         url(r'^v1/questionnaire/', 'questionnaire.questionnaire'),

         url(r'^v1/auth/grant/', 'auth.grant'),
         url(r'^v1/auth/token/', 'auth.token'),
         url(r'^v1/auth/refresh_token/', 'auth.refresh_token'),
         url(r'^v1/auth/grant_mobile/', 'auth.grant_mobile'),
         url(r'^v1/auth/token_mobile/', 'auth.token_mobile'),
         url(r'^v1/auth/refresh_token_mobile/', 'auth.refresh_token_mobile'),
         url(r'^v1/auth/granted_mobile/', 'auth.granted_mobile'),
         url(r'^v1/auth/gcm/', 'auth.gcm'),



#         url(r'^auth/revoke/', 'auth.revoke'),
#         url(r'^auth/sync/', 'auth.sync'),
)