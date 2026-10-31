import { docsLoader, i18nLoader } from "@astrojs/starlight/loaders";
import { docsSchema, i18nSchema } from "@astrojs/starlight/schema";
import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import en from "./content/i18n/en.json";

// Every djlint.* string the English dictionary defines may be translated.
const djlintStrings = Object.fromEntries(
  Object.keys(en).map((key) => [key, z.string().optional()]),
);

export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
  i18n: defineCollection({
    loader: i18nLoader(),
    schema: i18nSchema({ extend: z.object(djlintStrings) }),
  }),
};
