# Mapas

Los lugares que lo merecen (ruinas, mazmorras, edificios, asentamientos, parajes y regiones, según la regla `mapa` de su módulo) tienen, **además** de su imagen principal, un mapa. El mapa es la **leyenda numerada** de la sección `## Mapa` de la nota (ver `crear-entidad/referencias/mapas.md`); la imagen que dibuja esta skill es una **edición** de esa leyenda. El concept art sigue siendo obligatorio y la primera imagen de la nota: el mapa va después y en su propia sección.

## Qué edición toca
`python <crear-entidad>/scripts/map_key.py <Nota> --json` dice la clase del mapa, la edición, las zonas, las que faltan por cartografiar y si toca dibujar (`toca`):
- `primera`: aún no tiene mapa y la leyenda tiene las zonas mínimas;
- `nueva`: hay 3 zonas sin cartografiar o más, o un cuarto de las cartografiadas;
- nada: no toca. Si el usuario pide el mapa igualmente (`/generar-imagen <Nota> mapa`), se dibuja una edición nueva con lo que haya; si la nota no tiene leyenda, dilo y detente.

`niveles` dice qué niveles hay que dibujar: en una mazmorra de varios niveles, cada nivel es una imagen; en una edición nueva, solo los que tienen zonas sin cartografiar.

## Técnica de mapas
Los mapas de un mundo se ven todos igual, y casan con el resto de sus imágenes: misma ambientación y misma paleta de la Guía Visual, y una **técnica de mapas fija** en su sección `## Técnica de mapas`. Nunca «Variada» ni la técnica de un tipo: la de mapas vale para todos.
- Si la Guía no tiene esa sección, créala con la **técnica general** si es una técnica sobre papel (📄 en `tecnicas.md`), sin preguntar.
- Si la técnica general no es sobre papel (un óleo, un fotograma de cine, «Variada»), pregunta una sola vez cuál usar, **mostrando las 11 técnicas sobre papel** del catálogo (aunque el diálogo solo admita 4 opciones). Es una decisión del mundo, como la técnica general.

Formato de la sección en la Guía:
```markdown
## Técnica de mapas
<Nombre> (`<id>`)
`<bloque TÉCNICA>`
`<bloque ACABADO>`
```

## La plantilla del prompt
Se escribe en inglés y se arma con la leyenda y lo que la nota cuenta del lugar. Un prompt por nivel.
```
{APERTURA}. {TÉCNICA_MAPA}, on textured {SOPORTE} with no grid. {AMBIENTACIÓN}, {PALETA}. {FORMA}. Key features and layout, with north at the top: {ZONAS}. {CONEXIONES}. {MARCADORES}. {ACABADO}. No other text anywhere: no title, no labels, no names, no letters, no compass rose, no scale bar, no legend box. No grid, no border or frame, no watermark, no signature. {FORMATO}
```

| Campo | Fuente | Ejemplo |
|---|---|---|
| APERTURA | La clase del mapa (abajo) con lo que es el lugar, sin su nombre | `An overhead top-down 2D tabletop RPG map of a flooded crypt beneath a ruined chapel` |
| TÉCNICA_MAPA | El bloque TÉCNICA de la técnica de mapas | `loose watercolor sketch over a light pencil underdrawing, soft wet-on-wet color bleeds…` |
| SOPORTE | El de la técnica: `paper`, o `parchment` si la técnica lo es | `paper` |
| AMBIENTACIÓN, PALETA | Los bloques de la Guía Visual, tal cual (la paleta, según el Color de la técnica) | |
| FORMA | La forma del conjunto y lo que hay en sus bordes, de su descripción | `The crypt is carved into dark bedrock; the east edge is flooded; the north edge breaks into a natural cave` |
| ZONAS | Cada zona de la leyenda de este nivel, en orden: `{número} ({orientación}, {lo que es}): {lo que se ve}`. Lo que se ve sale de su línea y de lo que la nota cuenta de ella, concreto y sin nombres propios | `1 (south, entry): worn stone stairs descending from the surface into a pillared antechamber; 2 (center): a vaulted hall with a dry fountain and fallen statues` |
| CONEXIONES | Las conexiones de la leyenda, con su forma (un pasillo, una escalera, una calle, un camino). Las que llevan a otro nivel se dibujan como una escalera que baja o sube, sin el marcador del otro nivel. En un territorio, solo los caminos que se citan: «the other places have no road» | `Passages: 1 to 2 by a short stair; 2 to 3 and 2 to 5 by narrow corridors; 5 leads down a spiral stair to the lower level` |
| MARCADORES | La regla de los marcadores (abajo), con la lista exacta de números de este nivel | |
| ACABADO | El bloque ACABADO de la técnica de mapas | `airy, expressive sketchbook watercolor with loose unfinished edges` |
| FORMATO | Vertical u horizontal, para A4 (abajo) | `Vertical 3:4 portrait format, to be printed on an A4 sheet` |

### Apertura por clase
- **interior:** `An overhead top-down 2D tabletop RPG map of {lugar}, a plan of rooms, halls and passages seen from directly above`. Los muros, gruesos y legibles; el interior de cada sala, con sus objetos característicos dibujados desde arriba (mesas, camastros, barriles, pilares, escombros, agua).
- **urbano:** `An overhead top-down 2D map of {asentamiento}, a hand-drawn town plan seen from directly above, with streets, blocks of buildings, walls, gates and open spaces`. Los barrios, como manzanas de tejados con su carácter (ricos y ordenados, pobres y apiñados); los lugares notables, con su forma propia.
- **paraje:** `A top-down 2D map of {paraje}, the terrain seen from directly above, with hand-drawn relief, vegetation, paths and water`.
- **territorio:** `A top-down 2D hand-drawn regional map of {región}, with mountain ranges as inked ridges, forests as clusters of small trees, rivers, coasts, marshes and roads`. Los asentamientos, como pequeños grupos de edificios a su escala; las distancias, coherentes con lo que cuenta la nota (lo que está a dos jornadas, más lejos que lo que está a una).

### Los marcadores
Es lo que más falla: Gemini a veces repite o salta números. La regla va siempre, entera:
```
Exactly {N} circular map-key markers, one inside each zone listed above: bold hand-drawn black numerals in a solid black circle with an opaque white fill, large enough to read when printed on an A4 sheet, so they stand out clearly against the painted map. Use exactly these numbers, each one exactly once: {lista}. Do not repeat any number, do not skip any number, and add no other markers.
```
En una edición nueva o en un nivel, `{lista}` son los números de las zonas que van en esa imagen (por ejemplo `1, 2, 3, 4, 5, 6, 7, 8, 13`): los números son estables y una zona añadida después conserva el suyo.

### El formato
Que quepa en un A4 (1:1,41) aprovechando la hoja: **vertical 3:4** u **horizontal 4:3**, las proporciones estándar más cercanas, que impresas llenan el 94 % de la hoja.
- **Horizontal** si las zonas se reparten más de oeste a este que de norte a sur, o el lugar es alargado así (una costa, un valle, una muralla): `Horizontal 4:3 landscape format, to be printed on an A4 sheet`.
- **Vertical** en los demás casos: `Vertical 3:4 portrait format, to be printed on an A4 sheet`.

## Edición nueva: primero, editar la anterior
Para que el mapa no cambie de dibujo en cada edición, intenta primero **editar la edición anterior** en Gemini:
1. Adjunta la imagen de la edición anterior (de ese nivel) en el chat nuevo de Gemini, con la herramienta de subir archivos de Claude in Chrome. Si no puedes adjuntarla, ve directamente al punto 3.
2. Pide solo lo nuevo: `Edit this map. Keep the drawing exactly as it is: the same layout, style, colors and markers. Add only these new zones, each with a marker in the same style: {ZONAS nuevas}. {CONEXIONES nuevas}. Each number appears exactly once in the whole map; no other text.`
3. Si no se pudo adjuntar, o el resultado cambió el dibujo o desordenó los marcadores y no se arregla con una corrección, **redibuja** con el prompt completo de todas las zonas del nivel.

## Comprobación
Sigue la comprobación de `SKILL.md` (Paso 3c). En un mapa, además:
- **Marcadores:** lee los números que se ven y compáralos con la lista: los que faltan, los repetidos y los que sobran. Es obligatorio que estén todos, una vez cada uno.
- **Texto:** ni títulos, ni nombres, ni letras sueltas, ni cuadrícula, ni marco.
- **Zonas:** lo característico de cada una (el trono, el pozo, las rejas) y su sitio aproximado según su orientación, con el norte arriba.
- **Estilo:** el de la técnica de mapas, y que case con el concept art del mundo.
- **Formato:** vertical u horizontal, el pedido.

Correcciones, en el mismo chat y nombrando el problema exacto:
- `In this map the number 4 appears twice. Keep the one in the kitchen (south-west) and change the one in the library (east) to 10. Change nothing else.`
- `Marker 7 is missing: add it inside the laboratory, west of marker 6, in the same style. Change nothing else.`
- `Remove the title text at the top. Change nothing else.`

## Guardar y enlazar
- **Carpeta:** `00_Sistema/02_Activos/Mapas`. La primera vez, créala con su `README.md` y regístrala en la tabla «Carpetas añadidas por skills» de la Guía de Organización: `| 00_Sistema/02_Activos/Mapas | Mapas de los lugares (Mapa_<Nota>.<ext>, Mapa_<Nota>_Nivel_<n>.<ext>) | generar-imagen |`.
- **Nombre:** `Mapa_<Nota>`, y en una mazmorra de varios niveles, `Mapa_<Nota>_Nivel_<n>` desde el nivel 2. Una edición nueva no sobrescribe: `fetch_download.py` le pone `_v2`, `_v3`…, y las anteriores se conservan.
- **En la nota:**
  - `mapa`: la lista de imágenes de la edición vigente, una por nivel y en orden (`- "[[Mapa_Cripta_Honda.jpg]]"`). En una edición nueva, cambia solo las de los niveles redibujados.
  - En la sección `## Mapa`, encima de la leyenda: el mapa embebido (`![[Mapa_Cripta_Honda.jpg|600]]`; con varios niveles, cada uno tras su título `**Nivel 2**`) y la línea de la edición: `*Edición 1 · 2026-10-12 · técnica: Boceto en acuarela · comprobado: 9/9 marcadores, sin repetidos*`. Sustituyen a los de la edición anterior.
  - En la sección Imagen, después del prompt del concept art: `**Prompt del mapa:**` con la fecha, la técnica y la edición (y el nivel), y el prompt en un bloque de código, tal cual se generó (sin la orden `Generate an image:`). Sustituye al de la edición anterior.
  - Al final, `python <crear-entidad>/scripts/map_key.py <Nota> --charted`: suma la edición, pone `mapa_zonas` en el último número y quita las marcas «sin cartografiar».
