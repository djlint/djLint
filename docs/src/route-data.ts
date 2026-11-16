import { defineRouteMiddleware } from "@astrojs/starlight/route-data";

import { getHeadings } from "../../CHANGELOG.md";
import options from "./data/configuration.json";

// The configuration page and the changelog render their sections in a
// component, so Astro never sees their headings. List them in the table of
// contents: the options under the last heading of the configuration page,
// "Options", and the releases on the changelog, by version.
export const onRequest = defineRouteMiddleware(({ locals }) => {
  const { id, locale, toc } = locals.starlightRoute;
  const page = locale ? id.slice(locale.length + 1) : id;
  if (!toc) return;
  if (page === "docs/configuration") {
    const section = toc.items.at(-1);
    if (!section) return;
    section.children = options
      .map(({ name }) => name)
      .toSorted((a, b) => a.localeCompare(b))
      .map((name) => ({ depth: 3, slug: name.replaceAll("_", "-"), text: name, children: [] }));
  } else if (page === "docs/changelog") {
    toc.items.push(
      ...getHeadings()
        .filter(({ depth }) => depth === 2)
        .map(({ slug, text }) => ({
          depth: 2,
          slug,
          text: text.match(/^\[(.+?)\]/u)?.[1] ?? text,
          children: [],
        })),
    );
  }
});
