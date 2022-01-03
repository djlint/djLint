const algoliasearch = require("algoliasearch");

const objects = require("../../_site/search/all.json");

const client = algoliasearch('QFXNLHI6NP', process.env.ALGOLIA_SEARCH);

const index = client.initIndex('dev_atlas');

index.replaceAllObjects(objects, { autoGenerateObjectIDIfNotExist: true }).then(() => {
  console.log("updated");
}).catch((error) => console.error("Failed to Algolia update index", error));
