---
name: generar-imagen
description: Genera la imagen de una entidad del mundo (el retrato de un personaje, el paisaje de una región…) con Puter, por script y sin abrir el navegador, con la ambientación del mundo y la técnica artística elegida (óleo, acuarela, cómic, lápiz a mano alzada, grabado… según su Guía Visual), y la guarda y enlaza en su nota de Obsidian de forma automática. La invoca crear-entidad al terminar; también sirve para "genera la imagen de…", "regenera el retrato de… en acuarela" o "cambia la técnica del mundo a óleo".
---

# Generar imagen

Arma un prompt con el estilo del mundo y los datos de la nota, genera la imagen con Puter mediante un script y la guarda en la bóveda, enlazada a la nota. **Todo el flujo es automático.**

El estilo tiene dos capas: la **ambientación**, que marca el mundo (género, tono, materiales, paleta), y la **técnica**, que elige el usuario de un catálogo de 27 (óleo, acuarela, cómic, lápiz, grabado, vitral, fotograma de cine…).

Uso: `/generar-imagen <nota> [técnica]`.
- `/generar-imagen Aldric_Voss` usa la técnica de la Guía Visual.
- `/generar-imagen Aldric_Voss acuarela` usa otra técnica solo para esta imagen: un id o un nombre de `referencias/tecnicas.md`, o una descripción propia ("como un mapa antiguo").
- También se puede pedir un modelo de Puter para una imagen ("con gemini-3-pro-image"), o fijarlo para todo el mundo en la sección "Modelo de imagen" de la Guía Visual.
- "Cambia la técnica del mundo a óleo" o "los paisajes, en acuarela" cambian la Guía Visual: la técnica general o la tabla "Técnica por tipo". Solo se tocan esas secciones.
- `/generar-imagen tecnicas` (o "¿qué técnicas hay?") muestra el índice de `referencias/tecnicas.md` tal cual, con el total, y dice qué técnica usa ahora el mundo y cómo pedir otra. No genera nada.
- `/generar-imagen modelos` muestra los modelos de imagen de Puter (`generate_image.mjs --models`) y cuál usa el mundo. No genera nada.
- `/generar-imagen Aldric_Voss navegador` usa la alternativa con Gemini en el Chrome del usuario (`referencias/navegador.md`).

## Autorización
El pedido del usuario (invocar esta skill o crear una entidad con `crear-entidad`) es la autorización explícita para generar **esta** imagen con Puter y guardarla en la bóveda. Por eso:
- no preguntes antes de generarla;
- no preguntes si la imagen gusta;
- no preguntes antes de guardarla.

Al terminar, informa de lo que hizo (ver "Paso 5: informe").

Solo se para a preguntar en dos casos: para elegir la técnica al crear la Guía Visual (una vez por mundo) y para descargar la librería de Puter si falta (ver "Requisitos").

## Requisitos
- **Node.js 24 o posterior.**
- **La librería de Puter** (`@heyputer/puter.js`, de npm) en `scripts/node_modules`, que no va al repositorio. Si el script dice que falta, pide permiso al usuario para descargarla (unos 9 MB con sus dependencias) y ejecuta `npm install --prefix <directorio de esta skill>/scripts`.
- **Una cuenta de Puter.** La primera vez, el script abre puter.com en el navegador del usuario y espera a que inicie sesión: avísale antes de ejecutarlo. Guarda la sesión en `~/.config/generar-imagen/puter_token`, fuera del repositorio; también acepta la variable `PUTER_AUTH_TOKEN`. Cada imagen gasta saldo de esa cuenta.

## Archivos de la skill
- `referencias/prompt.md`: qué muestra la imagen de cada tipo (formato, carpeta y prefijo del archivo), qué técnica usa cada imagen, la plantilla del prompt de cada tipo y de dónde sale cada campo.
- `referencias/tecnicas.md`: el catálogo de técnicas artísticas, con sus bloques en inglés y las recomendadas por género.
- `referencias/estilos.md`: la ambientación por género, cómo crear la Guía Visual y su plantilla.
- `referencias/navegador.md`: la alternativa con Gemini en el Chrome del usuario, solo si la pide.
- `scripts/generate_image.mjs`: genera la imagen con Puter y la guarda en la bóveda sin sobrescribir.
- `scripts/package.json`: la dependencia del script (la librería de Puter).
- `scripts/fetch_download.py`: mueve a la bóveda una imagen descargada desde el navegador (solo para la alternativa).

## Paso 1: preparar
1. Lee la nota de la entidad y su `tipo`. Busca el tipo en la tabla "Resumen por tipo" de `prompt.md`: de ahí salen su formato, su **carpeta** y su **prefijo**. Si el tipo no figura, o no lleva imagen, dilo y detente.
2. **Guía Visual:** lee `00_Sistema/04_Convenciones/Guia_Visual.md`.
   - Si no existe (es el primer uso en este mundo), créala siguiendo "Cómo crear la Guía Visual" de `estilos.md`: la ambientación y la paleta salen de la Ficha, y la técnica se pregunta al usuario **mostrándole el catálogo completo**, no solo las opciones del diálogo. Es la única pregunta del flujo y se hace una sola vez por mundo.
   - Al guardarla, añádela a la lista de convenciones de `MOC_Inicio`.
   - Si es del formato anterior (sin sección "Técnica"), sigue "Guías de la versión anterior" de `estilos.md`. Si sus Restricciones incluyen un formato ("square 1:1") o "single subject", o su Estilo dice "portrait", **ignora esas partes** para tipos que no son retratos: el formato y el sujeto los pone cada tipo.
3. **Técnica de esta imagen:** según "Qué técnica usa cada imagen" de `prompt.md`: la pedida para esta imagen, la del tipo en la Guía o la general (si es "Variada", con una tirada). Si piden una técnica que no está en el catálogo, escribe sus bloques como dice "Técnica propia" en `tecnicas.md`.
4. **Modelo:** el pedido para esta imagen; si no, el de la sección "Modelo de imagen" de la Guía, con su calidad; si tampoco, ninguno (Puter usa el suyo por defecto). Si la Guía no tiene esa sección, no hace falta añadirla.
5. **Primera imagen de este tipo:** si no existe la carpeta del tipo (`00_Sistema/02_Activos/<Carpeta>/`), créala con un `README.md` breve. Añade una fila a la tabla "Carpetas añadidas por skills" de la Guía de Organización: `| 00_Sistema/02_Activos/<Carpeta> | Imágenes de <tipo> (<Prefijo><Nota>.<ext>) | generar-imagen |`. Varias carpetas las comparten varios tipos (`Escenas`, `Lugares`…, según "Resumen por tipo" de `prompt.md`): si la carpeta ya existe pero es la primera imagen de este tipo en ella, añade el tipo a la descripción de su fila y a su README (`Imágenes de fenomeno y cultura (Fenomeno_…, Cultura_…)`). Las carpetas de la estructura inicial (como `Iconos`) no se registran en esa tabla, porque no las creó una skill: basta con añadir el tipo a su README.

## Paso 2: prompt
Arma el prompt según la sección del tipo en `prompt.md`:
- la capa del mundo: la técnica de esta imagen y la ambientación y la paleta de la Guía Visual, con los bloques tal cual;
- la capa de la entidad, desde su nota (con el fondo fundido con el papel si la técnica es 📄);
- el formato del tipo, al final.

## Paso 3: generar con Puter
1. Ejecuta el script con un tiempo límite de 10 minutos (la primera vez espera a que el usuario inicie sesión). El prompt va por la entrada estándar, en un heredoc con el delimitador entre comillas, para que pase tal cual con sus apóstrofes y comillas:
   ```bash
   node <directorio de esta skill>/scripts/generate_image.mjs --dest "<bóveda>/00_Sistema/02_Activos/<Carpeta>" --name <Prefijo><Nombre_de_la_nota> --aspect <proporción> --prompt-file - <<'PROMPT'
   <prompt>
   PROMPT
   ```
   - `--aspect` es la proporción del formato del tipo: `1:1`, `16:9` o `3:4` (columna Formato de "Resumen por tipo").
   - Añade `--model <id>` y `--quality <calidad>` si el Paso 1 dio un modelo.
   - Si el entorno no admite heredocs, escribe el prompt en un archivo temporal y pásalo con `--prompt-file <ruta>`.
2. El script imprime el nombre final, el tamaño, los píxeles y el modelo. Nunca sobrescribe: si ya existía un archivo con ese nombre, usa `_v2`, `_v3`… La extensión es la del formato real de la imagen (`.png`, `.jpg` o `.webp`).
3. Si avisa de que la proporción no coincide con la pedida, sigue: el modelo no tiene ese formato. Anótalo en las incidencias.
4. Si termina con error, actúa según su código de salida:
   - **3, filtro de contenido:** suaviza el prompt (más sugerido, menos explícito) y reintenta una vez.
   - **2, sin sesión** (el usuario no completó el inicio de sesión), **4, sin saldo**, **5, fallo del proveedor** (ya reintentó una vez) o **1, otro error:** ve a "Si algo falla".
5. **Mira la imagen** guardada (léela con la herramienta de lectura de archivos) para describirla en el informe. Si salió algo claramente distinto de lo pedido (otro sujeto, texto o marcos que el prompt prohíbe, varias figuras en un retrato), genera otra una sola vez con el prompt ajustado y enlaza la nueva. La anterior se conserva, como toda imagen, y se menciona en el informe.

## Paso 4: enlazar en la nota
- Propiedad `imagen: "[[<nombre final>]]"`, con su extensión real.
- Embed justo debajo del resumen en cita: `![[<nombre final>|300]]` para retratos y otras imágenes cuadradas, `![[<nombre final>|600]]` para las apaisadas. Sustituye al anterior si regeneras.
- En la sección Imagen, `**Prompt:**` con la fecha de generación, la técnica y el modelo (`2026-10-10 · técnica: Boceto en acuarela (acuarela) · modelo: el de Puter por defecto`) y, debajo, el prompt en un bloque de código, tal cual se generó. Así se puede reutilizar.
- Actualiza `ultima_revision` (sin comillas).

## Paso 5: informe
Si la invocó `crear-entidad` o `expandir-mundo`, devuélveles el nombre del archivo, la técnica y el modelo usados y las incidencias: la imagen sale en su informe final. Si se invocó sola, termina con:
- **Imagen:** enlace al archivo guardado, relativo al directorio de trabajo (`[Retrato_Aldric_Voss.png](World_Building/00_Sistema/02_Activos/Ilustraciones/Personajes/Retrato_Aldric_Voss.png)`), su tamaño y sus píxeles (los imprime `generate_image.mjs`), y una línea sobre lo que muestra.
- **Técnica:** cuál y por qué: pedida para esta imagen, la del tipo, la general o sorteada (con la tirada).
- **Modelo:** el pedido, el de la Guía o el de Puter por defecto.
- **Nota actualizada:** enlace a la nota y lo que cambió en ella: la propiedad `imagen`, el embed y el prompt en la sección Imagen.
- **Prompt usado**, en un bloque de código.
- **Versión:** si es una regeneración, qué versión es (`_v2`, `_v3`…) y que la anterior se conserva.
- **Incidencias**, si las hubo: inicio de sesión en Puter, reintentos, prompt suavizado, proporción distinta de la pedida o una segunda generación por no parecerse a lo pedido.
- **Guía Visual:** si se creó o cambió en esta ejecución, enlace a ella y la técnica elegida. Recuerda cuántas técnicas hay (están en la sección "Técnicas disponibles" de la Guía) y que se puede pedir otra para una imagen o fijar una por tipo.

## Si algo falla
Si Puter no puede generar la imagen (falta Node.js o la librería, no hay sesión ni saldo, o el proveedor falla tras el reintento):
- guarda el prompt en la sección Imagen de la nota;
- deja `imagen` vacío para generarla más tarde;
- explica al usuario qué pasó y cómo seguir: generarla más tarde con `/generar-imagen <nota>`, o con Gemini en su Chrome (`/generar-imagen <nota> navegador`).

Nunca dejes la nota a medias.

## Reglas
- No borres imágenes anteriores: una regeneración se guarda como `_v2`, `_v3`…
- **Credenciales:** el inicio de sesión en Puter (o en Google, en la alternativa) lo hace siempre el usuario en su navegador; nunca introduzcas credenciales. Nunca muestres el token de Puter ni lo copies a la bóveda o al repositorio.
- La skill es genérica: el estilo de cada mundo vive en su Guía Visual, nunca aquí. El catálogo de técnicas sí es de la skill: una técnica nueva se añade a `tecnicas.md` con su sección (bloques, Color, 📄 si es sobre papel) y en el índice, actualizando los totales del índice y el de la introducción de esta skill.
