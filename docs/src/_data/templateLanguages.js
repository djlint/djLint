// Languages shown on the home page. `snippet` is a line of each language's
// own syntax, split into its opening delimiter, body and closing delimiter.
// `brand` colors the logo and the delimiters, and `logoScale` evens out
// logos whose drawing fills less of its box than the others.
module.exports = [
  {
    name: "Django",
    slug: "django",
    logo: "django.svg",
    brand: "#44b78b",
    snippet: ["{%", " url 'post' ", "%}"],
  },
  {
    name: "Jinja",
    slug: "jinja",
    logo: "jinja.svg",
    brand: "#d9473f",
    snippet: ["{{", " title|e ", "}}"],
  },
  {
    name: "Twig",
    slug: "twig",
    logo: "twig.svg",
    logoScale: 1.3,
    brand: "#8bb43a",
    snippet: ["{{", " name|upper ", "}}"],
  },
  {
    name: "Nunjucks",
    slug: "nunjucks",
    logo: "nunjucks.svg",
    brand: "#3f9a38",
    snippet: ["{%", " set n = 0 ", "%}"],
  },
  {
    name: "Handlebars",
    slug: "handlebars",
    logo: "handlebars.svg",
    brand: "#f0772b",
    snippet: ["{{#each", " posts", "}}"],
  },
  {
    name: "Liquid",
    slug: "liquid",
    logo: "liquid.svg",
    logoScale: 1.1,
    brand: "#3b82c4",
    snippet: ["{%", " unless ok ", "%}"],
  },
  {
    name: "Go templates",
    slug: "golang",
    logo: "golang.svg",
    logoScale: 1.8,
    brand: "#00add8",
    snippet: ["{{", " with .User ", "}}"],
  },
  {
    name: "Angular",
    slug: "angular",
    logo: "angular.svg",
    brand: "#dd0031",
    snippet: ["@if", " (user) ", "{"],
  },
  {
    name: "Mustache",
    slug: "mustache",
    logo: "mustache.svg",
    brand: "#9a9a9a",
    snippet: ["{{#", "items", "}}"],
  },
  {
    name: "Tera",
    slug: "tera",
    logo: "tera.svg",
    logoScale: 0.8,
    brand: "#1a8a7f",
    snippet: ["{%", " macro btn() ", "%}"],
  },
  {
    name: "Askama",
    slug: "askama",
    logo: "askama.svg",
    brand: "#c0392b",
    snippet: ["{%", " match item ", "%}"],
  },
];
