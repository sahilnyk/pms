import { gql } from "@apollo/client";

export const GET_TASK_COMMENTS = gql`
  query GetComments($taskId: ID!) {
    comments(taskId: $taskId) {
      id
      content
      authorEmail
    }
  }
`;

export const ADD_COMMENT = gql`
  mutation AddComment($taskId: ID!, $content: String!, $authorEmail: String!) {
    addTaskComment(taskId: $taskId, content: $content, authorEmail: $authorEmail) {
      comment {
        id
        content
        authorEmail
      }
    }
  }
`;
