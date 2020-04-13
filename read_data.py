import xmltodict
import json

def get_items():
    with open("raw_data/spitems.xml") as fp:
        xml_item = xmltodict.parse(fp.read())["Items"]
    armor = xml_item["Item"]
    weapons = xml_item["CraftedItem"]
    itemd = {}
    for a in armor:
        a["@name"] = a["@name"].split("}")[1]
        try:
            itemd[a["@id"]] = {"text": a["ItemComponent"]["Armor"]["@material_type"], "tip": json.dumps(a)}
        except:
            try:
                itemd[a["@id"]] = {"text": a["ItemComponent"]["Weapon"]["@weapon_class"], "tip": json.dumps(a)}
            except:
                pass
    for w in weapons:
        w["@name"] = w["@name"].split("}")[1]
        try:
            itemd[w["@id"]] = {"text": w["@crafting_template"], "tip": json.dumps(w)}
        except:
            pass
    return itemd


def get_chars():
    with open("raw_data/spnpccharacters.xml") as fp:
        xml_char = xmltodict.parse(fp.read())["NPCCharacters"]["NPCCharacter"]
    chars = []
    for xc in xml_char:
        try:
            if "@occupation" in xc and xc["@occupation"] == "Soldier":
                skills = {}
                if not (isinstance(xc["skills"]["skill"], list) and len(xc["skills"]["skill"]) == 8):
                    continue
                for s in xc["skills"]["skill"]:
                    skills[s["@id"]] = s["@value"]
                equipment = {}
                horse = ""
                harness = ""
                for e in xc["equipmentSet"][0]["equipment"] if isinstance(xc["equipmentSet"], list) else xc["equipmentSet"]["equipment"]:
                    equipment[e["@slot"]] = e["@id"].split(".")[1]
                    if "Horse" == e["@slot"]:

                        horse = e["@id"].split(".")[1]
                    elif "HorseHarness" == e["@slot"]:
                        harness = e["@id"].split(".")[1]
                if "equipment" in xc:
                    for e in xc["equipment"]:
                        if e["@slot"] == "Horse":
                            horse = e["@id"].split(".")[1]
                        elif e["@slot"] == "HorseHarness":
                            harness = e["@id"].split(".")[1]
                chars.append({"id": xc["@id"],
                            "group": xc["@default_group"],
                            "lvl": xc["@level"],
                            "culture": xc["@culture"].split(".")[1],
                            "skills": skills,
                            "equipment": equipment,
                            "horse": horse,
                            "harness": harness
                            })
        except:
            pass
    return chars


itemd = get_items()
chars = get_chars()
rows = []
for c in chars:
    row = {}
    for k in ['id', 'group', 'lvl', 'culture', 'horse', 'harness']:
        row[k] = c[k]
    for k in ['Item0', 'Item1', 'Item2', 'Item3', 'Head', 'Cape', 'Body', 'Gloves', 'Leg']:
        # row[k] = c["equipment"][k] if k in c["equipment"] else ""
        if k in c["equipment"]:
            if c["equipment"][k] in itemd:
                row[k] = itemd[c["equipment"][k]]
            else:
                row[k] = c["equipment"][k]
        else:
            row[k] = ""
    for k in ['Athletics', 'Riding', 'OneHanded', 'TwoHanded', 'Polearm', 'Bow', 'Crossbow', 'Throwing']:
        row[k] = c["skills"][k]
    rows.append(row)
with open("src/data.json", "w") as fp:
    json.dump(rows, fp)
