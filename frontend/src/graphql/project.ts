import { gql } from "@apollo/client";

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
