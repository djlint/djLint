import { HighlightStyle, syntaxHighlighting } from "@codemirror/language";
import { tags as t } from "@lezer/highlight";
import { EditorView } from "codemirror";

// Dark in both color schemes, with the Tomorrow Night colors the code
// blocks on the rest of the site use.
const mono = "Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace";

const theme = EditorView.theme(
  {
    "&": {
      height: "100%",
      backgroundColor: "#2d2d2d",
      color: "#cccccc",
      fontSize: "0.875rem",
    },
    "&.cm-focused": { outline: "none" },
    ".cm-scroller": { fontFamily: mono, lineHeight: "1.6" },
    ".cm-content": { caretColor: "#f2bd1d", padding: "0.75rem 0" },
    ".cm-cursor, .cm-dropCursor": { borderLeftColor: "#f2bd1d" },
    "&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection":
      { backgroundColor: "#515151" },
    ".cm-gutters": {
      backgroundColor: "#2d2d2d",
      color: "#6f6f6f",
      border: "none",
    },
    ".cm-activeLine": { backgroundColor: "#ffffff0a" },
    ".cm-activeLineGutter": { backgroundColor: "#ffffff0a", color: "#cccccc" },
    ".cm-matchingBracket, .cm-nonmatchingBracket": {
      backgroundColor: "#ffffff1a",
      outline: "none",
    },
    ".cm-foldPlaceholder": {
      backgroundColor: "#3a3a3a",
      border: "none",
      color: "#cccccc",
    },
    ".cm-tooltip": {
      backgroundColor: "#252525",
      border: "1px solid #3a3a3a",
      color: "#cccccc",
    },
    ".cm-tooltip-autocomplete > ul > li[aria-selected]": {
      backgroundColor: "#3a3a3a",
      color: "#ffffff",
    },
  },
  { dark: true },
);

const highlight = HighlightStyle.define([
  { tag: [t.tagName, t.attributeName], color: "#e2777a" },
  { tag: [t.attributeValue, t.string], color: "#7ec699" },
  { tag: [t.angleBracket, t.punctuation], color: "#cccccc" },
  { tag: t.comment, color: "#999999", fontStyle: "italic" },
  { tag: [t.keyword, t.processingInstruction], color: "#cc99cd" },
  { tag: [t.number, t.bool], color: "#f08d49" },
  { tag: [t.propertyName, t.className], color: "#f8c555" },
  { tag: [t.function(t.variableName)], color: "#6196cc" },
  { tag: t.invalid, color: "#ff6b6b" },
]);

export const djlintEditorTheme = [theme, syntaxHighlighting(highlight)];
