from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	 url(r'^connector_funf/', include('connectors.connector_funf.urls')),
)
