from graphene_django.utils.testing import GraphQLTestCase
from core.models import Organization, Project, Task
from backend.schema import schema


class ProjectSystemTests(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = "/graphql/"   # Important fix

    def setUp(self):
        self.org = Organization.objects.create(
            name="AVG",
            slug="avg",
            contact_email="avg@test.com"
        )

        self.project = Project.objects.create(
            organization=self.org,
            name="Sample Project",
            status="ACTIVE"
        )

    def test_list_projects(self):
        response = self.query(
            """
            query($slug: String!) {
              projects(organizationSlug: $slug) {
                name
                status
              }
            }
            """,
            variables={"slug": "avg"}
        )

        self.assertResponseNoErrors(response)

        data = response.json()["data"]["projects"]
        assert len(data) == 1
        assert data[0]["name"] == "Sample Project"

    def test_create_project(self):
        response = self.query(
            """
            mutation($slug: String!, $name: String!) {
              createProject(organizationSlug: $slug, name: $name) {
                project {
                  name
                  status
                }
              }
            }
            """,
            variables={
                "slug": "avg",
                "name": "New Project"
            }
        )

        self.assertResponseNoErrors(response)
        assert Project.objects.filter(name="New Project").exists()

    def test_create_task(self):
        response = self.query(
            """
            mutation($projectId: ID!, $title: String!) {
              createTask(projectId: $projectId, title: $title) {
                task {
                  title
                  status
                }
              }
            }
            """,
            variables={
                "projectId": self.project.id,
                "title": "First Task"
            }
        )

        self.assertResponseNoErrors(response)
        assert Task.objects.filter(title="First Task").exists()

    def test_add_comment(self):
        task = Task.objects.create(
            project=self.project,
            title="Comment Task",
            status="TODO"
        )

        response = self.query(
            """
            mutation($id: ID!, $content: String!, $email: String!) {
              addTaskComment(taskId: $id, content: $content, authorEmail: $email) {
                comment {
                  content
                }
              }
            }
            """,
            variables={
                "id": task.id,
                "content": "Nice Work",
                "email": "user@test.com"
            }
        )

        self.assertResponseNoErrors(response)

        content = response.json()["data"]["addTaskComment"]["comment"]["content"]
        assert content == "Nice Work"

    def test_project_stats(self):
        Task.objects.create(project=self.project, title="A", status="DONE")
        Task.objects.create(project=self.project, title="B", status="TODO")

        response = self.query(
            """
            query($id: ID!) {
              projectStats(projectId: $id) {
                totalTasks
                completedTasks
                todoTasks
              }
            }
            """,
            variables={"id": self.project.id}
        )

        self.assertResponseNoErrors(response)

        stats = response.json()["data"]["projectStats"]
        assert stats["totalTasks"] == 2
        assert stats["completedTasks"] == 1
        assert stats["todoTasks"] == 1
