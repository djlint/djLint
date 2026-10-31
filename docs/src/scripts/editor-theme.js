import { HighlightStyle, syntaxHighlighting } from "@codemirror/language";
import { tags as t } from "@lezer/highlight";
import { EditorView } from "codemirror";

// Dark in both color schemes, with the Tokyo Night colors the code blocks and
// the home page editor use.
const theme = EditorView.theme(
  {
    "&": {
      height: "100%",
      backgroundColor: "#1a1b26",
      color: "#c0caf5",
      fontSize: "0.85rem",
    },
    "&.cm-focused": { outline: "none" },
    ".cm-scroller": { fontFamily: "var(--sl-font-mono)", lineHeight: "1.7" },
    ".cm-content": { caretColor: "#f5c542", padding: "0.75rem 0" },
    ".cm-cursor, .cm-dropCursor": { borderLeftColor: "#f5c542" },
    "&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection":
      { backgroundColor: "#283457" },
    ".cm-gutters": {
      backgroundColor: "#1a1b26",
      color: "#3b4061",
      border: "none",
    },
    ".cm-activeLine": { backgroundColor: "#ffffff08" },
    ".cm-activeLineGutter": { backgroundColor: "#ffffff08", color: "#a9b1d6" },
    ".cm-matchingBracket, .cm-nonmatchingBracket": {
      backgroundColor: "#ffffff1a",
      outline: "none",
    },
    ".cm-foldPlaceholder": {
      backgroundColor: "#24283b",
      border: "none",
      color: "#c0caf5",
    },
    ".cm-tooltip": {
      backgroundColor: "#24283b",
      border: "1px solid #2a2c3d",
      color: "#c0caf5",
    },
    ".cm-tooltip-autocomplete > ul > li[aria-selected]": {
      backgroundColor: "#283457",
      color: "#ffffff",
    },
  },
  { dark: true },
);

const highlight = HighlightStyle.define([
  { tag: t.tagName, color: "#f7768e" },
  { tag: t.attributeName, color: "#bb9af7" },
  { tag: [t.attributeValue, t.string], color: "#9ece6a" },
  { tag: [t.angleBracket, t.punctuation], color: "#89ddff" },
  { tag: t.comment, color: "#565f89", fontStyle: "italic" },
  { tag: [t.keyword, t.processingInstruction], color: "#7dcfff" },
  { tag: [t.number, t.bool], color: "#ff9e64" },
  { tag: [t.propertyName, t.className], color: "#e0af68" },
  { tag: [t.function(t.variableName)], color: "#7aa2f7" },
  { tag: t.invalid, color: "#f7768e" },
]);

export const djlintEditorTheme = [theme, syntaxHighlighting(highlight)];
