import { l as RootCommand } from "./t-D8yuw7Fz.js";
import { t as CompletionConfig } from "./shared-hY8JIYei.js";
import { ArgsDef, CommandDef } from "citty";

//#region src/citty.d.ts
declare function tab<TArgs extends ArgsDef>(instance: CommandDef<TArgs>, completionConfig?: CompletionConfig): Promise<RootCommand>;
//#endregion
export { tab as default };