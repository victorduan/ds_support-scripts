# encoding: utf-8

import sys, os
import datasift

class Env(object):
    """
    Sets up and provides access to the environment for the Historics examples.
    """
    _user = None
    _args = []

    def __init__(self, user, api_key):
        """
        Initialise the environment with the provided arguments.
        """

        self._user = datasift.User(user, api_key)

    def get_user(self):
        return self._user

    def display_subscription_details(self, sub):
        print 'ID:           ', sub.get_id()
        print 'Name:         ', sub.get_name()
        print 'Status:       ', sub.get_status()
        print 'Created at:   ', sub.get_created_at()
        print 'Last request: ', sub.get_last_request()
        print 'Last success: ', sub.get_last_success()
        print 'Output type:  ', sub.get_output_type();

        print 'Output Params:'
        output_params = sub.get_output_params()
        for key in output_params:
            print '  %s = %s' % (key, output_params[key])

    def display_historic_details(self, historic):
        print 'Playback ID:  ', historic.get_hash()
        print 'Stream hash:  ', historic.get_stream_hash()
        print 'Name:         ', historic.get_name()
        print 'Start time:   ', historic.get_start_date()
        print 'End time:     ', historic.get_end_date()
        print 'Sources:      ', historic.get_sources();
        print 'Created at:   ', historic.get_created_at()
        print 'Status:       ', historic.get_status()
        print 'Progress:     ', '%d%%' % (historic.get_progress())
