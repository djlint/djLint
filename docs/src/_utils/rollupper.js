/*
rollup plugin from https://www.hoeser.dev/blog/2021-02-28-11ty-and-rollup/
*/

const rollup = require("rollup");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

module.exports = (eleventyConfig, options) => {
  new Rollupper(eleventyConfig, options);
};

class Rollupper {
  inputFiles = {};
  rollupOptions = {};

  constructor(eleventyConfig, { shortcode = "rollup", rollup } = {}) {
    this.rollupOptions = rollup;
    eleventyConfig.on("beforeBuild", () => this.beforeBuild());
    eleventyConfig.on("afterBuild", () => this.afterBuild());

    // We want to use "this" in the callback function, so we save the class instance beforehand
    const thisRollupper = this;
    eleventyConfig.addAsyncShortcode(shortcode, function (...args) {
      return thisRollupper.rollupperShortcode(this, ...args);
    });
  }

  beforeBuild() {
    this.inputFiles = {};
  }

  async rollupperShortcode(eleventyInstance, src, fileRelative = false) {
    // Resolve to the correct relative location
    if (fileRelative) {
      src = path.join(path.dirname(eleventyInstance.page.inputPath), src);
    }

    // resolve to absolute, since rollup uses absolute paths
    src = path.resolve(src);

    // generate a unique name for the file.
    // we take the first 6 chars of the sha256 of the absolute paths.
    const fileHash = await new Promise(function (resolve, reject) {
      const hash = crypto.createHash("sha256");
      const input = fs.createReadStream(src);

      input.on("error", reject);

      input.on("data", function (chunk) {
        hash.update(chunk);
      });

      input.on("close", function () {
        resolve(hash.digest("hex"));
      });
    });
    const scriptSrc = fileHash.substr(0, 6) + ".js";

    // register for rollup bundling
    this.inputFiles[src] = scriptSrc;

    // calculate script src after bundling
    const relativePath = path.relative(
      eleventyInstance.page.outputPath,
      path.join(this.rollupOptions.output.dir, scriptSrc),
    );

    return `<script src="${relativePath}" type="module"></script>`;
  }

  async afterBuild() {
    // Return early if no JS was used, since rollup throws on empty inputs
    if (!Object.keys(this.inputFiles).length) {
      return;
    }
    const bundle = await rollup.rollup({
      input: Object.keys(this.inputFiles),
      ...this.rollupOptions,
    });
    const inputFiles = this.inputFiles;
    await bundle.write({
      entryFileNames: (chunk) => {
        return inputFiles[chunk.facadeModuleId];
      },
      ...this.rollupOptions.output,
    });
    await bundle.close();
  }
}
