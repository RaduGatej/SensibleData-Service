from utils.log import log
from connectors import connectors_config
from connectors.connector_funf.models import *
from connectors.connector_questionnaire.models import *
from connectors.models import *
import json
from django.conf import settings
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		for connector in connectors_config.CONNECTORS:
			try:
				if not settings.CONNECTORS[connector]: continue
			except KeyError: continue

			if connector == 'ConnectorFunf': self.populateConnectorFunf(connectors_config.CONNECTORS[connector])
			if connector == 'ConnectorQuestionnaire': self.populateConnectorQuestionnaire(connectors_config.CONNECTORS[connector])

	def populateConnectorFunf(self, data):
		connector = ConnectorFunf.objects.create(name=data['name'],
							description=data['description'],
							upload_path=data['config']['upload_path'],
							upload_not_authorized_path=data['config']['upload_not_authorized_path'],
							decrypted_path=data['config']['decrypted_path'],
							decryption_failed_path=data['config']['decryption_failed_path'],
							load_failed_path=data['config']['load_failed_path'],
							config_path=data['config']['config_path'],
							backup_path=data['config']['backup_path'],
							connector_type=data['config']['connector_type'],
							max_population_processes=data['config']['max_population_processes'],
							max_population_files=data['config']['max_population_files'],
							grant_url=data['config']['grant_url'],
							revoke_url=data['config']['revoke_url'],
							)

		for scope in data['scopes']:
			Scope.objects.create(connector=connector, scope=data['name']+'.'+scope, description=data['scopes'][scope]['description'])


		print 'created funf connector: '+json.dumps(data)
	


	def populateConnectorQuestionnaire(self, data):
		connector = ConnectorQuestionnaire.objects.create(name=data['name'],
							description=data['description'],
							connector_type=data['config']['connector_type'],
							grant_url=data['config']['grant_url'],
							revoke_url=data['config']['revoke_url'],
							)

		for scope in data['scopes']:
			Scope.objects.create(connector=connector, scope=data['name']+'.'+scope, description=data['scopes'][scope]['description'])


		print 'created questionnaire connector: '+json.dumps(data)
