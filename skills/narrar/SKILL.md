---
name: narrar
description: Escribe relatos, escenas, crónicas y documentos (cartas, diarios, sermones, canciones) ambientados en el mundo y coherentes con su canon. Los guarda en 90_Narrativa, una subcarpeta por forma. Antes de escribir reúne lo que necesita con las consultas, sin leer la bóveda, y comprueba fechas, lugares y quién vive en cada momento. Lo que inventa se queda en la narración, no usa los secretos salvo que se le pida y, al terminar, ofrece ilustrar el momento clave. Úsala para "escribe un relato…", "una escena en…", "la crónica de…", "una carta de…", "/narrar …".
---

# Narrar

Escribe narraciones ambientadas en el mundo: relatos, escenas, crónicas y documentos. Cuentan el mundo, no lo cambian: no son entidades, sus enlaces solo van a lo que ya tiene nota, y lo que inventan se queda en ellas.

Uso: `/narrar [forma] <idea>`, por ejemplo `/narrar escena la noche en que volvió el cometa, vista desde una taberna del puerto`.

## Las formas
| Forma | Qué es | Carpeta | Extensión habitual |
|---|---|---|---|
| `escena` | Un momento, sin una trama completa | `90_Narrativa/Escenas` | 400 a 800 palabras |
| `relato` | Una historia con principio, conflicto y final | `90_Narrativa/Relatos` | 1.500 a 3.000 |
| `cronica` | Hechos contados con la voz de un cronista del mundo, con su sesgo | `90_Narrativa/Cronicas` | 800 a 1.500 |
| `documento` | Un escrito del mundo tal cual: una carta, un diario, un informe, un sermón, una canción | `90_Narrativa/Documentos` | 200 a 800 |

Si el usuario no dice la forma, dedúcela de la idea («una carta» es un documento; «lo que pasó aquel invierno», un relato o una crónica). Si pide «corta» o «larga», ajusta la extensión. Pregunta solo lo imprescindible.

## Paso 1: preparar
```bash
python <directorio de esta skill>/scripts/narrative.py prepare <forma>
```
La primera vez crea `90_Narrativa`, con su README y su índice (`MOC_Narrativa`, enlazado desde `MOC_Inicio`); después, la subcarpeta de cada forma y la plantilla `Plantilla_Narracion`. Lo registra todo en la Guía de Organización. Dice en qué carpeta va la narración. Anota lo que creó, para el informe.

## Paso 2: el mundo que va a contar
Sin leer la bóveda, con las consultas de `consultar-mundo` (`<consultar-mundo>/scripts/query_world.py`) y de `crear-entidad`:
- **Lo que entra en la historia:** `query_world.py --about <Nombre>` de cada personaje, lugar o facción que aparezca, con `--no-secrets` salvo que el usuario pida usar secretos. Para un detalle (cómo es el lugar, su gente, sus costumbres), `--section <Nombre> <Sección>`.
- **El momento:** `query_world.py --timeline --from <año> --to <año>`, alrededor de cuando ocurre. Si hay viajes, `routes.py <A> <B>`: los días cuentan.
- **Las reglas:** la Ficha (tono, crudeza, vetos, temas, voz, tecnología, poderes, especies) y, de la Guía de Estilo y Tono, solo lo que haga falta.
- **Las fechas:** con los nombres del calendario de referencia, si existe. Si el calendario está por definir, fechas relativas («la segunda noche de la helada»), sin decidir el pilar.
- **Una serie:** `narrative.py list --serie <Serie>`. De la anterior (`sigue_a`) lee solo su resumen y sus Notas, no el texto entero.

Comprueba la coherencia antes de escribir: quién vive en ese momento, dónde está cada uno y qué sabe. Si la idea contradice el canon, o un borrador importante, avisa antes de escribir y propón cómo encajarla. El canon manda sobre el borrador.

## Paso 3: escribir
El archivo va en la carpeta de su forma, con la plantilla: nombre en ASCII y con `_`, y título con la ortografía real.
- **Frontmatter:**
  - `forma` y `estado: borrador`;
  - `cuando`, el año del eje en que transcurre, si se sabe, y `momento`, en palabras;
  - `donde`, `personajes` y `entidades`, solo con lo que ya tiene nota;
  - `voz`: quién cuenta;
  - `serie` y `sigue_a`, si continúa otra;
  - `usa_secretos`;
  - `imagen`, vacía.
- **Resumen:** dos o tres frases en cita bajo el título (quién, dónde y qué pasa). Sirve para seguir la serie sin releerla.
- **El texto,** según su forma:
  - **escena:** un momento, en presente o en pasado cercano, sin cerrarlo todo;
  - **relato:** una situación, un conflicto, un giro y un desenlace;
  - **crónica:** la voz de un cronista del mundo, con sus fechas, sus fuentes y su sesgo;
  - **documento:** el escrito tal cual, con su autor, su destinatario y su tono.
- **La voz:** la de la Ficha de base, y la de quien cuenta si es un cronista o un documento. Lo que se cree va como creencia y los rumores, como rumores.
- **Las reglas del mundo:** la tecnología, los poderes y sus límites (sus sistemas), las especies (no se inventan), el tono y la crudeza, nada vetado y nada del mundo real.
- **Enlaces:** solo a lo que ya tiene nota, la primera vez que se nombra (no cada vez: es una narración), y en sus propiedades.
- **Lo inventado** (un tabernero, una calle, un barco) va sin enlace y se lista en «Inventado aquí». Los nombres nuevos salen de los perfiles de nombres de su cultura (`<crear-entidad>/scripts/generate_names.py --profile <Cultura>`). Nada de hechos importantes nuevos, como una guerra, un reino o la muerte de un personaje con nota: si la historia los necesita, pregunta antes.
- **Secretos:** por defecto, la narración cuenta lo que se sabe o se cree. Usa un secreto solo si el usuario lo pide; entonces lleva `usa_secretos: true`, la etiqueta `secreto` (así queda fuera del «Grafo sin secretos») y, en sus Notas, «🔒 Usa la verdad de: [[Secreto]]».
- **Notas,** tras la raya:
  - Cuándo y dónde.
  - Del mundo: lo que usa, con sus enlaces.
  - Inventado aquí.
  - La voz: quién cuenta y con qué sesgo.
  - 🔒, si usa secretos.
- **Imagen:** siempre, la «Descripción visual» de su momento clave (de 4 a 6 elementos), por si se ilustra.

## Paso 4: comprobar
```bash
python <directorio de esta skill>/scripts/narrative.py check <Nota>
```
Comprueba:
- el frontmatter y la carpeta;
- que todo enlace lleve a una nota que existe (nada pendiente; un secreto, solo con `usa_secretos`);
- que sus personajes vivan y sus lugares existan en `cuando`;
- el resumen y las Notas.

También cuenta las palabras. Corrige los errores. Los avisos se miran uno por uno: un muerto que aparece como recuerdo, por ejemplo, vale.

## Paso 5: la ilustración
Pregunta con AskUserQuestion si la ilustras («Sí, con la técnica del mundo» / «No»). Si dice que sí, sigue `generar-imagen` con la narración: su tipo, `narracion`, va en `Ilustraciones/Escenas` con el prefijo `Narracion_`, y el prompt sale de su «Descripción visual».

## Paso 6: Bitácora e informe
- **Bitácora** (rehace también las Estadísticas, que cuentan las narraciones aparte):
  ```bash
  python <crear-entidad>/scripts/log_entry.py --title "Narración: <Título>" --line "<Forma>: [[<Nota>|<Título>]], <momento>, en <lugar>." --line "Del mundo: <lo que usa>." --line "Inventado: <n> (<lo principal>)."
  ```
- **Informe en el chat,** con los enlaces en Markdown y la ruta del archivo, nunca `[[...]]`:
  - la narración, con su forma y sus palabras;
  - lo del mundo que usa;
  - lo que inventó, ofreciendo crear como entidad lo que guste (`/crear-entidad <tipo> <idea>`);
  - si usa secretos;
  - los avisos de coherencia;
  - la imagen, si la hay;
  - la primera vez, lo que se creó: la carpeta, el índice y la plantilla.

## Reglas
- Solo escribe la narración, su estructura la primera vez y su imagen, si se pide. No toca las notas del mundo.
- El canon manda. Una narración no contradice a una nota en canon ni decide un pilar por definir.
- Lo inventado se queda en la narración. Solo entra en el mundo si el usuario lo crea como entidad.
- Los secretos, solo si el usuario lo pide.
- La skill es genérica: nada de un mundo concreto en sus textos ni en sus ejemplos.
