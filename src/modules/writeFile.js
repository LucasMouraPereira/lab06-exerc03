import fs from "fs";
import csvWriter from "csv-write-stream";

export const writeCSV = async (nodes) => {
  let writer = null;
  let file = "./src/out/lab03.csv";
  const writableStream = fs.createWriteStream(file, { flags: "a" });

  if (!fs.existsSync(file)) {
    writer = csvWriter({
      headers: [
        "id",
        "name",
        "url",
        "ownerId",
        "ownerLogin",
        "primaryLanguageId",
        "primaryLanguageName",
        "createdAt",
        "stargazerCount",
        "totalPullRequestsMerged",
      ],
    });
  } else {
    writer = csvWriter({ sendHeaders: false });
  }

  writer.pipe(writableStream);

  await nodes.map(async (node) => {
    return new Promise((resolve, reject) => {
      writer.write({
        id: node?.id,
        name: node?.name,
        url: node?.url,
        ownerId: node?.owner?.id,
        ownerLogin: node?.owner?.login,
        primaryLanguageId:
          node.primaryLanguage === null ? node?.primaryLanguage?.id : "",
        primaryLanguageName:
          node.primaryLanguage === null ? node?.primaryLanguage?.name : "",
        createdAt: node?.createdAt,
        stargazerCount: node?.stargazerCount,
        totalPullRequestsMerged: node?.pullRequests.totalCount,
      });
    });
  });

  writer.end();
  console.log("Finished writing data");
};
