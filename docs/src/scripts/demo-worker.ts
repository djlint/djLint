// The messages between the demo page and its worker, public/static/js/worker.js.

/** A finding as djlint.api.lint_text gives it. */
export interface Finding {
  code: string;
  column: number;
  end_column: number;
  end_line: number;
  line: number;
  message: string;
}

/** The template to run djLint on, with djlint.api.load_config's keyword arguments. */
export interface WorkerRequest {
  html: string;
  id: number;
  options: Record<string, string | number | boolean>;
}

/** What the worker answers. Its Python side sends the version and the fields of a result. */
export type WorkerReply =
  | { message: "error" | "ready"; type: "status" }
  | { message: string; type: "version" }
  | { findings: Finding[]; html: string; id: number; type: "result"; warnings: string[] }
  | { id: number; message: string; type: "error" };
