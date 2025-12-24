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


class ProjectStatsType(graphene.ObjectType):
    total_tasks = graphene.Int()
    completed_tasks = graphene.Int()
    in_progress_tasks = graphene.Int()
    todo_tasks = graphene.Int()
    completion_rate = graphene.Float()


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

    project_stats = graphene.Field(
        ProjectStatsType,
        project_id=graphene.ID(required=True)
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

    def resolve_project_stats(self, info, project_id):
        tasks = Task.objects.filter(project_id=project_id)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status="DONE").count()
        in_progress_tasks = tasks.filter(status="IN_PROGRESS").count()
        todo_tasks = tasks.filter(status="TODO").count()
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return ProjectStatsType(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            in_progress_tasks=in_progress_tasks,
            todo_tasks=todo_tasks,
            completion_rate=completion_rate
        )

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


# Task mutations

class CreateTask(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String(required=False)
        status = graphene.String(required=False)
        assignee_email = graphene.String(required=False)
        due_date = graphene.String(required=False)

    task = graphene.Field(TaskType)

    def mutate(
        self,
        info,
        project_id,
        title,
        description=None,
        status="TODO",
        assignee_email=None,
        due_date=None
    ):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise Exception("Project not found")

        task = Task.objects.create(
            project=project,
            title=title,
            description=description or "",
            status=status,
            assignee_email=assignee_email or "",
            due_date=due_date if due_date else None
        )

        return CreateTask(task=task)
    


class UpdateTask(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)
        title = graphene.String(required=False)
        description = graphene.String(required=False)
        status = graphene.String(required=False)
        assignee_email = graphene.String(required=False)
        due_date = graphene.String(required=False)

    task = graphene.Field(TaskType)

    def mutate(
        self,
        info,
        task_id,
        title=None,
        description=None,
        status=None,
        assignee_email=None,
        due_date=None
    ):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Exception("Task not found")

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if assignee_email is not None:
            task.assignee_email = assignee_email
        if due_date is not None:
            task.due_date = due_date

        task.save()
        return UpdateTask(task=task)
    

class DeleteTask(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Exception("Task not found")

        task.delete()
        return DeleteTask(success=True)



# Task Comments

class AddTaskComment(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)
        content = graphene.String(required=True)
        author_email = graphene.String(required=True)

    comment = graphene.Field(TaskCommentType)

    def mutate(self, info, task_id, content, author_email):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Exception("Task not found")

        comment = TaskComment.objects.create(
            task=task,
            content=content,
            author_email=author_email
        )

        return AddTaskComment(comment=comment)



class DeleteTaskComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, comment_id):
        try:
            comment = TaskComment.objects.get(id=comment_id)
        except TaskComment.DoesNotExist:
            raise Exception("Comment not found")

        comment.delete()
        return DeleteTaskComment(success=True)



class CoreMutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()
    add_task_comment = AddTaskComment.Field()
    delete_task_comment = DeleteTaskComment.Field()

