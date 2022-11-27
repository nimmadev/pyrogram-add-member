import os
import json
import logging
from helper.pam_log import pamlog
def filterus(p1,p2,p4, root_path):
    # create logger
    PAM = pamlog('PAM-Filter-User')
    p3 = root_path / "data" / "user.json"
    if os.path.isfile(p1):
        PAM.info('starting filter user')
        try: 
            with open(p1, encoding='utf-8') as f:
                json11 = json.loads(f.read())
            with open(p2, encoding='utf-8') as b:
                json22 = json.loads(b.read())

            garbage_id = {d['userid'] for d in json22}
            json1 = [item for item in json11 if item['userid'] not in garbage_id]
            with open(p3, 'w', encoding='utf-8') as file:
                json.dump(json1, file, ensure_ascii=False, indent=4)
            PAM.info("Filter process done")
        except:
            PAM.info("failed to make filter json")
    #path_group3 = 'data/user.json'
    if os.path.isfile(p3):
        try:
            with open(p3) as c:
                json33 = json.loads(c.read())
            with open(p4) as h:
                json44 = json.loads(h.read())
            garbage_i = {d['userid'] for d in json44}
            json2 = [item for item in json33 if item['userid'] not in garbage_i]
            with open(p3, "w", encoding='utf-8') as f:
                json.dump(json2, f, ensure_ascii=False, indent=4)
        except:
            PAM.info("no admin in group")
        #disconect
