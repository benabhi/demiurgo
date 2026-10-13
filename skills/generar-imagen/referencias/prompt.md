# Prompt dinámico por tipo

El prompt se escribe **en inglés** (los modelos de imagen lo entienden mejor) y se arma en dos capas:
- **Capa del mundo**, de la Guía Visual (`00_Sistema/04_Convenciones/Guia_Visual.md`), con los bloques copiados tal cual:
  - ESTILO = `{TÉCNICA}. {AMBIENTACIÓN}`, más la paleta según el Color de la técnica (`estilos.md`, "Cómo se arma el estilo de cada prompt");
  - ACABADO, el de la técnica;
  - RESTRICCIONES, las de la Guía más las extra de la técnica.
- **Capa de la entidad**: lo que muestra la imagen según su tipo, sacado de su nota.

## Qué técnica usa cada imagen
Por orden de prioridad:
1. La que pidió el usuario para esta imagen (un id de `tecnicas.md`, su nombre o una descripción propia).
2. La del tipo de la entidad en la tabla "Técnica por tipo" de la Guía.
3. La técnica general de la Guía. Si es **"Variada"**, sortéala: `python <crear-entidad>/scripts/roll_dice.py 1d<N>`, con N el número de técnicas de la lista, y usa la que ocupa esa posición.

Los bloques TÉCNICA y ACABADO salen de la Guía si la técnica es la general; si no, de `tecnicas.md`.

## Resumen por tipo
Cada tipo define lo que muestra, el formato, la carpeta (dentro de `00_Sistema/02_Activos/`) y el prefijo del archivo.

| Tipo | Muestra | Formato | Carpeta | Prefijo |
|---|---|---|---|---|
| personaje | retrato de cabeza y hombros | `Square 1:1 format` | `Ilustraciones/Personajes` | `Retrato_` |
| region | paisaje panorámico | `Wide 16:9 landscape format` | `Ilustraciones/Lugares` | `Paisaje_` |
| ecosistema | paisaje del bioma, con su vida | `Wide 16:9 landscape format` | `Ilustraciones/Lugares` | `Ecosistema_` |
| asentamiento | plano general desde el camino de llegada | `Wide 16:9 landscape format` | `Ilustraciones/Lugares` | `Asentamiento_` |
| lugar | su vista más emblemática, por fuera o por dentro | `Wide 16:9 landscape format` | `Ilustraciones/Lugares` | `Lugar_` |
| ruta | vista a lo largo de la ruta en su tramo más reconocible, con sus viajeros | `Wide 16:9 landscape format` | `Ilustraciones/Lugares` | `Ruta_` |
| fenomeno | plano atmosférico del fenómeno sobre el paisaje | `Wide 16:9 landscape format` | `Ilustraciones/Escenas` | `Fenomeno_` |
| especie | figura de cuerpo entero de un miembro típico | `Vertical 3:4 portrait format` | `Ilustraciones/Seres` | `Especie_` |
| deidad | figura de cuerpo entero tal como la imaginan sus fieles | `Vertical 3:4 portrait format` | `Ilustraciones/Personajes` | `Deidad_` |
| cultura | tres miembros con su atuendo tradicional, en plano medio | `Wide 16:9 landscape format` | `Ilustraciones/Escenas` | `Cultura_` |
| idioma | muestra caligráfica de su escritura | `Square 1:1 format` | `Iconos` | `Escritura_` |
| objeto | el objeto solo, centrado | `Square 1:1 format` | `Ilustraciones/Objetos` | `Objeto_` |
| calendario | rueda del calendario con sus meses y estaciones | `Square 1:1 format` | `Iconos` | `Calendario_` |
| faccion | su emblema o su estandarte | `Square 1:1 format` | `Iconos` | `Emblema_` |
| linaje | su blasón o su marca de familia | `Square 1:1 format` | `Iconos` | `Blason_` |
| afeccion | lámina de estudio de sus señales, sin nada gráfico | `Square 1:1 format` | `Laminas` | `Afeccion_` |
| material | lámina de espécimen: el material en bruto y trabajado | `Square 1:1 format` | `Laminas` | `Material_` |
| flora | lámina botánica: la planta entera y sus partes | `Square 1:1 format` | `Laminas` | `Flora_` |
| criatura | cuerpo entero en su hábitat, en su pose característica | `Wide 16:9 landscape format` | `Ilustraciones/Seres` | `Criatura_` |
| sistema | el poder, la técnica o la ley en uso, con su efecto y su precio | `Wide 16:9 landscape format` | `Ilustraciones/Escenas` | `Sistema_` |
| mito | la escena clave del relato, tal como la imaginan quienes lo cuentan | `Wide 16:9 landscape format` | `Ilustraciones/Escenas` | `Mito_` |
| costumbre | la costumbre en plena práctica, en su momento más reconocible | `Wide 16:9 landscape format` | `Ilustraciones/Escenas` | `Costumbre_` |
| obra | la obra misma o su interpretación (el mural, la estatua; la canción cantada, el libro abierto) | `Wide 16:9 landscape format` | `Ilustraciones/Escenas` | `Obra_` |
| creencia | su símbolo sagrado | `Square 1:1 format` | `Iconos` | `Simbolo_` |
| era | escena alegórica de la era | `Wide 16:9 landscape format` | `Ilustraciones/Escenas` | `Era_` |
| evento | escena dramática del momento clave | `Wide 16:9 landscape format` | `Ilustraciones/Escenas` | `Evento_` |
| secreto | no lleva imagen | — | — | — |

Si el tipo de la nota no figura en esta tabla, el módulo todavía no tiene imagen: dilo y detente. Cada módulo nuevo añade aquí su fila y su sección.

**Mapas:** además de esta imagen, los lugares con leyenda (regla `mapa` de su módulo) tienen mapa, en la carpeta `Mapas` y con el prefijo `Mapa_`. Su prompt no sale de esta tabla sino de `mapas.md`.

## Reglas comunes
- **Concreto:** colores, materiales, formas y luz. Nada de nombres propios del mundo, porque el modelo no los conoce: describe lo que se ve.
- **Punto de partida:** la "Descripción visual" de la sección Imagen de la nota, que ya reúne lo esencial.
- **Nada gráfico,** aunque la crudeza del mundo sea adulta: los filtros de contenido de los modelos de imagen rechazan lo explícito. Sugiere el horror en vez de mostrarlo: `unsettling`, `disturbing silhouette`, `subtle deformities`.
- **Nunca** nombres de personas reales ni de artistas vivos. Las referencias a juegos y estilos de la Guía Visual sí valen.
- **El formato va siempre al final del prompt** y lo pone el tipo, no la Guía Visual.
- **Mayúscula al empezar cada bloque:** los bloques de la Guía se copian tal cual, pero cada uno empieza una frase (`Expressive charcoal drawing…. Dark medieval fantasy world…. Dramatic fine-art charcoal study.`).
- **Técnicas sobre papel** (📄 en `tecnicas.md`): el fondo no es oscuro, sino que se funde con el soporte. En FONDO usa `{lugar}, loosely suggested and fading into the bare paper` (o `parchment`, según la técnica).

## personaje — retrato
```
{ESTILO}. Close-up head and shoulders portrait with a highly detailed face, {ANGULO} view, {MIRADA}. Subject: {SUJETO}. Facial features: {RASGOS}. Expression: {EXPRESION}. Wearing: {VESTIMENTA}. Distinctive detail: {DETALLE}. Lighting: {LUZ}. Background: {FONDO}. Single character. {ACABADO}. {RESTRICCIONES}. Square 1:1 format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| SUJETO | edad, especie, género, ocupación o arquetipo | `a 41-year-old human former soldier turned vagrant` |
| RASGOS | Apariencia: rostro, cabello, ojos, piel y marcas | `gaunt face, a long scar across the left cheek, milky left eye` |
| EXPRESION | Personalidad (temperamento, bajo presión) | `haunted, wild-eyed, muttering` |
| VESTIMENTA | Apariencia: vestimenta habitual; equipo | `a torn hooded brown cloak over rusted mail` |
| DETALLE | Rasgo distintivo | `a crude iron hook in place of his left hand` |
| LUZ | Residencia, ocupación, momento del día | `distant flickering torchlight` |
| FONDO | Residencia o ubicación actual, sin que compita con el rostro | `a dark, indistinct narrow night alley`; sobre papel: `a narrow alley, loosely suggested and fading into the bare paper` |

**Ángulo y mirada según la personalidad:**

| Personalidad dominante | ANGULO | MIRADA |
|---|---|---|
| Seguro, desafiante, autoritario | `front-facing` | `looking intently at the viewer` |
| Reservado, astuto, desconfiado | `3/4 profile` | `looking slightly off-camera` |
| Melancólico, culpable, reflexivo | `3/4 profile` | `looking thoughtfully downward` |
| Altivo, distante, soñador | `side profile` | `looking far to the side` |
| Inestable, perturbado, salvaje | `almost front-facing` | `staring past the viewer with unfocused eyes` |

## region — paisaje
```
{ESTILO}. Sweeping wide landscape vista {PUNTO_DE_VISTA}. Subject: {SUJETO}. Terrain: {RELIEVE}. Vegetation and water: {VEGETACION_AGUA}. Landmark: {HITO}. Atmosphere: {ATMOSFERA}. Lighting: {LUZ}. No characters in the foreground. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| PUNTO_DE_VISTA | Categoría y relieve | `from a high mountain ridge`, `from the sea approaching the coast` |
| SUJETO | Qué clase de región es, sin su nombre | `a vast rugged highland of lakes and moors` |
| RELIEVE | Geografía: relieve y aguas | `jagged cliffs, rolling moorland, deep fjords` |
| VEGETACION_AGUA | Biomas, ríos, costas | `sparse pine forests, winding rivers, salt marshes` |
| HITO | Un lugar notable visible a lo lejos | `a ruined watchtower on a distant headland` |
| ATMOSFERA | Clima, estación y una señal visible del conflicto central | `heavy rain clouds, a column of black smoke rising on the horizon` |
| LUZ | Momento del día que mejor la define | `pale cold dawn light` |

**Según la categoría:**
- **`fisica`:** el paisaje natural es el protagonista.
- **`politica`:** su paisaje característico más una señal del poder (`a fortified border wall`, `banners flying over watchtowers`).
- **`plano`:** la dimensión como paisaje, aunque sea imposible (`an otherworldly realm of floating stone islands over a starless void`).

## ecosistema — paisaje del bioma
```
{ESTILO}. Wide landscape of a biome of an invented world, {PUNTO_DE_VISTA}. Biome: {SUJETO}. Terrain and water: {TERRENO}. Plant life: {FLORA}. Animal life: {FAUNA}. Sign of its balance or its change: {SENAL}. Lighting and atmosphere: {LUZ}. No people in the foreground. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| PUNTO_DE_VISTA | Desde dónde se ve mejor, de «Cómo es» | `seen from the edge of a peat bank at water level` |
| SUJETO | Qué clase de bioma es, sin su nombre | `a red peat marsh under low fog` |
| TERRENO | El terreno y el agua | `dark pools between tussocks of rust-red moss, standing water reflecting the sky` |
| FLORA | Sus plantas, de «La vida» | `stunted black alders, pale reeds, clusters of bulbous fungi` |
| FAUNA | Una o dos de sus criaturas, pequeñas | `a flock of long-legged wading birds, a half-hidden shape in the water` |
| SENAL | Lo que lo sostiene o lo que lo amenaza, de «Equilibrio y cambios» | `a band of dead grey trees where the water turned bitter` |
| LUZ | La luz y el tiempo | `diffuse grey morning light, drifting fog` |

**La vida es el sujeto:** a diferencia del paisaje de una región, aquí importa lo que vive: las plantas y las criaturas se ven, aunque pequeñas, y el plano se acerca lo justo para mostrarlas. Un ecosistema artificial (unos campos, una ciudad, el jardín de una nave), con su gente trabajando a lo lejos; uno sobrenatural, con lo que tiene de extraordinario a la vista.

## fenomeno — plano atmosférico
```
{ESTILO}. Atmospheric wide shot of an extraordinary phenomenon over a landscape, {PUNTO_DE_VISTA}. Phenomenon: {FENOMENO}. Landscape: {PAISAJE}. Mark on the land: {HUELLA}. Scale: {ESCALA}. Lighting and color: {LUZ}. Mood: {SENSACION}. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| PUNTO_DE_VISTA | Desde dónde se ve con seguridad | `seen from a rocky ridge at a safe distance` |
| FENOMENO | Manifestación: forma, color, movimiento | `a slow, endless storm of violet lightning coiling over the land` |
| PAISAJE | Zonas afectadas | `a cracked salt flat with a distant ruined tower` |
| HUELLA | Efectos sobre los lugares | `glassy scorched streaks where the lightning has struck` |
| ESCALA | Una figura o un elemento pequeño que dé el tamaño | `a tiny caravan of travelers crossing far below` |
| LUZ | La luz y el color del fenómeno | `a cold violet glow under a black sky` |
| SENSACION | Lo que transmite | `awe and dread` |

**El fenómeno es el protagonista:** ocupa buena parte del encuadre, y las figuras, si las hay, son pequeñas y lejanas. Su peligro se sugiere por su huella en el paisaje, nunca con víctimas en primer plano.

## especie — figura de cuerpo entero
```
{ESTILO}. Full-body concept art of a typical member of an intelligent species, {POSE}. Being: {SUJETO}. Anatomy: {ANATOMIA}. Distinctive traits: {RASGOS}. Clothing and gear: {ATUENDO}. Scale: {ESCALA}. Background: {FONDO}. Single figure. {ACABADO}. {RESTRICCIONES}. Vertical 3:4 portrait format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| POSE | Una postura neutra y natural | `standing in a relaxed three-quarter view` |
| SUJETO | Qué clase de ser es, sin su nombre | `a tall, slender humanoid with long limbs` |
| ANATOMIA | Anatomía: cuerpo, cobertura, extremidades | `olive-green scaled skin, digitigrade legs, four-fingered hands` |
| RASGOS | Lo que la delata a simple vista | `large amber eyes with vertical pupils and a crest of quills` |
| ATUENDO | El atuendo habitual de sus culturas, o nada | `simple woven wraps and a bone-handled knife at the belt` |
| ESCALA | Una referencia de tamaño | `standing beside a plain wooden staff as tall as an adult human` |
| FONDO | Su hábitat, apenas sugerido | `a sun-baked canyon, loosely suggested` |

**Un miembro típico, no un individuo:** sin heridas, marcas ni objetos personales que lo conviertan en un personaje concreto. Si la especie tiene variaciones visibles (tallas, colores), elige la más común y menciónalas en la descripción visual de la ficha.

## cultura — tres miembros con su atuendo
```
{ESTILO}. Medium shot of three members of a people in their traditional dress, {ESCENA}. People: {SUJETO}. The three: {TRES}. Clothing and adornment: {ATUENDO}. Cultural detail: {DETALLE}. Setting: {ENTORNO}. Lighting: {LUZ}. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| ESCENA | Una actividad típica de su vida cotidiana o de sus ritos | `sharing a meal around a low fire` |
| SUJETO | Su especie y su aspecto general, sin su nombre | `weathered highland herders` |
| TRES | Tres edades o papeles distintos | `an elder woman, a young man and a child, each with a different task` |
| ATUENDO | Vestimenta, adornos, peinados | `layered wool cloaks dyed ochre, braided hair with copper rings` |
| DETALLE | Un objeto, una artesanía o un símbolo de la cultura | `a carved wooden totem and woven baskets` |
| ENTORNO | Su territorio o su vivienda | `a windswept stone village on a hillside` |
| LUZ | La luz que mejor la define | `warm late-afternoon light` |

**Tres personas, no tres copias:** edades, papeles o gestos distintos que muestren la variedad dentro de la cultura. Nada de rasgos reales identificables como una etnia del mundo real si la Ficha pide un mundo inventado.

## idioma — muestra de su escritura
```
{ESTILO}. Calligraphic sample of an invented writing system on {SOPORTE}. Glyphs: {GLIFOS}. Layout: {DISPOSICION}. Ink and tools: {TINTA}. Decoration: {ADORNO}. The glyphs are invented and unreadable: no letters, numbers or words from any real alphabet or script. {ACABADO}. {RESTRICCIONES}. Square 1:1 format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| SOPORTE | Escritura: materiales y soportes | `a weathered strip of cured hide` |
| GLIFOS | Escritura: aspecto de los signos | `angular hooked strokes, each sign built around a single vertical stem` |
| DISPOSICION | Cómo se escriben: dirección, columnas, espirales | `three short vertical columns read from top to bottom` |
| TINTA | Con qué se escribe | `dark brown ink applied with a split reed` |
| ADORNO | Un adorno, un sello o una marca de quien escribe | `a small knotted cord threaded through one corner` |

**La escritura es el sujeto:** en este tipo, quita `No text` de las RESTRICCIONES de la Guía (deja el resto, como `no watermark`) y no añadas letras reales. Si la lengua no tiene escritura, la muestra es cómo guardan la memoria (cordones anudados, muescas talladas, cuentas ensartadas), con `no text` de nuevo.

## calendario — rueda del calendario
```
{ESTILO}. Ornate circular calendar wheel of an invented world on {SOPORTE}, seen from directly above. Divisions: {DIVISIONES}. Seasons: {ESTACIONES}. Center: {CENTRO}. Detail: {DETALLE}. All glyphs and symbols are invented and unreadable: no letters, numbers or words from any real alphabet or script, and no real zodiac or calendar signs. {ACABADO}. {RESTRICCIONES}. Square 1:1 format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| SOPORTE | El soporte de la descripción visual | `a weathered round slab of carved grey stone` |
| DIVISIONES | Los meses: cuántos son y cómo se marcan | `twelve wedge-shaped segments, each marked with a small invented glyph` |
| ESTACIONES | Las estaciones y sus motivos | `four quadrants tinted with seasonal motifs: sprouting grain, a blazing sun, falling leaves, bare frozen branches` |
| CENTRO | El astro que lo guía o el hecho del año 0 | `a stylized eclipsed sun` |
| DETALLE | Las fiestas, los días fuera de los meses u otra cuenta | `a narrow outer ring of five blank days set apart from the months` |

**La rueda es el sujeto:** como en el idioma, quita `No text` de las RESTRICCIONES de la Guía (deja el resto) y no añadas letras ni números reales: los meses se marcan con glifos inventados.

## era — escena alegórica
```
{ESTILO}. Allegorical wide scene that sums up a whole era of an invented world, {COMPOSICION}. Defining force: {FUERZA}. Figures: {FIGURAS}. Setting: {ESCENARIO}. Symbols: {SIMBOLOS}. Lighting and mood: {LUZ}. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| COMPOSICION | Cómo se ordena la escena para contar la era | `with the rising power at the center and the fallen at the edges` |
| FUERZA | Qué la define | `a colossal crowned figure of stone and gold looming over endless marching banners` |
| FIGURAS | Figuras anónimas que la encarnan, sin nombres | `kneeling peasants, armored standard-bearers and a robed chronicler` |
| ESCENARIO | Su paisaje o su arquitectura | `terraced cities of white stone climbing a mountainside` |
| SIMBOLOS | Objetos o signos de la era | `broken chains, overflowing granaries and a sealed book` |
| LUZ | La luz y el ánimo | `golden late-afternoon light darkening toward a stormy horizon` |

**Alegoría, no crónica:** la imagen resume la era entera (sus fuerzas, su ánimo), no un momento concreto: los momentos son de los eventos. Las figuras son tipos (un rey, una cronista, un soldado), sin nombres propios.

## evento — el momento clave
```
{ESTILO}. Dramatic wide scene of a decisive moment in the history of an invented world, {ENCUADRE}. Moment: {MOMENTO}. Figures: {FIGURAS}. Setting: {ESCENARIO}. Detail: {DETALLE}. Lighting and mood: {LUZ}. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| ENCUADRE | Desde dónde se ve el instante | `seen from a low angle at the edge of the fray` |
| MOMENTO | El momento clave, congelado | `the instant the river dam bursts and the water sweeps the bridge away` |
| FIGURAS | Quiénes están, sin nombres: tipos y gestos | `soldiers on the bridge turning in terror, a lone rider spurring toward the far bank` |
| ESCENARIO | El lugar del hecho | `a narrow stone bridge over a swollen grey river in a wooded valley` |
| DETALLE | Un objeto o un gesto que lo cuente | `a torn banner caught on the broken railing` |
| LUZ | La luz y el ánimo | `cold storm light breaking through low clouds, chaos and awe` |

**Un instante, no un resumen:** la imagen congela el momento clave; la alegoría que resume una época es la de la era. Nada gráfico: la violencia se sugiere (la tensión, el movimiento, las consecuencias), no se muestra.

## costumbre — en plena práctica
```
{ESTILO}. Wide scene of a custom of an invented world being practiced, {ENCUADRE}. Custom: {SUJETO}. Participants: {PARTICIPANTES}. Setting: {ESCENARIO}. Gestures and objects: {ELEMENTOS}. Lighting and mood: {LUZ}. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| ENCUADRE | Desde dónde se ve | `seen from the edge of the crowd, at eye level` |
| SUJETO | Qué se hace, sin su nombre | `a harvest festival in which the last sheaves are burned on a hilltop` |
| PARTICIPANTES | Quiénes la cumplen, sin nombres: tipos, atuendos y gestos | `villagers in patched wool cloaks passing torches hand to hand, children on their parents' shoulders` |
| ESCENARIO | Dónde se cumple | `a bare hilltop above a valley of stubble fields at dusk` |
| ELEMENTOS | El gesto, el objeto o la comida que la distinguen | `a towering pyre of straw shaped like a figure, clay bowls of dark bread set at its foot` |
| LUZ | La luz y el ánimo | `firelight against a cold violet sky, solemn and joyful at once` |

**Su momento más reconocible:** la fiesta en su punto álgido, el rito en su gesto central, la ley al cumplirse o al castigarse, el tabú en la señal que lo recuerda (la puerta que nadie cruza, el plato que nadie toca). Las figuras, sin protagonismo individual: la costumbre es el sujeto. Nada gráfico, aunque haya castigo o sacrificio: se sugiere.

## obra — la obra o su interpretación
```
{ESTILO}. {VISTA}. The work: {SUJETO}. What it shows: {CONTENIDO}. Setting: {ENTORNO}. Focal detail: {DETALLE}. Lighting and atmosphere: {LUZ}. Only invented symbols: no letters, numbers or words from any real alphabet. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| VISTA | La vista según su categoría (abajo) | `A wide view of a vast faded mural on the wall of a ruined chapel of an invented world` |
| SUJETO | Qué es, sin su título | `a mural of drowned figures rising toward a pale sun` |
| CONTENIDO | Lo que muestra o cuenta, de «Lo que dice», como imagen | `rows of figures with closed eyes, water lines painted across their chests, a single open hand at the center` |
| ENTORNO | Dónde está o dónde se canta, se lee o se representa | `cracked plaster, candle soot, a few pilgrims kneeling` |
| DETALLE | Lo que llama la atención | `a fresh scrape where someone tried to erase a face` |
| LUZ | La luz y el ambiente | `dim candlelight with a cold shaft from a broken window` |

**Vista por categoría:**
- **pintura, escultura o mapa:** la obra misma, como es y donde está: `A wide view of {la obra} of an invented world`. Un mapa, como un objeto antiguo sobre una mesa, con sus dibujos y sin letras.
- **texto, documento o poema:** el ejemplar abierto en su sitio, con sus ilustraciones o sus sellos, y sin letras legibles (`pages filled with invented script`), o el momento en que alguien lo lee en voz alta.
- **canción o representación:** el momento en que se canta o se representa, con quien la canta y quien escucha: `A scene of a song being performed in an invented world`.

La obra es el sujeto: lo que muestra o lo que se canta se entiende sin palabras. Si es un relato, se elige su escena más reconocible, como en un mito.

## asentamiento — llegada por el camino
```
{ESTILO}. Wide establishing view of a settlement of an invented world, seen from the road that leads to it, {PUNTO_DE_VISTA}. Settlement: {SUJETO}. Architecture: {ARQUITECTURA}. Surroundings: {ENTORNO}. Signs of life: {VIDA}. Landmark: {HITO}. Lighting and atmosphere: {LUZ}. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| PUNTO_DE_VISTA | Desde dónde se llega: una colina, un recodo, un muelle | `from a muddy bend of the road on a low hill` |
| SUJETO | Su categoría y su tamaño, sin su nombre | `a walled river town of a few thousand people` |
| ARQUITECTURA | Arquitectura y materiales | `steep slate roofs, timber-framed houses packed inside grey stone walls` |
| ENTORNO | Lo que lo rodea | `terraced fields and a slow brown river with a stone bridge` |
| VIDA | Señales de vida | `carts queuing at the gate, chimney smoke, laundry on lines` |
| HITO | Lo más visible | `a crooked bell tower rising above the rooftops` |
| LUZ | La luz y el ambiente | `late-afternoon light under a hazy sky` |

**El asentamiento es el sujeto, visto desde fuera:** el plano muestra su silueta entera y su relación con el entorno; las figuras, pequeñas y sin protagonismo. Un campamento o una estación se ven igual: desde el camino, el sendero o la ruta por la que se llega.

## lugar — su vista más emblemática
```
{ESTILO}. Wide view of a place of an invented world, {VISTA}. Place: {SUJETO}. Form and materials: {FORMA}. Surroundings: {ENTORNO}. Signs of use or neglect: {SENALES}. Focal detail: {DETALLE}. Lighting and atmosphere: {LUZ}. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| VISTA | Por fuera o por dentro, y desde dónde | `seen from the muddy street outside its door` / `interior view of its main hall from the entrance` |
| SUJETO | Qué es, sin su nombre | `a low roadside inn of dark timber` |
| FORMA | Su forma y sus materiales, o la forma del terreno | `a sagging thatched roof, smoke-stained beams, a stone hearth wall` |
| ENTORNO | Lo que lo rodea o lo que hay dentro | `a crossroads in a misty pine forest` |
| SENALES | Señales de uso o de abandono | `horses tied outside and warm light in the shutters` |
| DETALLE | Lo que llama la atención | `a carved wooden sign shaped like a lantern` |
| LUZ | La luz y el ambiente | `blue dusk with a cold drizzle` |

**La vista más emblemática:** la que define el sitio. Una posada o un templo, por fuera; una mazmorra o una cripta, desde su sala principal; un paraje, desde donde mejor se ve. Las figuras, pequeñas: el lugar es el sujeto.

## ruta — a lo largo del camino
```
{ESTILO}. Wide view along a route of an invented world, {VISTA}. Route: {SUJETO}. The way itself: {OBRA}. Landscape it crosses: {PAISAJE}. Travelers: {VIAJEROS}. Focal detail: {DETALLE}. Lighting and atmosphere: {LUZ}. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| VISTA | Desde dónde se ve el tramo: a ras de camino, desde un alto, desde la cubierta | `seen from the middle of the road as it winds away toward a distant pass` |
| SUJETO | Qué es, sin su nombre | `an old paved trade road climbing through hill country` |
| OBRA | Cómo es el camino: firme, obra, señales | `worn flagstones half sunk in mud, leaning milestones, a narrow stone bridge` |
| PAISAJE | Lo que cruza, de su Recorrido | `bare moorland, a slow river below, low clouds over the ridges` |
| VIAJEROS | Quién la recorre hoy, de «Quién la recorre», pequeños; o nadie, si está abandonada | `a small caravan of mule carts and two hooded guards` / `no one: grass grows between the stones` |
| DETALLE | Lo que llama la atención: un peaje, un mojón, una señal de su peligro | `a toll gate of black timber with a lantern` |
| LUZ | La luz y el ambiente | `grey morning light, drizzle` |

**El camino es el sujeto:** el plano sigue la ruta, que se aleja hacia el fondo y lleva la vista; las figuras, pequeñas. Según su categoría:
- **fluvial o marítima:** desde la cubierta o la orilla, con la estela, las boyas, los faros o la costa que la marcan;
- **subterránea:** el túnel o la galería que se pierde en la oscuridad, con la luz de quien la recorre;
- **aérea o espacial:** la ruta vista desde la montura o la nave, con las balizas, las torres o los astros que la guían;
- **paso:** el tramo más duro (el collado, el desfiladero, la pasarela sobre la ciénaga);
- **portal:** el portal y quien está a punto de cruzarlo, con lo que se ve (o se intuye) al otro lado. Su forma y su efecto, según las reglas de su `sistema`;
- **sin salida:** el tramo donde se pierde (la senda que se borra en la niebla, el camino que acaba en nada);
- **perdida o dudosa:** lo que queda de ella (unas losas bajo el musgo, un mojón solitario), o el tramo tal como lo describe su fuente.

## faccion — emblema o estandarte
```
{ESTILO}. Emblem of an organization of an invented world, shown as {SOPORTE}, centered and seen straight on. Main figure: {FIGURA}. Colors and materials: {COLORES}. Secondary elements: {ELEMENTOS}. Character of the design: {CARACTER}. Only invented symbols: no letters, numbers or words from any real alphabet, and no real-world heraldry, flags or religious symbols. {ACABADO}. {RESTRICCIONES}. Square 1:1 format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| SOPORTE | Dónde se lleva el emblema | `a weathered cloth banner hanging from a crossbar` / `a red wax seal` / `a painted wooden shield` |
| FIGURA | La figura principal del emblema | `an open hand holding a lantern` |
| COLORES | Colores y materiales | `faded ochre and charcoal black on rough linen` |
| ELEMENTOS | Lo que acompaña a la figura | `a border of knotted rope and three small stars` |
| CARACTER | Cómo es el diseño | `austere and hand-stitched, mended in places` |

**El emblema es el sujeto:** centrado, de frente y sin escena alrededor (como mucho, el soporte que lo sostiene). En este tipo se mantiene `No text`: el lema va en la ficha, no en la imagen.

## linaje — blasón o marca de familia
```
{ESTILO}. Coat of arms of a family of an invented world, shown as {SOPORTE}, centered and seen straight on. Field: {CAMPO}. Main charge: {FIGURA}. Colors and materials: {COLORES}. Secondary elements: {ELEMENTOS}. Character of the design: {CARACTER}. Only invented symbols: no letters, numbers or words from any real alphabet, and no real-world coats of arms, flags or religious symbols. {ACABADO}. {RESTRICCIONES}. Square 1:1 format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| SOPORTE | Dónde se muestra el blasón | `a painted heater shield hanging on a stone wall` / `a coat of arms carved above a gate` / `a signet ring pressed into wax` |
| CAMPO | La división y el fondo del escudo | `divided vertically, deep green and bone white` |
| FIGURA | La figura principal | `a heron standing on one leg` |
| COLORES | Colores y materiales | `faded green, bone white and tarnished silver` |
| ELEMENTOS | Cimera, soportes o bordura | `a narrow black border and a crest of reeds` |
| CARACTER | Cómo es el diseño y cuánto ha vivido | `old and worn, repainted many times` |

**El blasón es el sujeto:** centrado y de frente, como el emblema de una facción. Un clan o una familia sin heráldica muestra su marca en lugar del escudo: un tótem tallado, un sello, un dibujo bordado. Se mantiene `No text`: el lema va en la ficha.

## objeto — el objeto solo
```
{ESTILO}. A single object of an invented world, centered and seen {ANGULO}, against {FONDO}. Object: {SUJETO}. Materials and craftsmanship: {MATERIALES}. Details and markings: {DETALLES}. Signs of age and use: {DESGASTE}. Lighting: {LUZ}. No people, no hands. {ACABADO}. {RESTRICCIONES}. Square 1:1 format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| ANGULO | Desde dónde se ve mejor | `from a slight three-quarter angle` |
| FONDO | Un fondo oscuro y liso; sobre papel, el papel | `a plain dark background`; sobre papel: `the bare paper` |
| SUJETO | Qué es, sin su nombre | `a short single-edged knife with a hooked tip` |
| MATERIALES | Materiales y factura | `blackened iron blade, handle of polished bone bound with copper wire` |
| DETALLES | Marcas, grabados, adornos | `small invented glyphs etched along the spine` |
| DESGASTE | Señales del tiempo y del uso | `a nicked edge and a dark stain worn into the grip` |
| LUZ | La luz que lo define | `a single warm light from the left` |

**El objeto es el sujeto:** solo, centrado y entero, sin manos ni personas. Un vehículo o una máquina grande se ven enteros, en su medio (el agua, el camino) pero sin escena alrededor. Las inscripciones, con glifos inventados e ilegibles, nunca con letras reales.

## creencia — símbolo sagrado
```
{ESTILO}. Sacred symbol of a faith of an invented world, shown as {SOPORTE}, centered and seen straight on. The symbol: {FIGURA}. Materials and colors: {MATERIALES}. Around it: {ELEMENTOS}. Signs of devotion and age: {DESGASTE}. Only invented symbols: no letters, numbers or words from any real alphabet, and no real-world religious symbols (no crosses, crescents, stars of David, ankhs, om, yin-yang or pentagrams). {ACABADO}. {RESTRICCIONES}. Square 1:1 format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| SOPORTE | Dónde se ve el símbolo | `a small carved bone amulet on a leather cord` / `a painting on a cracked plaster wall` / `a stone altar slab` |
| FIGURA | La figura del símbolo, sin su nombre | `an open eye inside a ring of seven flames` |
| MATERIALES | Materiales y colores | `yellowed bone inlaid with faded red ochre` |
| ELEMENTOS | Lo que lo acompaña | `melted candle stubs and small offerings of salt` |
| DESGASTE | El uso de la devoción | `rubbed smooth by generations of fingers` |

**El símbolo es el sujeto:** centrado, de frente y sin fieles ni escena alrededor (como mucho, el soporte y las ofrendas). En este tipo se mantiene `No text`: las oraciones van en la ficha, no en la imagen.

## deidad — como la imaginan sus fieles
```
{ESTILO}. Devotional full-body depiction of a deity of an invented world, as its worshippers imagine it, {POSE}. Being: {SUJETO}. Form and attributes: {FORMA}. Symbols: {SIMBOLOS}. Setting: {ENTORNO}. Lighting: {LUZ}. Single figure. {ACABADO}. {RESTRICCIONES}. Vertical 3:4 portrait format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| POSE | Su actitud según su carácter | `standing calmly at full height, one hand raised in greeting` |
| SUJETO | Qué es y cómo es su figura, sin su nombre | `a tall hooded traveler with a face of weathered bronze` |
| FORMA | Sus atributos y lo que la acompaña | `a walking staff hung with small bells, a cloak of travel-worn leather` |
| SIMBOLOS | Su símbolo y sus señales | `three branching lines carved into the head of its staff` |
| ENTORNO | Cómo y dónde la pintan sus fieles | `standing at a crossroads lined with tiny votive lamps` |
| LUZ | La luz que la define | `warm dusk light from behind, long shadows on the road` |

**Una imagen devota, no un retrato:** muestra a la deidad tal como la imaginan sus fieles (su icono), no lo que es de verdad. Nada de iconografía, símbolos ni figuras religiosas del mundo real; si la Ficha pide que nada sea gráfico, su terror se sugiere.

## afeccion — lámina de estudio
```
{ESTILO}. Study plate from an invented world's treatise on illnesses, specimen-style composition, centered. Subject of the plate: {SUJETO}. Visible signs: {SENALES}. Around it: {ELEMENTOS}. Colors: {COLORES}. Mood: {TONO}. Nothing graphic: no gore, no open wounds, no blood, no suffering faces; the illness shows only through its signs. Only invented symbols: no letters, numbers or words from any real alphabet. {ACABADO}. {RESTRICCIONES}. Square 1:1 format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| SUJETO | Qué estudia la lámina: una parte del cuerpo, un rostro de perfil, una planta o un animal | `a forearm and hand seen from above, resting on a cloth` |
| SENALES | Las señales visibles de la afección | `dark spots following the veins, fingertips turned pale blue` |
| ELEMENTOS | Sus fases en pequeño y lo que la rodea: remedios, útiles de quien la trata | `three small circular studies of its stages, a stone mortar with crushed leaves, a small glass vial` |
| COLORES | Los colores de la lámina | `faded ochre, dull rose and slate blue` |
| TONO | Cómo se siente | `quiet and clinical, faintly unsettling` |

**Una lámina, no una escena:** el sujeto aislado y centrado, como en un tratado de su época, sin pacientes sufriendo ni heridas. La afección se reconoce por sus señales. **Técnica sugerida:** `codice` (lámina de naturalista); si el usuario la quiere para todas sus afecciones, va en la tabla "Técnica por tipo" de su Guía Visual.

## material — lámina de espécimen
```
{ESTILO}. Specimen plate from an invented world's treatise on materials, centered study composition. Subject of the plate: {SUJETO}. Raw form: {BRUTO}. Worked form: {TRABAJADO}. Color, texture and luster: {TEXTURA}. Around it: {ELEMENTOS}. Mood: {TONO}. Only invented symbols: no letters, numbers or words from any real alphabet. {ACABADO}. {RESTRICCIONES}. Square 1:1 format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| SUJETO | Qué es, sin su nombre | `a dark metallic ore with reddish veins` |
| BRUTO | Cómo se encuentra, de «Dónde se encuentra» | `a rough chunk still embedded in grey bog rock` |
| TRABAJADO | Cómo queda trabajado, de «Cómo se obtiene y se trabaja» (si no se trabaja, una muestra cortada o pulida) | `beside it, a small polished ingot and a filed bar` |
| TEXTURA | Su color, su textura y su brillo, de «Cómo es» | `matte black surface with rust-red streaks and a faint oily sheen` |
| ELEMENTOS | Lo que lo acompaña: la herramienta que lo saca, la roca o el ser de donde sale, un corte que muestra su interior | `a miner's pick, a cut cross-section showing the vein, a few loose grains` |
| TONO | Cómo se siente | `quiet and studious, with a hint of danger` |

**Una lámina, no una escena:** el material aislado y centrado, en bruto y trabajado, como en un tratado de su época. Lo que sale de un ser vivo, junto a una silueta pequeña del ser o de la planta, sin nada gráfico. Un recurso (el agua, el suelo, una fuente de energía), por su muestra y su fuente: un frasco junto al pozo dibujado, un corte de la tierra con sus capas. Si tiene propiedades extraordinarias, se notan en la muestra (una luz, una escarcha, un temblor del aire), según su sistema. **Técnica sugerida:** `codice` (lámina de naturalista); si el usuario la quiere para todos sus materiales, va en la tabla "Técnica por tipo" de su Guía Visual.

## flora — lámina botánica
```
{ESTILO}. Botanical plate from an invented world's herbal, centered study composition. Subject of the plate: {SUJETO}. The whole plant: {PLANTA}. Details around it: {DETALLES}. Colors: {COLORES}. Mood: {TONO}. Only invented symbols: no letters, numbers or words from any real alphabet. {ACABADO}. {RESTRICCIONES}. Square 1:1 format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| SUJETO | Qué es, sin su nombre | `a low marsh herb with grey-green leaves` |
| PLANTA | Su porte entero, con la raíz si se ve, de «Cómo es» | `the whole plant drawn upright, with its pale twisted roots` |
| DETALLES | Sus partes en pequeño: la hoja, la flor, el fruto, la semilla, un corte | `a single leaf, a flower opened in cross-section, a seed pod and a slice of the root` |
| COLORES | Los colores de la lámina | `muted sage green, bone white and a touch of violet` |
| TONO | Cómo se siente | `calm and precise, faintly ominous` |

**Una lámina, no una escena:** la planta entera y sus partes, como en un herbario de su época. Un árbol: su silueta pequeña, una rama con sus hojas y su fruto, y un corte del tronco. Un hongo: el sombrero, el pie y las láminas, y un trozo de lo que lo sostiene. Si tiene propiedades extraordinarias, se notan en la planta (una luz, una escarcha, un brillo de la savia), según su sistema. **Técnica sugerida:** `codice` (lámina de naturalista); si el usuario la quiere para toda su flora, va en la tabla "Técnica por tipo" de su Guía Visual.

## criatura — en su hábitat
```
{ESTILO}. Wildlife concept art of a creature of an invented world, full body, {POSE}. Creature: {SUJETO}. Anatomy: {ANATOMIA}. Distinctive traits: {RASGOS}. Scale: {ESCALA}. Habitat: {HABITAT}. Lighting: {LUZ}. A single creature, no people. Nothing graphic: no gore, no torn prey, no blood; its danger shows in its bearing and its traces. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| POSE | Su pose característica, según su comportamiento | `stalking low through tall reeds` / `perched motionless on a dead branch` |
| SUJETO | Qué clase de ser es, sin su nombre | `a long-limbed predator the size of a horse` |
| ANATOMIA | Anatomía y aspecto: cuerpo, cobertura, extremidades | `matted grey fur, a narrow skull and too many joints in the legs` |
| RASGOS | Lo que la delata a simple vista | `pale eyes that catch the light, ears turned backwards` |
| ESCALA | Una referencia de tamaño del paisaje | `beside a fallen tree trunk taller than a man` |
| HABITAT | Su hábitat, con su huella en él | `a flooded birch forest at dusk, deep tracks in the mud` |
| LUZ | La luz de su hora de actividad | `cold blue twilight under a pale moon` |

**La criatura es la protagonista:** de cuerpo entero y en su hábitat, como en una lámina de un bestiario ilustrado, sin personas que le resten escala. Su peligro se ve en su porte, sus armas o la huella que deja, nunca en una presa destrozada. Si es diminuta, el plano se acerca lo justo para verla entera, con su hábitat alrededor.

## sistema — en uso
```
{ESTILO}. Wide scene of an invented world showing an extraordinary art, a technique or a law of nature at work, {ENCUADRE}. Action: {ACCION}. Figures: {FIGURAS}. Visible effect: {EFECTO}. Tools and gestures: {UTILES}. Its price: {PRECIO}. Setting: {ESCENARIO}. Lighting and mood: {LUZ}. Nothing graphic: no gore, no blood, no open wounds; the price shows only through its signs. Only invented symbols: no letters, numbers or words from any real alphabet. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| ENCUADRE | Desde dónde se ve | `seen at eye level from a few steps away` |
| ACCION | Qué se hace con él, sin su nombre (o la ley cumpliéndose) | `a healer drawing a fever out of a sleeping child through a braided cord` |
| FIGURAS | Quiénes están, sin nombres: tipos y gestos | `a gaunt kneeling healer, the child's mother watching from the doorway` |
| EFECTO | Lo que se ve que hace: su manifestación | `the cord slowly darkening from the child's wrist toward the healer's hand` |
| UTILES | Lo que necesita: herramientas, materiales, gestos | `a bowl of water, a bone needle, bundles of dried herbs` |
| PRECIO | Su coste, a la vista | `the healer's own fingertips already pale and trembling` |
| ESCENARIO | Dónde ocurre | `a low smoky room with a single shuttered window` |
| LUZ | La luz y el ánimo | `warm lamplight against cold blue shadows, hushed and tense` |

**En uso, no un diagrama:** la imagen muestra un momento concreto en que alguien lo usa, con su efecto y su precio a la vista, no un esquema de sus reglas. Una tecnología se ve trabajando con quien la maneja (una forja, un telar, una nave); una ley del universo, cumpliéndose (lo que les pasa a los muertos, lo que nunca puede hacerse); un concepto, encarnado en una escena (un trato que se sella, un juicio). Las figuras son tipos, sin nombres; los signos y las runas, inventados.

## mito — la escena del relato
```
{ESTILO}. Mythic wide scene from a legend of an invented world, as its storytellers imagine it, {COMPOSICION}. Moment: {MOMENTO}. Figures: {FIGURAS}. Setting: {ESCENARIO}. Symbols: {SIMBOLOS}. Lighting and mood: {LUZ}. Only invented symbols: no letters, numbers or words from any real alphabet, and no figures or symbols from real-world myths or religions. {ACABADO}. {RESTRICCIONES}. Wide 16:9 landscape format.
```

| Campo | Fuente en la ficha | Ejemplo |
|---|---|---|
| COMPOSICION | Cómo se ordena la escena para contar el relato, con la escala del mito | `with the tiny hero at the bottom and the giant filling the sky` |
| MOMENTO | El momento clave del relato, congelado | `the giant kneeling to drink the sea dry while fish fall from its beard` |
| FIGURAS | Quiénes están, sin nombres: tipos y gestos | `a small shepherd with a sling, villagers fleeing up the hills` |
| ESCENARIO | Dónde ocurre, según el relato | `a bay emptying into a cracked seabed, with stranded ships` |
| SIMBOLOS | Objetos o signos que el relato hace importantes | `a broken crown floating on the last pool of water` |
| LUZ | La luz y el ánimo | `a red dawn behind the giant, awe and dread` |

**Un relato, no una crónica:** la escena se ve como la imaginan quienes lo cuentan, con la escala y los símbolos del mito (figuras enormes, gestos solemnes, señales en el cielo), no como pasó: la verdad no se ve. Una profecía se muestra como la imaginan quienes la esperan. Las figuras son tipos, sin nombres. **Técnicas sugeridas:** `tapiz` o `manuscrito`; si el usuario las quiere para todos sus mitos, van en la tabla "Técnica por tipo" de su Guía Visual.
