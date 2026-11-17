/**
 * The page's Starlight route, or undefined outside one: starlight-llms-txt
 * renders pages for llms.txt without a route, and reading it there throws.
 */
export function starlightRoute(locals: App.Locals) {
  try {
    return locals.starlightRoute;
  } catch {
    return undefined;
  }
}

/** The page's id without its locale, the same in every language: "docs/linter". */
export function pageId({ id, locale }: { id: string; locale?: string | undefined }) {
  return locale ? id.slice(locale.length + 1) : id;
}
