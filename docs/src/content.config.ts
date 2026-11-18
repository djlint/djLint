import { docsLoader, i18nLoader } from "@astrojs/starlight/loaders";
import { docsSchema, i18nSchema } from "@astrojs/starlight/schema";
import { z } from "astro/zod";
import { defineCollection } from "astro:content";

import en from "./content/i18n/en.json";

type Translatable<T> = Record<keyof T, z.ZodOptional<z.ZodString>>;

/**
 * Every djlint.* string the English dictionary defines may be translated.
 * @param dictionary - The English dictionary.
 * @returns A schema field for each of its strings, which also tells Starlight's t() the keys.
 */
function translatable<T extends Record<string, string>>(dictionary: T): Translatable<T> {
  const fields = Object.fromEntries(
    Object.keys(dictionary).map((key) => [key, z.string().optional()]),
  );
  // oxlint-disable-next-line typescript/no-unsafe-type-assertion -- Object.fromEntries forgets the keys
  return fields as Translatable<T>;
}

const djlintStrings = z.object(translatable(en));

export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
  i18n: defineCollection({ loader: i18nLoader(), schema: i18nSchema({ extend: djlintStrings }) }),
};
