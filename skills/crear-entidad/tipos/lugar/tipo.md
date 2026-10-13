# Tipo: lugar

Los sitios concretos del mundo: edificios (templos, fortalezas, puertos, mercados, posadas, talleres, casas, torres, monumentos), explotaciones (minas, canteras, salinas, pozos), ruinas y zonas peligrosas (mazmorras, pecios, yermos, zonas malditas) y parajes naturales (montañas, ríos y lagos, bosques, cuevas, islas, desiertos). La ficha dice dónde está, quién lo controla y quién lo ocupa, cómo es por fuera y por dentro, qué pasa allí, qué peligros y qué tesoros guarda y cómo se entra.

**No es un lugar:**
- un sitio donde vive una comunidad (`asentamiento`): una aldea o una ciudad contienen lugares;
- una gran región o un territorio (`region`): un continente, un reino o una comarca contienen asentamientos y lugares;
- un camino, un paso o un portal que une dos sitios (`ruta`): el lugar lo lista en sus `rutas`.

## Identidad del tipo
- **Emoji del tipo:** 📍, al inicio del H1: `# 📍 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (🍺 posada, ⛪ templo, 🏰 fortaleza, 🗼 torre, ⚒️ taller, ⛏️ mina o cantera, 🏚️ ruina, 🕳️ mazmorra, ⛰️ montaña, 🌊 agua, 🌲 bosque, 🏝️ isla…).
- **Carpeta:** según la `categoria`:
  - edificios y estructuras en uso (`edificio`, `templo`, `fortaleza`, `puerto`, `mercado`, `posada`, `taller`, `residencia`, `torre`, `monumento`) y las explotaciones (`explotacion`: minas, canteras, salinas, pozos) van en `10_Mundo/Lugares_y_Estructuras`;
  - lo abandonado o peligroso (`ruina`, `mazmorra`, `pecio`, `zona_peligrosa`) va en `10_Mundo/Ruinas_y_Zonas_Peligrosas`;
  - lo natural (`montana`, `agua`, `bosque`, `cueva`, `isla`, `desierto`, `paraje`) va en `10_Mundo/Geografia_y_Clima`.

  Un edificio en ruinas es `ruina`; un templo en uso, `templo`. La categoría sigue a lo que es hoy.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Lugar.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, valores permitidos, mapa y relaciones). Es de la familia `lugar` y su `completa` dice qué enlaces pendientes de otras fichas puede crear:
  - la residencia, la ubicación actual o el lugar de nacimiento de un personaje, cuando las notas describen un sitio («su taller», «la atalaya»), no un pueblo;
  - los lugares notables de una región, de un asentamiento o de otro lugar, y la ubicación de un lugar;
  - el escenario de un evento y la zona que afecta un fenómeno;
  - la sede de una facción, el centro o los lugares sagrados de una fe, y las `zonas` donde actúa una facción o donde se da una afección, cuando son un sitio (una mina, un pantano, unos muelles);
  - la partida, el destino o una parada de una ruta, cuando es un sitio (una posada del camino, un fuerte, una ruina al final de una senda);
  - el yacimiento de un material: una mina, una cantera, una salina (`explotacion`), o el paraje donde se encuentra.

  Antes de completar uno, lee lo que dicen de él las notas que lo enlazan: si describen un pueblo, es un `asentamiento`.

**Hechos importantes:** una posada, un taller, un claro o una ruina pequeña son detalles que Claude puede inventar según la autonomía de la Ficha. Un sitio que cambia la región (una fortaleza decisiva, el gran templo de una fe, una mazmorra legendaria) y que no está en el canon es un hecho importante: va como `Confirmar: …` en Preguntas Abiertas, enlazando su nota.

## Fechas y situación
- `construccion`: el año del eje en que se construyó o se fundó (vacío en lo natural, o si nadie lo sabe). `abandono`: el año en que dejó de usarse, se selló o se destruyó.
- **Si el calendario está por definir,** las fechas quedan vacías y el texto usa fechas relativas. No decidas el calendario: es un pilar (ver `referencias/pilares.md`).
- `situacion`:
  - `en_uso`: se usa hoy; sin `abandono`;
  - `abandonado`, `en_ruinas`, `sellado` y `destruido`: dejó de usarse, con `abandono` si se sabe;
  - `perdido`: nadie sabe dónde está, o cómo llegar;
  - `natural`: un paraje sin dueño ni uso concreto.

  `check_note.py` comprueba que la situación encaje con las fechas y con el año actual.

## Nombre
- Su nombre propio («La Lumbre Vieja», «el Faro de la Punta», «la Sima de los Ecos») en la lengua de quienes lo usan o de la bóveda, con `generate_names.py` si es un nombre inventado. En `aliases`, sus otros nombres.
- Archivo en ASCII. H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, dónde está y por qué importa.
- **Datos clave:** la tabla completa. «Origen» dice cuándo y por quién se construyó (o cómo se formó, si es natural); «Tamaño», a escala humana (una sala, tres pisos, media legua de bosque).
- **Exterior:** lo que se ve al acercarse, lo que se ve, se oye y se huele, y su forma y sus materiales (o la forma del terreno).
- **Recorrido:** de 3 a 6 zonas en el orden en que se recorren: las salas de un edificio, los niveles de una mazmorra, las partes de un bosque. Cada una con cómo es y qué hay. Si el lugar tiene mapa, nombra cada zona con su número de la leyenda («de la escalera (1) a la antecámara (2)»).
- **Mapa** (solo si le toca por su categoría y su relevancia; `check_note.py --depth lugar:<relevancia>:<categoría>`): la leyenda numerada de sus salas o partes, hasta 12 por nivel, con su orientación, lo que se ve y sus conexiones. Ruinas, mazmorras, cuevas, pecios, fortalezas, templos, torres, zonas peligrosas y explotaciones (sus galerías, sus pozos, sus niveles) lo llevan desde relevancia 2; los demás edificios, desde 3; los parajes naturales, desde 4; los monumentos, nunca. Ver `referencias/mapas.md`.
- **Actividad:** un día cualquiera (o quién pasa por un sitio abandonado) y quién viene y por qué.
- **Peligros y defensas:** lo que amenaza a quien entra y lo que lo protege (guardias, trampas, criaturas, el propio terreno).
- **Tesoros y recursos:** lo que guarda (objetos, saberes, secretos a la vista) y lo que se puede sacar de allí (madera, agua, mineral, información). Los materiales que tienen nota, enlazados y en `recursos`.
- **Accesos:** las entradas, los pasos ocultos y cómo se llega desde su ubicación (por qué ruta, enlazada si es una entidad, y en cuánto tiempo, coherente con `routes.py`). Los pasos ocultos que se conocen (y se sabe dónde están) van también en la leyenda del mapa (`Paso oculto a 7.`), y las trampas conocidas de «Peligros y defensas», en su zona (`Trampa: …`). Lo que nadie conoce es un secreto: ni aquí ni en el mapa.
- **Historia:** su origen, de 2 a 4 momentos decisivos y el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para la vista más emblemática, por fuera o por dentro (una posada, desde la calle; una mazmorra, desde su sala principal; un paraje, desde donde mejor se ve).
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `situacion`, `construccion` y `abandono`: ver arriba.
- Relaciones, solo con enlaces:
  - `ubicacion`: dónde está (un asentamiento, una región u otro lugar); ese sitio lo lista en sus `lugares_notables`;
  - `lugares_notables`: los lugares que contiene (la capilla de una fortaleza); cada uno lo tiene en su `ubicacion`;
  - `rutas` que pasan por él, salen o llegan a él: cada una lo tiene en su `partida`, su `destino` o sus `paradas`;
  - `dueno` (una persona) y `facciones` que lo controlan o lo usan;
  - `ocupantes`: quienes viven o trabajan allí;
  - `creencias` que se practican en él y `criaturas` que lo habitan (cada una lo tiene en su `habitat`);
  - `objetos` que guarda;
  - `recursos`: los materiales que se sacan de allí (el metal de una mina, la sal de una salina); cada uno lo tiene en sus `yacimientos`;
  - `fenomenos` que lo afectan, recíproca con sus `zonas_afectadas`;
  - `eventos` que ocurrieron en él: cada evento lo tiene en sus `lugares`;
  - `era` en que se construyó o se formó.
- `relevancia`: 4 o 5 un sitio que pesa en toda la región o en el mundo; 3 uno conocido en su comarca; 2 uno local; 1 un rincón.
- `ultima_revision` sin comillas.

## Coherencia
- **Su ubicación:** encaja con la geografía, el clima y la gente del sitio donde está, que lo lista en `lugares_notables`.
- **La Ficha:** la tecnología, los poderes y el conflicto central se notan en cómo está hecho, en qué lo amenaza y en qué guarda.
- **Lo que ya existe:** los personajes que lo ocupan o lo regentan, los eventos que ocurrieron en él y las criaturas o fenómenos que lo afectan deben encajar con lo que dicen sus notas. Léelas (`build_context.py`).
- **Reciprocidad:** su ubicación, los lugares que contiene, los fenómenos y los eventos que ya existen lo listan en su propiedad inversa.
- **Glosario:** registra su nombre, sus apodos y los términos nuevos.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 2 y 6 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- quien lo regenta o lo guarda (`dueno`, `ocupantes`);
- quien lo controla (`facciones`);
- lo que guarda (`objetos`);
- lo que lo habita (`criaturas`);
- un lugar que contiene (`lugares_notables`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, el lugar guarda un secreto (una sala que no figura en ningún plano, un muerto bajo el suelo, una puerta que no lleva a donde parece, algo que lo habita y nadie ha visto). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] La categoría lo lleva a su carpeta y sigue a lo que es hoy.
- [ ] Su ubicación lo lista en `lugares_notables`; los fenómenos y eventos que ya existen, también.
- [ ] La situación cuadra con sus fechas y con el año actual.
- [ ] Un sitio de peso que no estaba en el canon quedó como `Confirmar: …`.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
