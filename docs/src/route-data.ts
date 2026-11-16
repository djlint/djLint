import { defineRouteMiddleware } from "@astrojs/starlight/route-data";
import options from "./data/configuration.json";

// The configuration page renders its options in a component, so Astro never
// sees their headings. List them in the table of contents under the last
// heading of the page, "Options".
export const onRequest = defineRouteMiddleware(({ locals }) => {
  const { id, locale, toc } = locals.starlightRoute;
  const page = locale ? id.slice(locale.length + 1) : id;
  const section = toc?.items.at(-1);
  if (page !== "docs/configuration" || !section) return;
  section.children = options
    .map(({ name }) => name)
    .toSorted((a, b) => a.localeCompare(b))
    .map((name) => ({ depth: 3, slug: name.replaceAll("_", "-"), text: name, children: [] }));
});
