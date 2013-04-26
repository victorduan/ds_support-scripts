# encoding: utf-8

import sys, os
from datetime import datetime
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), "..", ".."),]
import datasift
import csv
from env import Env

def usage(message = '', exit = True):
	"""
	Display usage information, with an error message if provided.
	"""
	if len(message) > 0:
		sys.stderr.write('\n%s\n' % message)
		sys.stderr.write('\n');
		sys.stderr.write('Usage: bulk-historic-load-from-csv.py <username> <api_key> \\\n')
		sys.stderr.write('			</path/to/csvfile> <output_type> <output_params>\n')
		sys.stderr.write('\n')
		sys.stderr.write('Where: 	path/to/csvfile = the absolute path to the CSV file (with headers "Name", "Hash", "Start", "End", "Sources")\n')
		sys.stderr.write('	output_type 	= endpoint connector type"\n')
		sys.stderr.write('	output_params	= output_type specific parameters \n')
		sys.stderr.write('\n')
		sys.stderr.write('Example: ')
		sys.stderr.write('bulk-historic-load-from-csv.py <username> <api_key> \\\n')
		sys.stderr.write('		/path/to/some.csv s3 delivery_frequency=0 max_size=10485760	\\\n')
		sys.stderr.write('		bucket=<bucketname> directory=<directory>	\\\n')
		sys.stderr.write('		acl=private file_prefix=Datasift	\\\n')
		sys.stderr.write('		auth.access_key=<accesskey> auth.secret_key=<secretkey>	\n')
		sys.stderr.write('\n')
	if exit:
		sys.exit(1)

# Set up the environment
env = Env(sys.argv)

# Make sure we have enough arguments
if env.get_arg_count() < 3:
    usage("Not enough arguments")

fieldNames = ["Name", "Hash", "Start", "End", "Sources"]

fn = env.get_arg(0)

f = open(fn, 'rU')

historics_jobs = csv.DictReader(f, fieldNames)

# Skip the header row
next(historics_jobs)

for parameters in historics_jobs:
	print parameters
	# Get the args
	stream_hash = parameters['Hash'].strip()
	start 		= parameters['Start'].strip()
	end 		= parameters['End'].strip()
	sources 	= parameters['Sources'].strip()
	sample 		= "100"
	name 		= parameters['Name'].strip()
	output_type = env.get_arg(1)

	try:
		# Create the historics job
		historic = env.get_user().create_historic(stream_hash, start, end, sources.split(','), sample, name)

		sys.stderr.write('Historic playback ID: {0}\n'.format(historic.get_hash()))

		env.display_historic_details(historic)

		# Create the Push definition
		pushdef = env.get_user().create_push_definition()
		pushdef.set_output_type(output_type)

		# Now add the output_type-specific args from the command line
		for arg in env.get_args()[2:]:
			key, val = arg.split('=')
			pushdef.set_output_param(key, val)

		# Subscribe the historic to the hash
		sub = pushdef.subscribe_historic(historic, name)

		# Start the Historics query
		historic.start()

		print 'Push subscription:'
		env.display_subscription_details(sub)

	except datasift.InvalidDataError, e:
		sys.stderr.write('InvalidDataError: %s\n' % e)
	except datasift.AccessDeniedError, e:
		sys.stderr.write('InvalidDataError: %s\n' % e)
	except datasift.APIError, e:
		sys.stderr.write('APIError: %s\n' % e)

sys.stderr.write('Rate-limit-remaining: %s\n' % str(env.get_user().get_rate_limit_remaining()));

f.close()