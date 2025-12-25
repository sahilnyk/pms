import { gql } from "@apollo/client";

// Fetch project details + stats
export const GET_PROJECT_DETAILS = gql`
  query ProjectDetails($projectId: ID!) {
    tasks(projectId: $projectId) {
      id
      title
      status
      description
      assigneeEmail
    }

    projectStats(projectId: $projectId) {
      totalTasks
      completedTasks
      inProgressTasks
      todoTasks
      completionRate
    }
  }
`;

// Fetch projects by organization
export const GET_PROJECTS = gql`
  query GetProjects($slug: String!) {
    projects(organizationSlug: $slug) {
      id
      name
      description
      status
    }
  }
`;

// Create Project
export const CREATE_PROJECT = gql`
  mutation CreateProject(
    $organizationSlug: String!
    $name: String!
    $description: String
  ) {
    createProject(
      organizationSlug: $organizationSlug
      name: $name
      description: $description
    ) {
      project {
        id
        name
        description
        status
      }
    }
  }
`;

// Update Project
export const UPDATE_PROJECT = gql`
  mutation UpdateProject(
    $projectId: ID!
    $name: String
    $description: String
  ) {
    updateProject(
      projectId: $projectId
      name: $name
      description: $description
    ) {
      project {
        id
        name
        description
        status
      }
    }
  }
`;
