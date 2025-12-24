import graphene
from core.schema import CoreQuery

class Query(CoreQuery, graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
