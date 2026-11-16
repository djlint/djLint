// The demo keeps its input and settings in the address, as deflated JSON in
// base64url after the "#", so a link opens the same example.

export interface DemoState {
  html: string;
  config: Record<string, string | boolean>;
}

async function pipe(bytes: BufferSource, transform: CompressionStream | DecompressionStream) {
  const stream = new Blob([bytes]).stream().pipeThrough(transform);
  return new Uint8Array(await new Response(stream).arrayBuffer());
}

export async function encodeState(state: DemoState): Promise<string> {
  const bytes = await pipe(
    new TextEncoder().encode(JSON.stringify(state)),
    new CompressionStream("deflate-raw"),
  );
  const binary = Array.from(bytes, (byte) => String.fromCharCode(byte)).join("");
  return btoa(binary).replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/, "");
}

/** The state in `hash`, or undefined when it holds none or is damaged. */
export async function decodeState(hash: string): Promise<DemoState | undefined> {
  if (!hash) return undefined;
  try {
    const binary = atob(hash.replaceAll("-", "+").replaceAll("_", "/"));
    const bytes = await pipe(
      Uint8Array.from(binary, (char) => char.charCodeAt(0)),
      new DecompressionStream("deflate-raw"),
    );
    const state = JSON.parse(new TextDecoder().decode(bytes));
    const valid =
      typeof state?.html === "string" && state.config && typeof state.config === "object";
    return valid ? state : undefined;
  } catch {
    return undefined;
  }
}
