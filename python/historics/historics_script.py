# encoding: utf-8

import sys, os
import time
import calendar
import datasift
import config
from env import Env

# Set up the environment (initialize with username/api_key)
env = Env(config.username, config.api_key)

# Parameters
stream_hash = config.stream_hash
start_date	= config.start_date
end_date 	= config.end_date
sources 	= config.sources
sample 		= config.sample
name 		= config.name
# FTP
output_type = config.output_type
output_params = config.output_params

try:
	# Parse the dates from the command line
	in_format  	= '%Y-%m-%d %H:%M:%S'
	start_date	= time.strptime(start_date, in_format)
	end_date 	= time.strptime(end_date,   in_format)

	start 		= calendar.timegm(start_date)
	end			= calendar.timegm(end_date)

	# Create the historics job
	historic = env.get_user().create_historic(stream_hash, start, end, sources.split(','), sample, name)

	sys.stderr.write('Historic playback ID: {0}\n'.format(historic.get_hash()))

	env.display_historic_details(historic)

	# Create the Push definition
	pushdef = env.get_user().create_push_definition()
	pushdef.set_output_type(output_type)

	# Now add the output_type-specific args
	for key,val in output_params.items():
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
