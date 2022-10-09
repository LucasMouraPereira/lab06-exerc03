import { client } from "./server/api";
import { GET_REPOSITORIES } from "./graphql/schema";
import { writeCSV } from "./modules/writeFile";

let variables = {
  first: 100,
  after: null,
};

client.request(GET_REPOSITORIES, variables).then(({ search }) => {
  writeCSV(search.nodes);
});
