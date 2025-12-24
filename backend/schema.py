import graphene
from core.schema import CoreQuery, CoreMutation

class Query(CoreQuery, graphene.ObjectType):
    pass

class Mutation(CoreMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
