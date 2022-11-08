def filterus(p1,p2,p4, root_path):
        p3 = root_path / "data" / "user.json"
        if os.path.isfile(p1):
            print('starting filter user')
            try: 
                with open(p1) as f:
                    json11 = json.loads(f.read())
                with open(p2) as b:
                    json22 = json.loads(b.read())

                for x in json22:
                    if x in json11:
                        json11.remove(x)
                with open(p3, 'w', encoding='utf-8') as file:
                    json.dump(json11, file, ensure_ascii=False, indent=4)
                print("Filter process done")
            except:
                print("failed to make filter json")
        #path_group3 = 'data/user.json'
        if os.path.isfile(p3):
            try:
                with open(p3) as c:
                    json33 = json.loads(c.read())
                with open(p4) as h:
                    json44 = json.loads(h.read())
                for x in json44:
                    if x in json33:
                        json33.remove(x)
                with open(p3, "w", encoding='utf-8') as f:
                    json.dump(json33, f, ensure_ascii=False, indent=4)
            except:
                print("no admin in group")
            #disconect
