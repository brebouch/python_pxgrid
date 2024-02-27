#################################################
#                                               #
# Simple Python pxGrid App                      #
#                                               #
# Author: Brennan Bouchard                      #
#                                               #
#################################################

import sys
import session

search_ip = sys.argv[0]
if search_ip:
    session_by_ip = session.by_ip(search_ip)
all_sessions = session.all()

