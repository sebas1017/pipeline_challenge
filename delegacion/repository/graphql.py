from delegacion.schemas_graphql import DelegacionModel
import graphene


class Query(graphene.ObjectType):
    all_delegaciones = graphene.List(DelegacionModel)

    post_by_id = graphene.Field(DelegacionModel, post_id=graphene.Int(required=True))


    def resolve_all_delegaciones(self, info):
        query = DelegacionModel.get_query(info)
        return query.all()