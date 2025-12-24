import { gql } from "@apollo/client";

export const UPDATE_TASK_STATUS = gql`
  mutation UpdateTaskStatus($taskId: ID!, $status: String!) {
    updateTask(taskId: $taskId, status: $status) {
      task {
        id
        status
      }
    }
  }
`;
