/**
 * Starlight's data for the page, if it has any.
 * @param locals - The page's `Astro.locals`.
 * @returns The page's Starlight route, or undefined outside one: starlight-llms-txt renders pages
 *   for llms.txt without a route, and reading it there throws.
 */
export function starlightRoute(locals: App.Locals): App.Locals["starlightRoute"] | undefined {
  try {
    return locals.starlightRoute;
  } catch {
    return void 0;
  }
}

/**
 * The page's id, the same in every language.
 * @param route - The page's Starlight route.
 * @param route.id - Its id, with the locale: "ru/docs/linter".
 * @param route.locale - Its locale, if it is a translation.
 * @returns The id without the locale: "docs/linter".
 */
export function pageId({ id, locale }: { id: string; locale?: string | undefined }): string {
  return locale ? id.slice(locale.length + 1) : id;
}
