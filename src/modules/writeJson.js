import fs from "fs";

export const writeJson = async (nodes) => {
  let file = "./src/out/lab03.json";
  fs.writeFile(file, JSON.stringify(nodes, null, "\t"), (err) => {
    if (err) return err;

    console.log("Finished writing data");
  });
};
