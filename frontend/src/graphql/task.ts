import { gql } from "@apollo/client";

export const CREATE_TASK = gql`
  mutation CreateTask(
    $projectId: ID!
    $title: String!
    $description: String
    $assigneeEmail: String
  ) {
    createTask(
      projectId: $projectId
      title: $title
      description: $description
      assigneeEmail: $assigneeEmail
    ) {
      task {
        id
        title
        status
        description
        assigneeEmail
      }
    }
  }
`;
