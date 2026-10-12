---
name: inicializar-mundo
description: Inicializa una bóveda de Obsidian para worldbuilding de cualquier género. Entrevista al usuario sobre los pilares del mundo (premisa, género, tono, poderes, tecnología, reglas de rol, autonomía de Claude…) y crea la estructura neutral de carpetas con README, las guías de convenciones, los MOCs automáticos (Obsidian Bases), la Ficha del Mundo y un CLAUDE.md con reglas derivadas de las respuestas. Úsala al empezar un mundo nuevo o para completar la estructura de uno existente. No crea plantillas ni contenido de lore.
---

# Inicializar mundo

Crea la base de una bóveda de worldbuilding a partir de una entrevista. **Idempotente:** el script solo crea lo que falta y nunca sobrescribe.

## Progreso visible
Quien usa la skill tiene que ver en todo momento por qué paso va y qué estás haciendo, sin abrir tus pensamientos. Es igual en todas las skills de este sistema.
1. **Lista de etapas.** Al empezar, crea una lista de tareas con la herramienta de tareas de Claude Code (TodoWrite o, en versiones nuevas, TaskCreate y TaskUpdate), con una tarea por etapa de las de abajo. Claude Code la muestra con casillas y anima la etapa en curso. Pon cada etapa en curso al empezarla y complétala al terminarla; nunca hay más de una en curso. Si no tienes esa herramienta, escribe la lista en el chat con `○` (pendiente), `▸` (en curso) y `✓` (hecha).
2. **Una línea al empezar cada etapa,** en el chat: `**▸ 3/8 · <Etapa>** — <qué haces, en concreto>`. Al cerrar una etapa que produce algo, otra línea: `✓ <resultado>` (la nota creada, la imagen guardada, los errores corregidos). Una o dos líneas, nunca párrafos.
3. **Herramientas con descripción:** cada llamada lleva una descripción breve, en el idioma de la conversación, de lo que hace para el usuario («Buscar duplicados de “<nombre>”»), no el comando.
4. **Si otra skill te invoca,** no crees una lista nueva: añade tus etapas a la suya, justo después de la etapa que te invocó, con `↳ ` delante del nombre (`↳ Imagen: armar el prompt`). Esa etapa sigue en curso hasta que termines.
5. **Esperas:** si te toca esperar algo largo (una generación, al usuario), dilo en una línea antes: `⏳ <qué esperas>`.

Etapas de esta skill (7):
1. Situación de partida (Paso 0)
2. Modo de entrevista (Paso 1)
3. Entrevista (Paso 2)
4. Confirmación (Paso 3)
5. Respuestas (Paso 4)
6. Generar la bóveda (Paso 5)
7. Informe (Paso 6)

En la entrevista, di en una línea qué bloque de preguntas empieza y cuántos quedan.

## Archivos de la skill
- `assets/cuestionario.json`: banco de preguntas por rondas, con las opciones y la regla que cada respuesta aporta a `CLAUDE.md`.
- `assets/estructura.json`: carpetas, títulos y textos de cada `README.md`.
- `assets/convenciones/` y `assets/CLAUDE.md.tpl`: guías y plantilla de `CLAUDE.md`, con placeholders `{{...}}`.
- `assets/respuestas_ejemplo.json`: ejemplo del formato de respuestas.
- `scripts/init_world.py`: genera todo a partir de las respuestas.

## Paso 0: situación de partida
1. La bóveda es por defecto `World_Building/` en la raíz del proyecto; confírmalo si no es evidente.
2. Si ya existe `<bóveda>/00_Sistema/Ficha_del_Mundo.md`, **no repitas la entrevista**: reconstruye `respuestas.json` a partir de la Ficha (frontmatter y cuerpo) y ve al paso 5. Solo se crearán los archivos que falten.
3. Pregunta si hay material previo del mundo (documentos, notas). Si lo hay, léelo, deduce las respuestas que puedas y en la entrevista confirma lo deducido y pregunta solo lo que falte.

## Paso 1: modo de entrevista
Antes de las rondas, pregunta con AskUserQuestion cómo quiere hacerla:
- **"Respondo yo" (Recomendado):** la entrevista completa, ronda por ronda.
- **"Solo lo esencial":** el usuario responde la ronda 1 (identidad) y Claude decide el resto.
- **"Decide tú todo":** el usuario da, si quiere, una idea en una frase, y Claude inventa todas las respuestas.

En los dos últimos modos, Claude decide como se explica en "Decide tú", más abajo.

## Paso 2: entrevista
Lee `assets/cuestionario.json` y pregunta ronda por ronda, en orden:
- **Rondas `modo: "texto"`:** un solo mensaje con la `intro` y las preguntas numeradas, cada una con su `ejemplo`. Espera la respuesta libre.
- **Rondas `modo: "opciones"`:** una sola llamada a AskUserQuestion con las preguntas de la ronda.
  - Usa `encabezado` como header, y `etiqueta` y `descripcion` en cada opción.
  - Activa multiSelect si `formato` es `multiple`.
  - Si una opción tiene `recomendada: true`, ponla primera y añade "(Recomendado)" a su etiqueta.
  - **Añade al final la opción "Decide tú"** (textos en `opcion_decidir`) a toda pregunta, salvo las que tienen `permite_decidir: false` (propósito y sistema de rol: son decisiones del usuario, no del mundo).
- Omite las preguntas cuya `condicion` no se cumpla (por ejemplo, el sistema de rol solo se pregunta si el propósito incluye rol).
- Toda pregunta admite "por definir"; no insistas. La ronda 5 es opcional entera.
- Fuera de "Decide tú", no inventes respuestas ni completes huecos por tu cuenta.

### Decide tú
Cuando el usuario elige "Decide tú", escribe "decide tú" en una pregunta de texto o eligió un modo que delega:
- Elige el valor **más coherente con lo ya respondido** (premisa, género, tono, conflicto…), no el más genérico.
- En las preguntas de opciones, elige una de las opciones existentes. En las de texto, escribe una respuesta concreta y breve.
- Si nada lo orienta, en lugar de lo más genérico prefiere lo que dé más juego al conflicto central.
- En el resumen de confirmación, marca cada una de esas respuestas con "(elegido por Claude)".

## Paso 3: confirmación
Muestra un resumen compacto (una línea por pregunta, marcando las elegidas por Claude) y pide confirmación. Corrige lo que el usuario indique.

## Paso 4: respuestas.json
Escribe el archivo en un directorio temporal (el scratchpad, si existe):
```json
{"nombre": "...", "respuestas": {"premisa": "texto", "tono": "oscuro", "proposito": ["worldbuilding", "rol"], "poderes": {"texto": "respuesta libre", "regla": "regla breve para CLAUDE.md"}}}
```
- **Pregunta de opciones:** usa el `valor` de la opción (una lista si es `multiple`).
- **Respuesta propia en una pregunta de opciones** ("Other"): un objeto con `texto`. Añade `regla` (una frase imperativa) si la pregunta no trae su propia `regla` con `{valor}`.
- **Por definir:** omite la clave.
- **Año actual:** un número como texto (`"312"`); el script lo guarda como número en la Ficha.

## Paso 5: generar
Desde la raíz del proyecto:
```bash
python <directorio de esta skill>/scripts/init_world.py --answers <ruta>/respuestas.json
```
Opciones: `--root` (por defecto, el directorio actual), `--vault` (por defecto, `World_Building`) y `--verbose` (lista cada archivo). Si el script muestra líneas `AVISO`, revísalas antes de cerrar.

## Paso 6: informe final
El usuario tiene que ver con claridad qué se creó. Con la salida del script y las respuestas, muestra, con enlaces relativos al directorio de trabajo que se abren con un clic (`[Ficha del Mundo](World_Building/00_Sistema/Ficha_del_Mundo.md)`):
- **Mundo:** nombre y premisa en una línea, con enlace a la Ficha del Mundo.
- **Estructura:** cuántos archivos y carpetas se crearon y cuántos ya existían (sin tocar), con enlaces a `MOC_Inicio`, la Guía de Organización y `CLAUDE.md`.
- **Pilares:** una tabla breve pilar → respuesta, marcando "(elegido por Claude)" lo que decidiste tú.
- **Reglas de `CLAUDE.md`:** cuántas se añadieron y las que más pesan (contenido, tono, poderes, sistema de rol).
- **Por definir:** los pilares que quedaron en `Preguntas_Abiertas`, con enlace.
- **Avisos** del script, si los hubo.
- **Siguientes pasos:**
  - activar el plugin principal "Bases" de Obsidian (los MOCs lo usan);
  - las plantillas y el contenido se crean con otras skills, que se registran en la tabla "Tipos registrados" de la Guía de Organización: la primera entidad con `/crear-entidad`, o generar con `/expandir-mundo` a partir del foco inicial.

## Reglas
- La skill es genérica: nada de contenido de un mundo concreto en `assets/`, solo placeholders.
- Para cambiar carpetas, edita `assets/estructura.json`; para cambiar preguntas o reglas, `assets/cuestionario.json`. El script no se toca para eso.
- Si cambias el cuestionario, mantén los límites de AskUserQuestion: máximo 4 preguntas por ronda de opciones, 4 opciones por pregunta y un encabezado de 12 caracteres. El script avisa si no se cumplen.
