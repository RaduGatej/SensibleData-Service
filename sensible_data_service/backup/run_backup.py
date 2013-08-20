from django.conf import settings
import datetime
import time
import os
import shutil
from utils import SECURE_settings

def run_backup():
	current_folder = buildHourlyFolder(hours_delta = 0, days_delta = 1)
	BACKUP_DIR = settings.DATA_BACKUP_DIR
	print 'running backup'
	print BACKUP_DIR
	print current_folder

	for hourly_folder in os.listdir(BACKUP_DIR):
		if not hourly_folder < current_folder: continue
		if 'tar.gz' in hourly_folder: continue
		print 'to back up: ', hourly_folder
		folder_name = os.path.join(BACKUP_DIR, hourly_folder)
		archive_name = folder_name+'.tar.gz'
		archive_name_encrypted = archive_name+'.enc'
		command = 'tar cfz %s %s'%(archive_name, folder_name)
		command_encrypt = 'openssl aes-256-cbc -a -k %s -in %s -out %s'%(SECURE_settings.BACKUP_ENCRYPTION_KEY, archive_name, archive_name_encrypted)
		os.system(command)
		os.system(command_encrypt)

		clean(folder_name, archive_name)
		clean(archive_name, archive_name_encrypted)


	return True

def recover(filename):
	if '.enc' in filename:
		try:
			command_decrypt = 'openssl aes-256-cbc -d -a -k %s -in %s -out %s'%(SECURE_settings.BACKUP_ENCRYPTION_KEY, filename, filename.split('.enc')[0])
			os.system(command_decrypt)
		except: pass
		try:
			if not '.tar.gz' in filename: return False
			command_untar = 'tar xvf %s -C %s'%(filename.split('.enc')[0], os.path.dirname(filename))
			os.system(command_untar)
		except: return False

def recover_all(directory):
	for filename in os.listdir(directory):
		if 'enc' in filename:
			f = os.path.join(directory, filename)
			recover(f)

def clean(filename, required_next_file = ''):
	if not os.path.exists(filename): return False
	if not os.path.exists(required_next_file): return False
	try:
		os.remove(filename)
		return True
	except OSError:
		try:
			shutil.rmtree(filename)
			return True
		except: return False
	except: return False

def buildHourlyFolder(hours_delta = 0, days_delta = 0):
	now = datetime.datetime.now() - datetime.timedelta(hours=hours_delta, days=days_delta)
	folder = ''
	folder += '%s_'%now.year
	folder += '%s_'%str(now.month).zfill(2)
	folder += '%s_'%str(now.day).zfill(2)
	folder += '%s'%str(now.hour).zfill(2)
	return folder