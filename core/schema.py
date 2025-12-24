import graphene
from graphene_django.types import DjangoObjectType
from .models import Organization, Project, Task, TaskComment


# types
class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = "__all__"


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = "__all__"


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = "__all__"


class TaskCommentType(DjangoObjectType):
    class Meta:
        model = TaskComment
        fields = "__all__"

# queries
class CoreQuery(graphene.ObjectType):
    organizations = graphene.List(OrganizationType)
    
    projects = graphene.List(
        ProjectType,
        organization_slug=graphene.String(required=True)
    )

    tasks = graphene.List(
        TaskType,
        project_id=graphene.ID(required=True)
    )

    comments = graphene.List(
        TaskCommentType,
        task_id=graphene.ID(required=True)
    )

# resolvers

    def resolve_organizations(self, info):
        return Organization.objects.all()

    def resolve_projects(self, info, organization_slug):
        return Project.objects.filter(organization__slug=organization_slug)

    def resolve_tasks(self, info, project_id):
        return Task.objects.filter(project_id=project_id)

    def resolve_comments(self, info, task_id):
        return TaskComment.objects.filter(task_id=task_id)
