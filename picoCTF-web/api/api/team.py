__author__ = 'collinpetty'

from api.annotations import *
from api import app, common
import api.user

def get_team(tid=None, team_name=None):
    db = common.get_conn()
    if tid is not None:
        return db.teams.find_one({'tid': tid})
    elif team_name is not None:
        return db.teams.find_one({'team_name': team_name})
    return None


def create_team(team_name, adviser_name, adviser_email, school, password):
    db = common.get_conn()
    tid = common.token()
    try:
        db.teams.insert({'tid': tid,
                         'team_name': team_name,
                         'adviser_name': adviser_name,
                         'adviser_email': adviser_email,
                         'school': school,
                         'password': password})  # JB: Currently, group passwords are plaintext. We should think
                                                 # whether we should hash them or if we need to display them
    except Exception as e:
        print("Error creating the team account.")
        return None
    return tid


def get_teammate_uids(tid):
    db = common.get_conn()
    return [t['uid'] for t in db.users.find({'tid': tid})]


@app.route('/api/team', methods=['GET'])
@return_json
@require_login
def team_information():
    db = common.get_conn()
    useracct = api.user.get_user()
    uid = useracct['uid']
    tid = useracct['tid']
    team_cur = db.teams.find_one({'tid': tid})

    teammates = []
    for u in get_teammate_uids(tid):
        teammate = db.users.find_one({'uid': u})
        teammates.append({'teammate': teammate['username'], 'is_you': teammate['uid'] == uid})

    team_data = {'team_name': team_cur['team_name'], 'password': team_cur['password'],
                 'adviser_name': team_cur['adviser_name'], 'adviser_email': team_cur['adviser_email'],
                 'school': team_cur['school'],
                 'teammates': teammates}
    return 1, team_data