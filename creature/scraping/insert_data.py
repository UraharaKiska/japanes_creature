from creature.models import *
import json

def json_load():
    with open("creature/scraping/data/yokais.json") as f:
        data = json.load(f)
    for d in data:
        try:
            write = Creature(title=d['title'],
                             slug=d['slug'],
                             content=d['content'],
                             photo=['17'],
                             cat=Category.objects.get(pk=2)
                             )
            write.save()
        except Exception as ex:
            print(ex)
        break

f = open("creature/scraping/data/yokais.json")
data = json.load(f)
for d in data:
    data = d
    try:
        write = Creature(title=data['title'],
                       slug=data['slug'],
                       content=data['content'],
                       photo=data['img'],
                       cat=Category.objects.get(pk=2)
                       )
        write.save()
    except Exception as ex:
        print(ex)



