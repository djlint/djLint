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
