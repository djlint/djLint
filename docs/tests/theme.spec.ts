import { expect, test } from "./fixtures";

for (const theme of ["light", "dark"]) {
  test(`code blocks stand out from the page in the ${theme} theme`, async ({ page }) => {
    await page.addInitScript((value) => localStorage.setItem("starlight-theme", value), theme);
    await page.goto("/docs/getting-started/");
    await expect(page.locator("html")).toHaveAttribute("data-theme", theme);

    // The contrast ratio between the block's background and the first one
    // behind it, as WCAG computes it.
    const contrast = await page
      .locator(".expressive-code pre")
      .first()
      .evaluate((pre) => {
        const context = document
          .createElement("canvas")
          .getContext("2d", { willReadFrequently: true });
        if (!context) {
          throw new Error("no 2D canvas");
        }
        // The canvas turns any CSS color into sRGB bytes.
        const rgba = (color: string) => {
          context.clearRect(0, 0, 1, 1);
          context.fillStyle = color;
          context.fillRect(0, 0, 1, 1);
          const [r = 0, g = 0, b = 0, a = 0] = context.getImageData(0, 0, 1, 1).data;
          return { a, b, g, r };
        };
        const background = (element: Element | null | undefined) => {
          for (let node = element; node; node = node.parentElement) {
            const color = rgba(getComputedStyle(node).backgroundColor);
            if (color.a === 255) {
              return color;
            }
          }
          return rgba("white");
        };
        const linear = (byte: number) => {
          const c = byte / 255;
          return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
        };
        const luminance = ({ b, g, r }: { b: number; g: number; r: number }) =>
          0.2126 * linear(r) + 0.7152 * linear(g) + 0.0722 * linear(b);
        const block = luminance(background(pre));
        const page = luminance(
          background(pre.parentElement?.closest(".expressive-code")?.parentElement),
        );
        return (Math.max(block, page) + 0.05) / (Math.min(block, page) + 0.05);
      });
    // #f6f7fa on white is 1.07.
    expect(contrast).toBeGreaterThan(1.05);
  });
}
