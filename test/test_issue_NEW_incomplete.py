from neomodel import StructuredRel, StructuredNode 
from neomodel import RelationshipTo, RelationshipFrom
from neomodel import StringProperty, DateTimeProperty
from py2neo.neo4j import GraphDatabaseService as GDS
from datetime import datetime

gdb = GDS()

def clear_db():
    gdb.clear()


class FridgeRelationship(StructuredRel):
    purchased = DateTimeProperty(default=datetime.now)

class ItemFridgeRelationship(StructuredRel):
    purchased = DateTimeProperty(default=datetime.now)

class Person(StructuredNode):
    name    = StringProperty(unique_index=True)
    fridges = RelationshipTo("Fridge", "owns", model=FridgeRelationship)

class Fridge(StructuredNode):
    name  = StringProperty() 
    owner = RelationshipFrom("Person", "owns", model=FridgeRelationship)
    items = RelationshipTo("Item", "containes", model=ItemFridgeRelationship) 

class Item(StructuredNode):
    name = StringProperty()
    expiry = DateTimeProperty()



def build_dataset():
    jean = Person(name="Jean").save()

    bar        = Fridge(name="Bar").save()
    freezer    = Fridge(name="Deep Freeze").save()
    kitchen    = Fridge(name="Kitchen").save()
    
    jean.fridges.connect(bar)
    jean.fridges.connect(freezer)
    jean.fridges.connect(kitchen)

    beer = Item(name="Beer").save()
    cola = Item(name="Cola").save()
    
    bar.items.connect(beer)
    bar.items.connect(cola)
    
    milk    = Item(name="Milk").save()
    carrots = Item(name="Carrots").save()
    wraps   = Item(name="Wraps").save()
    cheese  = Item(name="Cheese").save()

    kitchen.items.connect(milk)
    kitchen.items.connect(carrots)
    kitchen.items.connect(wraps)
    kitchen.items.connect(cheese)

    steak    = Item(name="Steak").save()
    calamari = Item(name="Calamari").save()
    
    freezer.items.connect(steak)
    freezer.items.connect(calamari)
    
    return jean 

def test_double_traversal():
    jean = None
    for person in Person.category().instance.all():
        if person.name is "Jean":
            jean = person
    #clear_db()
    if not jean:
        print "building dataset"
        jean = build_dataset()
    jean.traverse("fridges").traverse("items").run()







