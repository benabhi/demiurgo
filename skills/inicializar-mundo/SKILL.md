---
name: inicializar-mundo
description: Inicializa una bóveda de Obsidian para worldbuilding de cualquier género. Entrevista al usuario sobre los pilares del mundo (premisa, género, alcance (una ciudad, una región, un mundo o varios), tono, poderes, tecnología, reglas de rol, autonomía de Claude…) y lo que ya tiene nombre propio, y crea la estructura neutral de carpetas con README, las guías de convenciones, los MOCs automáticos (Obsidian Bases), la Ficha del Mundo y un CLAUDE.md con reglas derivadas de las respuestas. Úsala al empezar un mundo nuevo o para completar la estructura de uno existente. No crea plantillas ni contenido de lore.
---

# Inicializar mundo

Crea la base de una bóveda de worldbuilding a partir de una entrevista. **Idempotente:** el script solo crea lo que falta y nunca sobrescribe.

## Archivos de la skill
- `assets/cuestionario.json`: banco de preguntas por rondas, con las opciones y la regla que cada respuesta aporta a `CLAUDE.md`.
- `assets/estructura.json`: carpetas, títulos y textos de cada `README.md`.
- `assets/convenciones/` y `assets/CLAUDE.md.tpl`: guías y plantilla de `CLAUDE.md`, con placeholders `{{...}}`.
- `assets/respuestas_ejemplo.json`: ejemplo del formato de respuestas.
- `scripts/init_world.py`: genera todo a partir de las respuestas.

## Paso 0: situación de partida
1. La bóveda es por defecto `World_Building/` en la raíz del proyecto; confírmalo si no es evidente.
2. Si ya existe `<bóveda>/00_Sistema/Ficha_del_Mundo.md`, **no repitas la entrevista**: reconstruye `respuestas.json` a partir de la Ficha (frontmatter y cuerpo) y ve al paso 5. Solo se crearán los archivos que falten. Una Ficha anterior con `escala: local` se reconstruye como `ciudad` o `region`, según su foco.
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
  - **Añade al final la opción "Decide tú"** (textos en `opcion_decidir`) a toda pregunta, salvo las que tienen `permite_decidir: false`: el propósito y el sistema de rol, que son decisiones del usuario y no del mundo, y la escala, cuyas cuatro opciones no le dejan sitio (si quiere que decidas tú, lo escribe en «Other»).
- Omite las preguntas cuya `condicion` no se cumpla (por ejemplo, el sistema de rol solo se pregunta si el propósito incluye rol).
- Toda pregunta admite "por definir"; no insistas. La ronda 5 es opcional entera.
- Fuera de "Decide tú", no inventes respuestas ni completes huecos por tu cuenta.

### Decide tú
Cuando el usuario elige "Decide tú", escribe "decide tú" en una pregunta de texto o eligió un modo que delega:
- Elige el valor **más coherente con lo ya respondido** (premisa, género, tono, conflicto…), no el más genérico.
- En las preguntas de opciones, elige una de las opciones existentes. En las de texto, escribe una respuesta concreta y breve.
- Si nada lo orienta, en lugar de lo más genérico prefiere lo que dé más juego al conflicto central.
- En el resumen de confirmación, marca cada una de esas respuestas con "(elegido por Claude)".

### El alcance
La escala dice qué abarca el mundo, y con el foco decide dónde se crea todo:
- **`ciudad`** o **`region`:** el mundo es su foco (una ciudad, o un sitio como una estación, un barco o una mazmorra; un valle, una isla, un reino). Todo se crea dentro de él. Lo de fuera (la ciudad vecina, el reino al que pertenece) se enlaza como referencia con el tipo `fuera` y el motor no lo crea. En un mundo que es una ciudad, sus barrios son asentamientos de categoría `barrio`.
- **`mundial`** o **`multiple`:** el foco es la zona por la que se empieza, y el mundo crece desde ella.

Por eso, en una escala `ciudad` o `region`, el foco tiene que nombrar ese lugar (con su nombre, si lo tiene).

### Lo que ya tiene nombre
La última ronda recoge lo que el usuario ya tiene con nombre propio. Con su respuesta y con lo que nombró en las demás (el foco, el conflicto, la premisa):
- Identifica cada entidad con nombre propio y dale el tipo del módulo de `crear-entidad` que la crearía (los de su carpeta `tipos/`): una ciudad o un barrio es un `asentamiento`; un reino, un valle o un continente, una `region`; un dios, una `deidad`; un pueblo, una `cultura`; una orden o un gremio, una `faccion`; un hecho, un `evento`. Un término sin entidad detrás (un título, un oficio) no va aquí: irá al Glosario cuando se use.
- **El alcance manda:** en una escala `ciudad` o `region`, el foco es todo el mundo y va el primero, con su tipo (`asentamiento` o `region`), si tiene nombre. En una `mundial`, añade lo más alto del mapa (el continente o el mundo entero, con el nombre del mundo si el usuario no le da otro) como `region`: así cada región cuelga de algo y el mapa del mundo tiene qué dibujar.
- En «Solo lo esencial» o «Decide tú todo», no inventes nombres para esta ronda: solo el foco y lo más alto del mapa, como arriba.
- Cada uno, con una línea de qué es, tomada de lo que dijo el usuario.

Así la Ficha nace con esos nombres como enlaces pendientes con su tipo, y el motor empieza por ellos (canon de base).

## Paso 3: confirmación
Muestra un resumen compacto (una línea por pregunta, marcando las elegidas por Claude) y pide confirmación. Lo que ya tiene nombre va en lista, cada nombre con su tipo y su línea. Corrige lo que el usuario indique.

## Paso 4: respuestas.json
Escribe el archivo en un directorio temporal (el scratchpad, si existe):
```json
{"nombre": "...", "respuestas": {"premisa": "texto", "tono": "oscuro", "proposito": ["worldbuilding", "rol"], "poderes": {"texto": "respuesta libre", "regla": "regla breve para CLAUDE.md"}}}
```
- **Pregunta de opciones:** usa el `valor` de la opción (una lista si es `multiple`).
- **Respuesta propia en una pregunta de opciones** ("Other"): un objeto con `texto`. Añade `regla` (una frase imperativa) si la pregunta no trae su propia `regla` con `{valor}`.
- **Por definir:** omite la clave.
- **Año actual:** un número como texto (`"312"`); el script lo guarda como número en la Ficha.
- **Lo que ya tiene nombre:** una lista, `"nombrados": [{"nombre": "Vel", "tipo": "asentamiento", "que_es": "la ciudad portuaria donde empieza todo"}]`, con el nombre en su ortografía real (el script hace el enlace, en ASCII y con `_`). Sin la clave si no hay nada.

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
- **Bitácora:** el script la crea (`00_Sistema/Bitacora.md`) con la entrada de la creación del mundo; desde ahí, cada skill anota en ella lo que crea. Enlázala.
- **Estadísticas:** el script crea `00_Sistema/Estadisticas.md`, enlazada desde `MOC_Inicio`: cuánto hay en el mundo y qué falta. La rehacen las skills al terminar cada tarea. Enlázala.
- **Grafo:** el script deja configurado el grafo de Obsidian (`.obsidian/graph.json`): cada tipo de entidad con su color, los nombres visibles desde más lejos al alejar el zoom y sin las notas del sistema, los README ni los MOC, que enredan el grafo. Los enlaces pendientes salen en gris. Las flechas no se activan, porque ensucian el grafo: quien las quiera, las enciende a mano. Deja también dos marcadores de grafo (panel Marcadores): «Grafo sin secretos», para enseñar el mundo sin spoilers, y «Grafo completo», para volver a verlo todo; abrir uno cambia el filtro, los colores y lo que se muestra. En un mundo creado antes, o cuando lleguen tipos nuevos, lo hace `crear-entidad/scripts/graph_colors.py`, sin un grafo abierto en Obsidian: uno abierto vuelve a guardar el suyo encima a los pocos segundos (si pasa, el marcador «Grafo completo» aplica la configuración entera).
- **Pilares:** una tabla breve pilar → respuesta, marcando "(elegido por Claude)" lo que decidiste tú.
- **Alcance:** qué abarca el mundo y dónde empieza. Si es una ciudad o una región, que todo se creará dentro, y que lo de fuera se nombra sin crearse.
- **Lo que ya tiene nombre:** cuántos y cuáles, enlazados desde la Ficha como enlaces pendientes con su tipo (en el registro de enlaces pendientes, que el script crea y enlaza desde `MOC_Inicio`): el motor empieza por ellos. Los que quedaron sin tipo, si los hubo.
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
