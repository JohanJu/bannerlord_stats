import xmltodict
import json

def get_items():
    with open("raw_data/spitems.xml") as fp:
        xml_item = xmltodict.parse(fp.read())["Items"]
    item = xml_item["Item"]
    crafted = xml_item["CraftedItem"]
    itemd = {}
    for a in item:
        a["@name"] = a["@name"].split("}")[1]
        try:
            itemd[a["@id"]] = {"text": a["ItemComponent"]["Armor"]["@material_type"], "tip": json.dumps(a)}
        except:
            try:
                itemd[a["@id"]] = {"text": a["ItemComponent"]["Weapon"]["@weapon_class"], "tip": json.dumps(a)}
            except:
                try:
                    if "Horse" in a["ItemComponent"]:
                        itemd[a["@id"]] = {"text": a["@name"], "tip": json.dumps(a)}
                except:
                    pass
    for w in crafted:
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
                equipment["horse"] = horse
                equipment["harness"] = harness
                chars.append({"id": xc["@id"],
                            "group": xc["@default_group"],
                            "lvl": xc["@level"],
                            "culture": xc["@culture"].split(".")[1],
                            "skills": skills,
                            "equipment": equipment,
                            })
        except:
            pass
    return chars


itemd = get_items()
chars = get_chars()
rows = []
for c in chars:
    row = {}
    for k in ['id', 'group', 'lvl', 'culture']:
        row[k] = c[k]
    for k in ['Item0', 'Item1', 'Item2', 'Item3', 'Head', 'Cape', 'Body', 'Gloves', 'Leg', 'horse', 'harness']:
        # row[k] = c["equipment"][k] if k in c["equipment"] else ""
        if k in c["equipment"]:
            if c["equipment"][k] in itemd:
                row[k] = itemd[c["equipment"][k]]
            else:
                row[k] = c["equipment"][k]
        else:
            row[k] = ""
    armor = {"head": 0, "body": 0, "arm": 0, "leg": 0}
    for k in ['Head', 'Cape', 'Body', 'Gloves', 'Leg']:
        if k in c["equipment"]:
            if c["equipment"][k] in itemd:
                a = json.loads(itemd[c["equipment"][k]]["tip"])["ItemComponent"]["Armor"]
                for aa in armor:
                    if f"@{aa}_armor" in a:
                        armor[aa] += int(a[f"@{aa}_armor"])
    for a in armor:
        row[a] = str(armor[a])
    for k in ['Athletics', 'Riding', 'OneHanded', 'TwoHanded', 'Polearm', 'Bow', 'Crossbow', 'Throwing']:
        row[k] = c["skills"][k]
    rows.append(row)
with open("src/data.json", "w") as fp:
    json.dump(rows, fp)
