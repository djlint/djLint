import { defineRouteMiddleware } from "@astrojs/starlight/route-data";

import { getHeadings } from "../../CHANGELOG.md";
import options from "./data/configuration.json";
import { pageId } from "./utils/route";

// The configuration page and the changelog render their sections in a
// component, so Astro never sees their headings. List them in the table of
// contents: the options under the last heading of the configuration page,
// "Options", and the releases on the changelog, by version.
export const onRequest = defineRouteMiddleware(({ locals }) => {
  const { toc } = locals.starlightRoute;
  const page = pageId(locals.starlightRoute);
  if (!toc) {
    return;
  }
  if (page === "docs/configuration") {
    const section = toc.items.at(-1);
    if (!section) {
      return;
    }
    section.children = options
      .map(({ name }) => name)
      .toSorted((a, b) => a.localeCompare(b))
      .map((name) => ({ children: [], depth: 3, slug: name.replaceAll("_", "-"), text: name }));
  } else if (page === "docs/changelog") {
    toc.items.push(
      ...getHeadings()
        .filter(({ depth }) => depth === 2)
        .map(({ slug, text }) => ({
          children: [],
          depth: 2,
          slug,
          text: /^\[(?<version>.+?)\]/u.exec(text)?.groups?.["version"] ?? text,
        })),
    );
  }
});
