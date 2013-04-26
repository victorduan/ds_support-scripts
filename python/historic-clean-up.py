# encoding: utf-8

# This example lists the current Historics queries in your account.

import sys, os
from datetime import datetime, timedelta
import time
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), "..", ".."),]
import datasift
from env import Env

# Set up the environment
env = Env(sys.argv)

try:
    pageSize = 20
    pageNum = 1
    runLoop = True

    while runLoop:
        # Get the list of Historics queries in your account
        queries = env.get_user().list_historics(pageNum, pageSize)
        pageNum += 1

        if len(queries['historics']) == 0:
            print "No Historics Found"
            runLoop = False
            break

        for historic in queries['historics']:
            if historic.get_status() == "init":
                historic.delete()
                print "Deleting Playback ID: {0}, Status: {1}".format(historic.get_hash(), historic.get_status())
            elif historic.get_status() == "succeeded":
                #print historic.get_created_at()
                histJob = datetime.fromtimestamp(int(historic.get_created_at()))
                refDate = datetime.now() - timedelta(days=14)

                if refDate > histJob:
                    # Delete the historic job if it is in success state for over 2 weeks
                    print "Deleting Playback ID: {0}, Status: {1}".format(historic.get_hash(), historic.get_status())
                    historic.delete()
                    time.sleep(0.5)

except datasift.InvalidDataError, e:
    sys.stderr.write('InvalidDataError: %s\n' % e)
except datasift.APIError, e:
    sys.stderr.write('APIError: %s\n' % e)
except datasift.AccessDeniedError, e:
    sys.stderr.write('InvalidDataError: %s\n' % e)

sys.stderr.write('Rate-limit-remaining: %s\n' % str(env.get_user().get_rate_limit_remaining()));
