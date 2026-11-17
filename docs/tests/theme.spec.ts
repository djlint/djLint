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
          .getContext("2d", { willReadFrequently: true })!;
        // The canvas turns any CSS color into sRGB bytes.
        const rgba = (color: string) => {
          context.clearRect(0, 0, 1, 1);
          context.fillStyle = color;
          context.fillRect(0, 0, 1, 1);
          return [...context.getImageData(0, 0, 1, 1).data];
        };
        const background = (element: Element | null) => {
          for (; element; element = element.parentElement) {
            const color = rgba(getComputedStyle(element).backgroundColor);
            if (color[3] === 255) return color;
          }
          return [255, 255, 255, 255];
        };
        const luminance = ([r, g, b]: number[]) => {
          const [lr, lg, lb] = [r, g, b].map((byte) => {
            const c = byte / 255;
            return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
          });
          return 0.2126 * lr + 0.7152 * lg + 0.0722 * lb;
        };
        const [a, b] = [
          background(pre),
          background(pre.parentElement!.closest(".expressive-code")!.parentElement),
        ].map(luminance);
        return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
      });
    // #f6f7fa on white is 1.07.
    expect(contrast).toBeGreaterThan(1.05);
  });
}
