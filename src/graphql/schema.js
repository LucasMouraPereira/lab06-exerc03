import { gql } from 'graphql-request'

export const GET_REPOSITORIES = gql`
  query GetRepositories($first: Int!, $after: String) {
    search(query: "stars:>100", type: REPOSITORY, first: $first, after: $after) {
      nodes {
        ... on Repository {
          id
          name
          url
          owner {
            id
            login
          }
          primaryLanguage {
            id
            name
          }
          createdAt
          stargazerCount
          pullRequests(states: MERGED, first: 100) {
            totalCount
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
`;
