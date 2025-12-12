import { n as ArgumentHandler, s as OptionHandler } from "./t-D8yuw7Fz.js";

//#region src/shared.d.ts
interface CompletionConfig {
  subCommands?: Record<string, CompletionConfig>;
  options?: Record<string, OptionHandler>;
  args?: Record<string, ArgumentHandler>;
}
//#endregion
export { CompletionConfig as t };