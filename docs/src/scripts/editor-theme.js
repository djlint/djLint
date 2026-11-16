import { HighlightStyle, syntaxHighlighting } from "@codemirror/language";
import { tags as t } from "@lezer/highlight";
import { EditorView } from "codemirror";

// Dark in both color schemes, with the Tokyo Night colors the code blocks and
// the home page editor use.
const theme = EditorView.theme(
  {
    "&": { height: "100%", backgroundColor: "#222436", color: "#c0caf5", fontSize: "0.85rem" },
    "&.cm-focused": { outline: "none" },
    ".cm-scroller": { fontFamily: "var(--sl-font-mono)", lineHeight: "1.7" },
    ".cm-content": { caretColor: "#f5c542", padding: "0.75rem 0" },
    ".cm-cursor, .cm-dropCursor": { borderLeftColor: "#f5c542" },
    "&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection":
      { backgroundColor: "#2d3f76" },
    ".cm-gutters": { backgroundColor: "#222436", color: "#8a91b8", border: "none" },
    ".cm-activeLine": { backgroundColor: "#ffffff08" },
    ".cm-activeLineGutter": { backgroundColor: "#ffffff08", color: "#a9b1d6" },
    ".cm-matchingBracket, .cm-nonmatchingBracket": {
      backgroundColor: "#ffffff1a",
      outline: "none",
    },
    ".cm-foldPlaceholder": { backgroundColor: "#2f334d", border: "none", color: "#c0caf5" },
    ".cm-tooltip": { backgroundColor: "#2f334d", border: "1px solid #3b4261", color: "#c0caf5" },
    // Findings get the squiggle of the home page's editor.
    ".cm-lintRange-warning": {
      backgroundImage:
        "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='6' height='3'%3E%3Cpath d='M0 1.5 Q1.5 0 3 1.5 T6 1.5' fill='none' stroke='%23f5c542' stroke-width='1.2'/%3E%3C/svg%3E\")",
      backgroundSize: "6px 3px",
      paddingBottom: "2px",
    },
    ".cm-diagnostic": { padding: "0.3rem 0.6rem", fontSize: "0.75rem" },
    ".cm-diagnostic-warning": { borderLeft: "3px solid #f5c542" },
    ".cm-tooltip-autocomplete > ul > li[aria-selected]": {
      backgroundColor: "#2d3f76",
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
  // Lighter than Tokyo Night's comments, which are too faint to read on this background.
  { tag: t.comment, color: "#8a91b8", fontStyle: "italic" },
  { tag: [t.brace, t.processingInstruction], color: "#7dcfff" },
  { tag: t.keyword, color: "#bb9af7" },
  { tag: [t.operator, t.derefOperator], color: "#89ddff" },
  { tag: t.special(t.variableName), color: "#7aa2f7" },
  { tag: [t.number, t.bool, t.atom], color: "#ff9e64" },
  { tag: [t.propertyName, t.className], color: "#e0af68" },
  { tag: [t.function(t.variableName)], color: "#7aa2f7" },
  { tag: t.invalid, color: "#f7768e" },
]);

export const djlintEditorTheme = [theme, syntaxHighlighting(highlight)];
