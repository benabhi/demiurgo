#!/usr/bin/env node
/**
 * Genera una imagen con Puter (puter.ai.txt2img) y la guarda en la bóveda.
 *
 * Uso:
 *   node generate_image.mjs --prompt-file <archivo> --dest <carpeta> --name Retrato_Nombre --aspect 1:1
 *   node generate_image.mjs --prompt-file - ...     lee el prompt de la entrada estándar
 *   node generate_image.mjs --login                  inicia sesión en Puter y la guarda
 *   node generate_image.mjs --logout                 borra la sesión guardada
 *   node generate_image.mjs --models                 lista los modelos de imagen de Puter
 *
 * Opciones: --model <id> y --quality <calidad> (si no se indican, los de Puter por defecto),
 * --test (imagen de muestra que no gasta saldo), --timeout <s> (generación, 300) y
 * --login-timeout <s> (inicio de sesión, 300).
 *
 * Sesión: usa PUTER_AUTH_TOKEN si está definida; si no, la guardada en
 * ~/.config/generar-imagen/puter_token. Si no hay ninguna, abre el navegador para iniciar sesión
 * en Puter (una sola vez) y la guarda ahí, fuera del repositorio. El token nunca se imprime.
 *
 * Nunca sobrescribe: si el nombre ya existe (con cualquier extensión), usa _v2, _v3…
 * La extensión sale del formato real de la imagen (png, jpg o webp).
 *
 * Salida: "<archivo>\t<tamaño>\t<ancho>×<alto>\t<modelo>". Códigos de salida: 0 bien, 1 error,
 * 2 sin sesión, 3 prompt rechazado por el filtro de contenido, 4 sin saldo, 5 fallo del proveedor.
 */
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { homedir } from "node:os";
import { dirname, join, parse, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

const EXIT = { OK: 0, ERROR: 1, SESSION: 2, MODERATION: 3, FUNDS: 4, PROVIDER: 5 };
const TOKEN_FILE = join(homedir(), ".config", "generar-imagen", "puter_token");
const SCRIPTS_DIR = dirname(fileURLToPath(import.meta.url));
const MIN_NODE = 24;

class ScriptError extends Error {
    constructor(code, message) {
        super(message);
        this.code = code;
    }
}

// Node avisa de que localStorage es experimental cuando Puter recorre los globales: aquí no aporta nada
process.removeAllListeners("warning");
process.on("warning", (warning) => {
    if (!String(warning.message).includes("localStorage")) {
        console.error(`${warning.name}: ${warning.message}`);
    }
});

const OPTIONS = {
    "prompt-file": { type: "string" },
    dest: { type: "string" },
    name: { type: "string" },
    aspect: { type: "string", default: "1:1" },
    model: { type: "string" },
    quality: { type: "string" },
    test: { type: "boolean", default: false },
    login: { type: "boolean", default: false },
    logout: { type: "boolean", default: false },
    models: { type: "boolean", default: false },
    timeout: { type: "string", default: "300" },
    "login-timeout": { type: "string", default: "300" },
    help: { type: "boolean", short: "h", default: false },
};

function parseOptions() {
    let values;
    try {
        ({ values } = parseArgs({ options: OPTIONS }));
    } catch (error) {
        throw new ScriptError(EXIT.ERROR, `${error.message} (usa --help para ver las opciones).`);
    }
    if (!/^\d+:\d+$/.test(values.aspect)) {
        throw new ScriptError(EXIT.ERROR, `--aspect debe ser una proporción como 1:1, 16:9 o 3:4 (llegó «${values.aspect}»).`);
    }
    return values;
}

function printHelp() {
    const source = readFileSync(fileURLToPath(import.meta.url), "utf8");
    const doc = source.match(/\/\*\*([\s\S]*?)\*\//)[1];
    console.log(doc.split("\n").map((line) => line.replace(/^ \* ?/, "")).join("\n").trim());
}

function loadPuter() {
    const require = createRequire(join(SCRIPTS_DIR, "package.json"));
    try {
        return require("@heyputer/puter.js/src/init.cjs");
    } catch {
        throw new ScriptError(EXIT.ERROR,
            `Falta la librería de Puter. Instálala una vez con: npm install --prefix "${SCRIPTS_DIR}"`);
    }
}

function withTimeout(promise, seconds, message) {
    let timer;
    const limit = new Promise((_, reject) => {
        timer = setTimeout(() => reject(new ScriptError(EXIT.PROVIDER, message)), seconds * 1000);
    });
    return Promise.race([promise, limit]).finally(() => clearTimeout(timer));
}

// --- Sesión ------------------------------------------------------------------

async function login(puterLib, seconds) {
    console.error("Se abre el navegador para iniciar sesión en Puter. Hace falta solo la primera vez.");
    const loginError = new ScriptError(EXIT.SESSION,
        `No se completó el inicio de sesión en Puter en ${seconds} s. Vuelve a ejecutar el script para intentarlo de nuevo.`);
    const token = await withTimeout(puterLib.getAuthToken(), seconds, loginError.message)
        .catch(() => { throw loginError; });
    if (!token) {
        throw new ScriptError(EXIT.SESSION, "Puter no devolvió la sesión. Vuelve a ejecutar el script para intentarlo de nuevo.");
    }
    mkdirSync(dirname(TOKEN_FILE), { recursive: true, mode: 0o700 });
    writeFileSync(TOKEN_FILE, token, { mode: 0o600 });
    return token;
}

async function session(puterLib, options, forceLogin = false) {
    if (process.env.PUTER_AUTH_TOKEN && !forceLogin) {
        return { token: process.env.PUTER_AUTH_TOKEN, source: "variable PUTER_AUTH_TOKEN" };
    }
    if (!forceLogin && existsSync(TOKEN_FILE)) {
        const token = readFileSync(TOKEN_FILE, "utf8").trim();
        if (token) {
            return { token, source: "archivo" };
        }
    }
    return { token: await login(puterLib, Number(options["login-timeout"])), source: "nueva" };
}

// --- Errores de Puter ----------------------------------------------------------

function classify(error) {
    if (error instanceof ScriptError) {
        return { kind: "script", error };
    }
    const inner = error && typeof error.error === "object" ? error.error : error;
    const code = String(inner?.code ?? "");
    const status = Number(inner?.status ?? error?.status ?? 0);
    const message = String(inner?.message ?? error?.message ?? (typeof error === "string" ? error : JSON.stringify(error)));
    const text = `${code} ${message}`.toLowerCase();
    let kind = "other";
    if (status === 401 || /unauthori|auth_failed|invalid_token|token_expired|token_auth/.test(text)) {
        kind = "auth";
    } else if (/moderation|content_policy|safety/.test(text)) {
        kind = "moderation";
    } else if (status === 402 || /insufficient_funds|subscription_required/.test(text)) {
        kind = "funds";
    } else if (code.startsWith("upstream") || status >= 500) {
        kind = "upstream";
    }
    return { kind, code, status, message };
}

function toScriptError(info) {
    const detail = [info.code, info.status || "", info.message].filter(Boolean).join(" · ");
    switch (info.kind) {
        case "script":
            return info.error;
        case "auth":
            return new ScriptError(EXIT.SESSION, `Puter no aceptó la sesión (${detail}).`);
        case "moderation":
            return new ScriptError(EXIT.MODERATION, `El filtro de contenido rechazó el prompt (${detail}). Suavízalo antes de reintentar.`);
        case "funds":
            return new ScriptError(EXIT.FUNDS, `No queda saldo en la cuenta de Puter para generar imágenes (${detail}).`);
        case "upstream":
            return new ScriptError(EXIT.PROVIDER, `Falló el proveedor de imágenes (${detail}).`);
        default:
            return new ScriptError(EXIT.ERROR, `Puter devolvió un error (${detail}).`);
    }
}

// --- Imagen --------------------------------------------------------------------

async function readImage(src) {
    if (typeof src !== "string" || !src) {
        throw new ScriptError(EXIT.ERROR, "Puter no devolvió ninguna imagen.");
    }
    if (src.startsWith("data:")) {
        const comma = src.indexOf(",");
        const data = src.slice(comma + 1);
        return src.slice(0, comma).endsWith(";base64") ? Buffer.from(data, "base64") : Buffer.from(decodeURIComponent(data));
    }
    if (/^https?:\/\//.test(src)) {
        // Las direcciones de Puter son temporales: se descarga en el momento
        const response = await fetch(src);
        if (!response.ok) {
            throw new ScriptError(EXIT.PROVIDER, `No se pudo descargar la imagen generada (HTTP ${response.status}).`);
        }
        return Buffer.from(await response.arrayBuffer());
    }
    throw new ScriptError(EXIT.ERROR, `Puter devolvió la imagen en un formato inesperado (${src.slice(0, 30)}…).`);
}

/** Formato real y tamaño en píxeles a partir de la cabecera (PNG, JPEG o WebP). */
function imageInfo(bytes) {
    if (bytes.length > 24 && bytes.readUInt32BE(0) === 0x89504e47) {
        return { ext: ".png", width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
    }
    if (bytes.length > 4 && bytes[0] === 0xff && bytes[1] === 0xd8) {
        let i = 2;
        while (i + 9 < bytes.length) {
            if (bytes[i] !== 0xff) {
                i++;
                continue;
            }
            const marker = bytes[i + 1];
            if (marker === 0xff || marker === 0x01 || (marker >= 0xd0 && marker <= 0xd8)) {
                i += marker === 0xff ? 1 : 2;
                continue;
            }
            // SOF0…SOF15, salvo DHT (c4), JPG (c8) y DAC (cc): ahí van el alto y el ancho
            if (marker >= 0xc0 && marker <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(marker)) {
                return { ext: ".jpg", width: bytes.readUInt16BE(i + 7), height: bytes.readUInt16BE(i + 5) };
            }
            i += 2 + bytes.readUInt16BE(i + 2);
        }
        return { ext: ".jpg" };
    }
    if (bytes.length > 30 && bytes.toString("ascii", 0, 4) === "RIFF" && bytes.toString("ascii", 8, 12) === "WEBP") {
        const chunk = bytes.toString("ascii", 12, 16);
        if (chunk === "VP8X") {
            return { ext: ".webp", width: 1 + bytes.readUIntLE(24, 3), height: 1 + bytes.readUIntLE(27, 3) };
        }
        if (chunk === "VP8 ") {
            return { ext: ".webp", width: bytes.readUInt16LE(26) & 0x3fff, height: bytes.readUInt16LE(28) & 0x3fff };
        }
        if (chunk === "VP8L") {
            const bits = bytes.readUInt32LE(21);
            return { ext: ".webp", width: (bits & 0x3fff) + 1, height: ((bits >> 14) & 0x3fff) + 1 };
        }
        return { ext: ".webp" };
    }
    return null;
}

/** Primer nombre libre; cuenta como ocupado el mismo nombre con cualquier extensión. */
function freeDestination(folder, name, ext) {
    const taken = new Set(readdirSync(folder)
        .filter((file) => statSync(join(folder, file)).isFile())
        .map((file) => parse(file).name.toLowerCase()));
    let candidate = name;
    for (let n = 2; taken.has(candidate.toLowerCase()); n++) {
        candidate = `${name}_v${n}`;
    }
    return join(folder, `${candidate}${ext}`);
}

function ratioWarning(aspect, info) {
    const match = /^(\d+):(\d+)$/.exec(aspect);
    if (!match || !info.width || !info.height) {
        return null;
    }
    const wanted = Number(match[1]) / Number(match[2]);
    const got = info.width / info.height;
    // Margen amplio: muchos modelos solo tienen unos pocos tamaños (3:2 por 16:9, por ejemplo)
    return Math.abs(got - wanted) / wanted > 0.2
        ? `Aviso: se pidió ${aspect} y la imagen salió de ${info.width}×${info.height}.`
        : null;
}

// --- Principal -----------------------------------------------------------------

async function generate(puterLib, options, prompt) {
    const request = { aspect_ratio: options.aspect };
    if (options.model) request.model = options.model;
    if (options.quality) request.quality = options.quality;
    if (options.test) request.test_mode = true;

    let { token, source } = await session(puterLib, options);
    for (let attempt = 1; ; attempt++) {
        const puter = puterLib.init(token);
        try {
            const image = await withTimeout(puter.ai.txt2img(prompt, request), Number(options.timeout),
                `Puter no devolvió la imagen en ${options.timeout} s.`);
            return image?.src ?? String(image ?? "");
        } catch (error) {
            const info = classify(error);
            if (info.kind === "auth" && source === "archivo" && attempt === 1) {
                // La sesión guardada caducó: se borra y se inicia sesión de nuevo, una vez
                rmSync(TOKEN_FILE, { force: true });
                ({ token, source } = await session(puterLib, options, true));
                continue;
            }
            if (info.kind === "upstream" && attempt === 1) {
                console.error("Falló el proveedor de imágenes; se reintenta una vez.");
                continue;
            }
            throw toScriptError(info);
        }
    }
}

async function main() {
    const major = Number(process.versions.node.split(".")[0]);
    if (major < MIN_NODE) {
        throw new ScriptError(EXIT.ERROR, `Hace falta Node.js ${MIN_NODE} o posterior (tienes ${process.versions.node}).`);
    }
    const options = parseOptions();
    if (options.help) {
        printHelp();
        return;
    }
    if (options.logout) {
        rmSync(TOKEN_FILE, { force: true });
        console.log("Sesión de Puter borrada.");
        return;
    }
    const puterLib = loadPuter();
    if (options.login) {
        const token = await login(puterLib, Number(options["login-timeout"]));
        const user = await withTimeout(puterLib.init(token).auth.getUser(), 20, "").catch(() => null);
        console.log(`Sesión de Puter guardada${user?.username ? ` (usuario ${user.username})` : ""}.`);
        return;
    }
    if (options.models) {
        const { token } = await session(puterLib, options);
        const response = await withTimeout(puterLib.init(token).drivers.call("puter-image-generation", "models", {}),
            30, "Puter no respondió con la lista de modelos.").catch((error) => { throw toScriptError(classify(error)); });
        const models = Array.isArray(response?.result) ? response.result : [];
        for (const model of models) {
            console.log(`${model.id}\t${String(model.provider ?? "").replace(/-image-generation$/, "")}`);
        }
        console.log(`(${models.length} modelos)`);
        return;
    }

    for (const required of ["prompt-file", "dest", "name"]) {
        if (!options[required]) {
            throw new ScriptError(EXIT.ERROR, `Falta --${required} (usa --help para ver las opciones).`);
        }
    }
    const promptFile = options["prompt-file"];
    const prompt = readFileSync(promptFile === "-" ? 0 : promptFile, "utf8").trim();
    if (!prompt) {
        throw new ScriptError(EXIT.ERROR, "El prompt está vacío.");
    }

    const src = await generate(puterLib, options, prompt);
    const bytes = await readImage(src);
    const info = imageInfo(bytes);
    if (!info) {
        throw new ScriptError(EXIT.ERROR, "Lo que devolvió Puter no es una imagen PNG, JPEG ni WebP.");
    }
    const folder = resolve(options.dest);
    mkdirSync(folder, { recursive: true });
    const final = freeDestination(folder, options.name, info.ext);
    writeFileSync(final, bytes, { flag: "wx" });

    const warning = ratioWarning(options.aspect, info);
    if (warning) {
        console.error(warning);
    }
    const size = info.width ? `${info.width}×${info.height}` : "tamaño desconocido";
    const model = options.test ? "imagen de muestra (--test)" : `modelo: ${options.model ?? "el de Puter por defecto"}`;
    console.log([parse(final).base, `${Math.round(bytes.length / 1024)} KB`, size, model].join("\t"));
}

main()
    .then(() => process.exit(EXIT.OK))
    .catch((error) => {
        console.error(`Error: ${error instanceof ScriptError ? error.message : error?.stack ?? error}`);
        process.exit(error instanceof ScriptError ? error.code : EXIT.ERROR);
    });
