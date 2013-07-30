import sys
import os
import shutil
import fnmatch
from dbdecrypt import decrypt_if_not_db_file
from decrypt import key_from_password
from utils import SECURE_settings
from utils import log, fail
from django.conf import settings
from connectors.connector_funf.models import ConnectorFunf 

#import pdb

mConnector = ConnectorFunf.objects.all()[0];

key = key_from_password(SECURE_settings.CONNECTORS['connector_funf']['db_pass']);

def decrypt():
	decrypt_directory()

def decrypt_directory(directory_to_decrypt=mConnector.upload_path):
	decrypted_directory_path = mConnector.decrypted_path
	decryption_failed_path = mConnector.decryption_failed_path;
	backup_path = mConnector.backup_path;
	
	''' 
	NEW VERSION: moves a file, decrypts it, moves on to the next file
	'''
	raw_filenames = [filename for filename in os.listdir(directory_to_decrypt) if fnmatch.fnmatch(filename, '*.db')]
	found_files = len(raw_filenames);
	print 'Found ' + str(len(raw_filenames)) + ' files in the folder'
	#filenames = [os.path.join(directory_to_decrypt, filename) for filename in raw_filenames]
	proc_dir = os.path.join(directory_to_decrypt, 'processing')
	if not os.path.exists(proc_dir):
		os.mkdir(proc_dir)
	failed_filenames = []
	
	already_moved_counter = 0;
	success_counter = 0;
	
	for f in raw_filenames:
		upload_filename = os.path.join(directory_to_decrypt, f)
		proc_filename = os.path.join(proc_dir, f)
		decrypted_filename = os.path.join(decrypted_directory_path, f)
		curr_filename = upload_filename #for keeping track of the file's current location
		decryption_success = False;
		try:
			# check if still exists, might have been moved in another thread
			if os.path.exists(upload_filename) and not os.path.exists(proc_filename):
				# move it to processing
				shutil.move(upload_filename, proc_dir)
				curr_filename = proc_filename
				# decrypt
				if decrypt_if_not_db_file(proc_filename, key, extension=None):
					decryption_success = True;
					fail.safe_move(proc_filename, decrypted_directory_path)
					curr_filename = decrypted_filename
					orig_filename = proc_filename + '.orig'
					if os.path.exists(orig_filename):
						os.remove(orig_filename)
					success_counter +=1;
			else:
				already_moved_counter +=1;
		except Exception as e:
			#find out when it happened
			action = '';
			if curr_filename == upload_filename:
				action = 'moving to /processing'
			elif curr_filename == proc_filename and decryption_success == False:
				action = 'decrypting'
			elif curr_filename == proc_filename and decryption_success == True:
				action = 'moving to /decrypted'
			elif curr_filename == decrypted_filename:
				action = 'removing the .orig file of'
			try:
				if not str(e).contains('already exists'):
					fail.fail(curr_filename, decryption_failed_path, 'Exception thrown: ' + str(e) + '. While ' + action + ' file: ' + f)
					log.log('error', 'README ^^^^^^^^^^^^^')
				else:
					log.log('error','Exception thrown: ' + str(e) + '. While ' + action + ' file: ' + f);
				
			except Exception as e1:
				pass
			failed_filenames.append(os.path.basename(f))
	
	print str(already_moved_counter) + ' of them were already moved when I tried to decrypt them'
	print 'I encrypted ' + str(success_counter) + ' files, which means the Devil took ' + str(found_files - already_moved_counter - success_counter) + ' of all files'
	
	'''
	#OLD VERSION: first moves all files to upload/processing, then decrypts the whole processing dir
	#TODO
	raw_filenames = [filename for filename in os.listdir(directory_to_decrypt) if fnmatch.fnmatch(filename, '*.db')]
	#raw_filenames = [filename for filename in os.listdir(directory_to_decrypt) if fnmatch.fnmatch(filename, '*.orig')]
	filenames = [os.path.join(directory_to_decrypt, filename) for filename in raw_filenames]
	proc_dir = os.path.join(directory_to_decrypt, 'processing')
	if not os.path.exists(proc_dir):
		os.mkdir(proc_dir)
	failed_filenames = []
	
	for f in filenames:
		try:
			shutil.move(f, proc_dir)
		except Exception as e:
			fail.fail(f, decryption_failed_path, 'Exception thrown: ' + str(e) + '. While moving file: ' + f)
			failed_filenames.append(os.path.basename(f))

	raw_filenames = [e for e in raw_filenames if e not in failed_filenames]
	filenames = [os.path.join(proc_dir, filename) for filename in raw_filenames]


	for filename in filenames:
		try:
			# If successfull we move the decrypted file to the decrypted directory
			#pdb.set_trace();
			if decrypt_if_not_db_file(filename, key, extension=None):
				fail.safe_move(filename, decrypted_directory_path)
				
				# Move original db file to original directory if it exists -- if db file is already decrypted .orig will not exist
				orig_filename = filename + '.orig'
				#orig_filename = filename
				#pdb.set_trace()
				if os.path.exists(orig_filename):
					os.remove(orig_filename)

			# If decryption fails we move the file to the failed directory
			else:
				fail.fail(filename, decryption_failed_path, 'Could not decrypt file: ' + filename)
		except Exception as e:
			# If anything goes wrong we move the file to the failed directory
			fail.fail(filename, decryption_failed_path, 'Exception thrown: ' + str(e) + '. While decrypting file: ' + filename)
			
	'''


if __name__ == '__main__':
	if len(sys.argv) == 2:
		directory = sys.argv[1]
		decrypt_directory(directory_to_decrypt=directory)
	else:
		decrypt_directory()
