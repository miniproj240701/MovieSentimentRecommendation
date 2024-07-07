import json
배우 = []
with open('배우리스트.json', encoding='utf-8') as f:
    o = json.load(f)
    for 배우정보 in o['배우']:
        # print(배우정보['이름'])
        배우.append(배우정보['이름'])
print(배우)