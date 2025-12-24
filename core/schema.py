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

# Project Mutations

class CreateProject(graphene.Mutation):
    class Arguments:
        organization_slug = graphene.String(required=True)
        name = graphene.String(required=True)
        description = graphene.String(required=False)
        status = graphene.String(required=False)
        due_date = graphene.String(required=False)

    project = graphene.Field(ProjectType)

    def mutate(self, info, organization_slug, name, description=None, status="ACTIVE", due_date=None):
        try:
            org = Organization.objects.get(slug=organization_slug)
        except Organization.DoesNotExist:
            raise Exception("Organization not found")

        project = Project.objects.create(
            organization=org,
            name=name,
            description=description or "",
            status=status,
            due_date=due_date if due_date else None
        )

        return CreateProject(project=project)


class UpdateProject(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        name = graphene.String(required=False)
        description = graphene.String(required=False)
        status = graphene.String(required=False)
        due_date = graphene.String(required=False)

    project = graphene.Field(ProjectType)

    def mutate(self, info, project_id, name=None, description=None, status=None, due_date=None):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise Exception("Project not found")

        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        if status is not None:
            project.status = status
        if due_date is not None:
            project.due_date = due_date

        project.save()
        return UpdateProject(project=project)


class DeleteProject(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise Exception("Project not found")

        project.delete()
        return DeleteProject(success=True)


class CoreMutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()
