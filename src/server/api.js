import { GraphQLClient } from "graphql-request";
import "../config";

export const client = new GraphQLClient(process.env.API_URL, {
  headers: {
    authorization: `Bearer ${process.env.API_KEY}`,
  },
});
