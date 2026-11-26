// The demo keeps its input and settings in the address, as deflated JSON in
// base64url after the "#", so a link opens the same example.

export interface DemoState {
  html: string;
  config: Record<string, string | boolean>;
}

async function pipe(
  bytes: BufferSource,
  transform: CompressionStream | DecompressionStream,
): Promise<Uint8Array<ArrayBuffer>> {
  const stream = new Blob([bytes]).stream().pipeThrough(transform);
  return new Uint8Array(await new Response(stream).arrayBuffer());
}

function isConfig(value: unknown): value is DemoState["config"] {
  return (
    typeof value === "object" &&
    value !== null &&
    !Array.isArray(value) &&
    Object.values(value).every((item) => typeof item === "string" || typeof item === "boolean")
  );
}

function isDemoState(value: unknown): value is DemoState {
  return (
    typeof value === "object" &&
    value !== null &&
    "html" in value &&
    typeof value.html === "string" &&
    "config" in value &&
    isConfig(value.config)
  );
}

export async function encodeState(state: DemoState): Promise<string> {
  const bytes = await pipe(
    new TextEncoder().encode(JSON.stringify(state)),
    new CompressionStream("deflate-raw"),
  );
  const binary = Array.from(bytes, (byte) => String.fromCodePoint(byte)).join("");
  return btoa(binary).replaceAll("+", "-").replaceAll("/", "_").replace(/[=]+$/u, "");
}

/**
 * Reads the state back from the address.
 * @param hash - The address's hash, without the "#".
 * @returns The state, or undefined when the hash holds none or is damaged.
 */
export async function decodeState(hash: string): Promise<DemoState | undefined> {
  if (!hash) {
    return void 0;
  }
  try {
    const binary = atob(hash.replaceAll("-", "+").replaceAll("_", "/"));
    const bytes = await pipe(
      Uint8Array.from(binary, (char) => char.codePointAt(0) ?? 0),
      new DecompressionStream("deflate-raw"),
    );
    const state: unknown = JSON.parse(new TextDecoder().decode(bytes));
    return isDemoState(state) ? state : void 0;
  } catch {
    return void 0;
  }
}
