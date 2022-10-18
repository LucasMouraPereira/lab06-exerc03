import { client } from "./server/api";
import { GET_REPOSITORIES } from "./graphql/schema";
import { writeCSV } from "./modules/writeFile";
import { writeJson } from "./modules/writeJson";

import _ from "lodash";

const main = async () => {
  let data = [];
  let variables = {
    first: 10,
    after: null,
  };
  for (let i = 0; i < 10; i++) {
    await client.request(GET_REPOSITORIES, variables).then(({ search }) => {
      data.push(search.nodes);
      writeCSV(search.nodes);
      variables = {
        first: 10,
        after: search.pageInfo.endCursor,
      };
    });
  }
  writeJson(_.concat(data));
};

main();
