import { a as legacyRootDirArgs, i as extendsArgs, n as dotEnvArgs, o as logLevelArgs, r as envNameArgs, t as cwdArgs } from "./_shared-BCYCnX0T.mjs";
import "./logger-B4ge7MhP.mjs";
import "./kit-CPEUdXTm.mjs";
import "./versions-CTlxnxbH.mjs";
import "./banner-drlfl0J-.mjs";
import "./fs-B_hD5MnA.mjs";
import "./env-kdrdHqLf.mjs";
import build_default from "./build-BrNcO3Nf.mjs";
import { defineCommand } from "citty";

//#region ../nuxi/src/commands/generate.ts
var generate_default = defineCommand({
	meta: {
		name: "generate",
		description: "Build Nuxt and prerender all routes"
	},
	args: {
		...cwdArgs,
		...logLevelArgs,
		preset: {
			type: "string",
			description: "Nitro server preset"
		},
		...dotEnvArgs,
		...envNameArgs,
		...extendsArgs,
		...legacyRootDirArgs
	},
	async run(ctx) {
		ctx.args.prerender = true;
		await build_default.run(ctx);
	}
});

//#endregion
export { generate_default as default };