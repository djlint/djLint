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

const contentHash = (file) =>
  new Promise(function (resolve, reject) {
    const hash = crypto.createHash("sha256");
    const input = fs.createReadStream(file);

    input.on("error", reject);

    input.on("data", function (chunk) {
      hash.update(chunk);
    });

    input.on("close", function () {
      resolve(hash.digest("hex"));
    });
  });

class Rollupper {
  inputFiles = {};
  rollupOptions = {};

  constructor(eleventyConfig, { shortcode = "rollup", rollup } = {}) {
    this.rollupOptions = rollup;
    eleventyConfig.on("beforeBuild", () => this.beforeBuild());
    eleventyConfig.on("afterBuild", () => this.afterBuild());

    const plugin = this;
    eleventyConfig.addAsyncShortcode(shortcode, function (...args) {
      return plugin.rollupperShortcode(this, ...args);
    });
  }

  beforeBuild() {
    this.inputFiles = {};
  }

  async rollupperShortcode(eleventyInstance, src, fileRelative = false) {
    if (fileRelative) {
      src = path.join(path.dirname(eleventyInstance.page.inputPath), src);
    }

    const absoluteSource = path.resolve(src);
    const scriptSrc = (await contentHash(absoluteSource)).substr(0, 6) + ".js";
    this.inputFiles[absoluteSource] = scriptSrc;

    const bundledPath = path.relative(
      eleventyInstance.page.outputPath,
      path.join(this.rollupOptions.output.dir, scriptSrc),
    );

    return `<script src="${bundledPath}" type="module"></script>`;
  }

  async afterBuild() {
    const nothingToBundle = !Object.keys(this.inputFiles).length;
    if (nothingToBundle) {
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
