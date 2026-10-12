# Ambientación y Guía Visual

Cada mundo tiene **una** Guía Visual en `00_Sistema/04_Convenciones/Guia_Visual.md`, compartida por todas sus imágenes. Tiene dos capas independientes:
- **Ambientación**, que la marca el mundo: género, época, tono, materiales, el elemento visual que lo identifica y la paleta. Sale de la Ficha y es igual en todas las imágenes: por eso el mundo se ve coherente.
- **Técnica**, que la elige el usuario: cómo está hecha la imagen (óleo, acuarela, cómic, lápiz…). El catálogo está en `tecnicas.md`. Hay una técnica general, opcionalmente una por tipo, y cada imagen puede pedir otra.

## Cómo crear la Guía Visual
1. Lee de la Ficha el género, el tono, la tecnología, la premisa y el conflicto central.
2. **Ambientación:** parte del preset de género más cercano de abajo y **personalízalo** con lo que hace único al mundo: el elemento omnipresente (un sol rojo, nieve perpetua, un cielo sin estrellas), los materiales típicos, el estado del mundo (ruinas, abundancia, decadencia).
3. **Paleta:** de 3 a 5 colores dominantes y la luz típica, en inglés.
4. **Técnica:** la elige el usuario. Es la única pregunta del flujo y se hace una sola vez por mundo. AskUserQuestion admite como mucho 4 opciones: si el usuario solo ve esas, creerá que no hay más. Por eso el catálogo completo tiene que estar a la vista **en el mensaje y dentro del diálogo**:
   1. En el mensaje que acompaña a la pregunta, muestra el índice de `tecnicas.md` tal cual, con el total.
   2. Pregunta con AskUserQuestion:
      - **Pregunta,** con el total y cómo elegir otra: `¿Con qué técnica hacemos las imágenes de <Mundo>? Hay <total> (lista completa en la vista previa de cada opción); estas tres son las que mejor encajan. Para otra, escribe su nombre en «Other».`
      - **Opciones:** las tres técnicas de "Recomendadas por género" que mejor encajen con el género y el tono (la más adecuada primero, con "(Recomendado)") y **"Variada"** (cada imagen sortea su técnica entre varias que encajen con el mundo). La descripción de cada una dice qué aspecto tiene.
      - **Vista previa** (`preview`) de cada opción: dos líneas sobre su aspecto y, debajo, el índice completo. Así la lista se ve dentro del propio diálogo.
      - Con «Other», el usuario puede escribir cualquier técnica del catálogo (nombre o id), varias (es una "Variada" con esa lista) o describir una propia.
   3. Si elige "Variada" sin decir cuáles, elige tú de 3 a 5 técnicas del catálogo que encajen con el mundo.
5. Escribe la Guía con la plantilla de abajo y sigue con la imagen, sin más preguntas. El usuario puede editarla cuando quiera (por ejemplo, para añadir técnicas por tipo).

## Ambientación por género
La ambientación describe **qué** se ve, no **cómo** está pintado: nada de técnicas, soportes ni pinceladas, que pone la técnica.

| Género | AMBIENTACIÓN (base) | Referencias de juego (solo para `rpg_clasico`) | Fondos típicos |
|---|---|---|---|
| Fantasía oscura | `dark medieval fantasy world, grim and weathered, worn leather, rusted steel and ancient stone` | `Baldur's Gate 2 and Icewind Dale` | `temple, ancient dungeon, misty forest, medieval tavern` |
| Fantasía épica | `high fantasy world, heroic and wondrous, ornate armor, elegant craftsmanship, majestic vistas` | `Dragon Age and Pillars of Eternity` | `castle hall, mountain pass, elven grove` |
| Fantasía ligera | `whimsical fairy-tale world, cozy villages, enchanted woods, gentle magic` | `Ni no Kuni and Dragon Quest` | `cottage interior, flower meadow, village square` |
| Ciencia ficción | `gritty far-future science fiction world, utilitarian starship technology, worn armor plating` | `Mass Effect and Rogue Trader` | `spaceship interior, industrial space dock` |
| Cyberpunk | `cyberpunk near-future city, neon signage glow, chrome implants, rain and grime` | `Shadowrun and Cyberpunk 2077` | `rain-slicked neon alley, high-tech hideout` |
| Post-apocalíptico | `post-apocalyptic wasteland, scavenged gear, rust, dust and ruin` | `Fallout 2 and Wasteland` | `junkyard, desert outpost, ruined bunker` |
| Horror | `gothic horror world, oppressive shadows, decay, candlelight and dread` | `Darkest Dungeon and Bloodborne` | `crumbling manor, foggy graveyard, candlelit crypt` |
| Steampunk | `Victorian steampunk world, brass gears, steam pipes, gaslight and soot` | `Arcanum and Dishonored` | `brass workshop, airship deck, gaslit street` |
| Histórico | `historically grounded world, period-accurate clothing, tools and architecture` | `Pentiment and Kingdom Come` | `scriptorium, market square, war camp` |

**Ejemplo personalizado** (fantasía oscura bajo un sol moribundo): `dark medieval fantasy world under a dying red sun, grim and weathered, rusted iron and cracked stone, long crimson shadows over everything`.

## Cómo se arma el estilo de cada prompt
`prompt.md` usa: ESTILO = `{TÉCNICA}. {AMBIENTACIÓN}`, más la paleta según el Color de la técnica:
- `mundo`: `, {PALETA}`;
- `acento`: `, monochrome with a single {un color de la paleta} accent`;
- `monocromo`: nada.

El ACABADO es el de la técnica, y las RESTRICCIONES son las de la Guía más las extra de la técnica.

## Plantilla de la Guía Visual
```markdown
# Guía Visual — <Mundo>

Estilo compartido por todas las imágenes del mundo. La skill `generar-imagen` copia los bloques en inglés tal cual en cada prompt.
- La **ambientación** y la **paleta** las marca el mundo: son iguales en todas las imágenes.
- La **técnica** se puede cambiar: para todo el mundo aquí, por tipo en "Técnica por tipo", o para una sola imagen al pedirla (`/generar-imagen <Nota> acuarela`). Todas las que hay están abajo, en "Técnicas disponibles".

## Técnica
<Nombre> (`<id>`)
`<bloque TÉCNICA en inglés>`

## Acabado
`<bloque ACABADO de la técnica>`

## Ambientación
`<bloque AMBIENTACIÓN en inglés>`

## Paleta
`<paleta en inglés>`

<En español: colores dominantes, luz típica y el elemento visual que identifica al mundo.>

## Restricciones
`No text, no watermark, no border, no signature`

## Técnica por tipo
Opcional: un tipo que figure aquí usa su técnica en lugar de la general.

| Tipo | Técnica |
|---|---|

## Técnica de mapas
<La de todos los mapas del mundo: la general si es sobre papel; si no, una técnica sobre papel elegida por el usuario. Se rellena con el primer mapa (ver `mapas.md`).>

## Fondos habituales
<Lista en inglés de fondos coherentes con el mundo, para el campo FONDO.>

## Técnicas disponibles
<El índice de `tecnicas.md`, tal cual: la línea del total y la lista, sin bloque de código.>

Es el catálogo de la skill cuando se creó esta guía; `/generar-imagen tecnicas` muestra el actual.
```
- **Técnica "Variada":** la sección Técnica dice `Variada: <id>, <id>, <id>` y no lleva bloque; tampoco la sección Acabado. Los bloques salen de `tecnicas.md` en cada sorteo.
- **Técnica propia:** sus bloques los escribe Claude (ver "Técnica propia" en `tecnicas.md`) y van tal cual en la Guía.
- Para `rpg_clasico`, rellena `{GENERO}` y `{REFERENCIAS}` con el género y las referencias de juego de la tabla de arriba.

## Guías de la versión anterior
Si la Guía no tiene sección "Técnica" (formato anterior, con un único bloque "Estilo" que mezcla la técnica y la ambientación):
- úsala tal cual: su Estilo hace de TÉCNICA y AMBIENTACIÓN a la vez, con la paleta incluida;
- si se pide otra técnica para una imagen, quita del Estilo lo que describe la técnica ("digital painting…", "reminiscent of…", "RPG art style") y usa el resto como ambientación;
- si el usuario quiere técnicas variadas o por tipo, propón pasar la Guía al formato nuevo conservando su ambientación y su paleta.

Si la Guía no tiene la sección "Técnicas disponibles", añádela al final la próxima vez que generes una imagen: es la única parte que se añade sin pedirlo, porque solo informa.
