# Plan de las skills

> **Seguimiento del desarrollo.** Cada punto se tilda al terminarlo: probado en un mundo de prueba y con commit.

## Visión
Un **sistema de creación de mundos con IA** que cualquiera pueda clonar para empezar su propio mundo en una bóveda de Obsidian.
- **Para cualquier género:** fantasía, ciencia ficción, histórico, terror… Nada de un mundo concreto en las skills.
- **Pensado para Obsidian:** notas con propiedades, enlaces, índices con Bases y una estructura de carpetas para un mundo.
- **Mundos ricos y entrelazados:** entidades completas, con historias, fechas y relaciones que se cruzan, coherentes con la Ficha y entre ellas.
- **Extensible:** cada tipo de entidad es un módulo, y las tablas, los perfiles de nombres y las técnicas se amplían sin tocar el código.
- **Muy completo:** desde la entrevista inicial hasta el motor que hace crecer el mundo solo, con validación, auditoría, imágenes e informes.
- **Barato en tokens:** la IA consulta el mundo con scripts y no lee la bóveda entera, que puede llegar a ser enorme.

## Redondeo
Lo que falta de esta sección se hace después de terminar las entidades (de la 20 a la 26).

- [x] **Repositorio propio para las skills.** Solo las skills, con un README que deja claro que trabajan sobre una bóveda de Obsidian. El mundo de prueba vive en su propio proyecto y usa las skills enlazadas.
- [x] **Consultas baratas:** que la IA no lea la bóveda entera. Probado con una deidad: la sesión buscó duplicados y relaciones con `search_vault.py`, escribió el Glosario y las preguntas con `add_entries.py` y auditó con `--focus`, sin abrir el Glosario, las preguntas, el registro ni el índice. El registro de ciclos y el git de la bóveda del motor están probados por script, y se confirmarán en el primer uso del motor. Medido en un mundo sintético de 3.000 notas: el índice daba 347.000 caracteres, y la búsqueda da menos de 3.000.
  - `search_vault.py`: entidades, enlaces pendientes, Glosario y preguntas que coinciden con un texto, también por nombres parecidos (posibles duplicados), o por tipo; con tope por grupo.
  - `add_entries.py` (Glosario y Preguntas Abiertas), `add_relation.py` (vínculos inversos) y `rename_link.py` (un nombre de rol por el definitivo): escriben sin que la IA lea las notas.
  - `log_cycle.py` (registro de generación del motor); `audit_world.py --focus` (solo lo de las notas tocadas, y el recuento del resto); topes en la salida del selector.
  - La regla en las skills y en el `CLAUDE.md` de cada mundo, y la cabecera del Glosario, que ya no invita a leerlo entero.
- [ ] **`inicializar-mundo` a fondo.** Hecho; se tilda cuando se pruebe con un mundo nuevo:
  - **el alcance:** la escala distingue una ciudad (o un sitio: una estación, un barco, una mazmorra), una región, un continente o un mundo, y varios mundos o planos. En una ciudad o una región, el foco es todo el mundo: el motor crea el foco con su tipo y todo dentro de él; lo de fuera se enlaza como referencia con el tipo `fuera`, que manda sobre el de la propiedad y el motor nunca crea; en un mundo-ciudad no se crean regiones. En uno mundial, lo más alto del mapa (el continente o el mundo) entra como enlace pendiente, para que cada región cuelgue de algo y el mapa del mundo tenga qué dibujar;
  - **los barrios:** el asentamiento gana la categoría `barrio`, con su `ciudad` y los `barrios` de la ciudad (recíprocas), su mapa urbano desde relevancia 4, y la cadena de lugares (el contexto, los mapas y las rutas) sube del barrio a su ciudad. Antes, un barrio con nombre propio iba al módulo `lugar`, que no tenía categoría para él;
  - **lo que ya tiene nombre:** una ronda para lo que el usuario ya tiene con nombre propio. Claude identifica cada entidad y su tipo (el foco, el primero, en un mundo local; lo más alto del mapa en uno mundial), el usuario lo confirma, y la Ficha nace con ellos enlazados, con su tipo en el registro de enlaces pendientes: el motor empieza por ellos (canon de base) y crea el foco completando su enlace;
  - la estructura de carpetas sigue igual en todas las escalas: es neutra, y las carpetas que una escala no usa quedan vacías. Las reglas de la escala van al `CLAUDE.md` que se genera.
- [ ] **`revisar-mundo`.** Hecha; se tilda cuando se pruebe con borradores reales. Dice cuántos borradores hay (por origen y por tipo, los que más pesan y cuánto le falta al motor para detenerse: `review_queue.py --summary`), el usuario elige cuántos revisar (o los pide al llamarla: «12», «los personajes», «solo lo del motor»), y los repasa en pantallas de 4, de lo que más pesa a lo que menos (relevancia y notas que los enlazan; cada secreto, detrás de su entidad; al final, lo ya revisado que siguió en borrador). Una ficha corta por borrador (`review_queue.py`): quién lo enlaza y cuántas en canon, lo que propuso, sus secretos, su imagen y su mapa, los enlaces pendientes que solo nombra él y los avisos del auditor; Claude lo coteja con la Ficha y con el canon que toca. Cuatro decisiones (`review_apply.py`):
  - **canon:** `estado: canon`; lo que propuso, o de lo que es sujeto, en Preguntas Abiertas queda confirmado; una línea en el Registro de Canon;
  - **sigue en borrador:** `revisado` con la fecha (propiedad opcional, que `check_note` acepta);
  - **archivar y rehacer:** la nota va a `03_Archivados` como `<Nota>_archivada`, así sus menciones vuelven a ser enlaces pendientes con su tipo y se crea de nuevo con el mismo nombre;
  - **quitar del mundo:** va a `03_Archivados` con su nombre (nada queda pendiente ni se recrea), el auditor avisa de cada mención hasta que Claude la reescribe, y su zona en el mapa se retira (`map_key.py --retire`: «se quita en la edición siguiente» y, al dibujarla, «retirada»; el dibujo la omite y la edición nueva la borra).
  - Al archivar, de las dos formas: sus imágenes van a `02_Activos/Anteriores` con `_archivada` (la nota archivada las sigue enlazando, y la imagen de la entidad rehecha no choca con la vieja), y los secretos que solo afectan a lo archivado van con ello. Las Estadísticas lo cuentan como archivado.
- [ ] **`consultar-mundo`.** Hecha; se tilda cuando se pruebe. Responde preguntas sobre el mundo con lo que dice la bóveda, sin leerla entera ni inventar: cita las notas con su estado (canon o borrador), atribuye lo que se cree, aparta los secretos (🔒, solo para el autor) y, sin spoilers (`--no-secrets`), ni los muestra ni dice que existen. Una tabla le dice qué consulta responde cada pregunta: las de `crear-entidad` (`search_vault`, `routes`, `world_stats`, `map_key`) y `query_world.py`, nueva:
  - `--about`: qué es algo, su estado, dónde está (aunque lo que lo contiene aún no tenga nota), sus fechas, sus relaciones con el estado de cada una, quién la tiene en sus relaciones y en qué propiedad, quién la nombra en su texto, sus secretos, lo que está por decidir y sus secciones; de un enlace pendiente, su tipo, si espera confirmación y lo que dicen de él las notas que lo nombran;
  - `--in`: lo que hay dentro de un lugar (también en sus barrios, lugares y comarcas), por tipo y con cómo se relaciona con él, y lo que se nombra dentro y aún no tiene nota;
  - `--timeline`: lo que tiene fecha, en orden, con los años del calendario y la marca de hoy;
  - `--outline` y `--section`: las secciones de una nota y el texto de las que hacen falta.
- [ ] **`narrar`.** Hecha; se tilda cuando se pruebe. Relatos, escenas, crónicas y documentos ambientados en el mundo, en `90_Narrativa` (el espacio que la Guía reserva para los usos del mundo), una subcarpeta por forma, con su índice y su plantilla, creados la primera vez. Las decisiones del usuario:
  - **No son entidades:** cuentan el mundo, no lo cambian. Fuera del índice y de los enlaces pendientes, y contadas aparte en las Estadísticas; en el grafo, con su color.
  - **Lo inventado se queda en la narración:** solo se enlaza lo que ya tiene nota; lo demás va sin enlace, en «Inventado aquí», y se ofrece crearlo como entidad.
  - **Los secretos, solo si se piden:** entonces la narración lleva `usa_secretos` y la etiqueta `secreto`, y queda fuera del «Grafo sin secretos».
  - **La ilustración, ofrecida al final:** `generar-imagen` tiene el tipo `narracion` (su momento clave, en `Escenas`, con el prefijo `Narracion_`).
  - Antes de escribir reúne el contexto con `consultar-mundo` (sin secretos, salvo que se pidan), comprueba fechas, viajes y quién vive en cada momento, y avisa si la idea choca con el canon. `narrative.py` prepara la estructura, comprueba cada narración (enlaces, secretos, quién vive y qué existe en su fecha, resumen y notas; cuenta las palabras) y lista las narraciones por entidad o por serie.

## Cómo funciona
- Cada "skill de entidad" es un **módulo** de `crear-entidad`, en `tipos/<tipo>/`, con tres archivos: `tipo.md`, `plantilla.md` y `modulo.json`. Se usa con `/crear-entidad <tipo> …`.
- Las imágenes las genera `generar-imagen` con Gemini en el Chrome del usuario, y con la Guía Visual del mundo:
  - la **ambientación** (género, tono, paleta) es la misma en todas;
  - la **técnica** (óleo, acuarela, cómic, lápiz… 27 en `generar-imagen/referencias/tecnicas.md`) la elige el usuario: general, por tipo o para una sola imagen.

  Cada tipo define qué muestra su imagen, su encuadre, su formato y su carpeta, pero no la técnica: como mucho la **sugiere** para la tabla "Técnica por tipo" de la Guía.
- El motor `expandir-mundo` hace crecer el mundo por ciclos y usa los módulos que existan: cada módulo nuevo amplía lo que el motor puede crear.
- **Orden:** primero el **canon base** (lo que todo lo demás necesita para ser coherente), después lo más enlazado.

## Esqueleto común de todas las fichas
**La relevancia decide la profundidad.** El frontmatter va siempre completo. El núcleo (datos clave, lo que define al tipo, el origen y el presente, la relación con el mundo, la imagen) va siempre; las secciones de profundidad, desde la relevancia que declara `profundidad` en `modulo.json` (de forma general: ganchos, citas, secretos y rumores, y momentos decisivos desde 3); las que el tipo no necesita por naturaleza (los ganchos de un idioma) se marcan con 0 y van solo si hay algo real que contar. Nunca se inventa para llenar: las cantidades de cada tipo son para relevancia 3 o más, el secreto se tira solo desde relevancia 3 y el rango de enlaces pendientes nuevos se reduce con la relevancia. La relevancia inicial no baja de la que pide el número de notas que ya la nombran (3, 6 y 10 notas: 3, 4 y 5).

**Relaciones:** solo se espejan las bilaterales por naturaleza (parentesco, vecindad, pertenencia, un pacto); las actitudes (rivalidad, miedo, desprecio) no, y el otro lado se escribe desde su punto de vista.

Cada módulo añade sus secciones propias sobre esta base común:
- **Inicio:** título con el emoji del tipo, resumen en cita e imagen embebida.
- **Datos clave:** tabla con lo esencial de un vistazo.
- **Descripción sensorial:** qué se ve, se oye y se huele.
- **Historia:** con fechas del calendario, o relativas si está por definir.
- **Relación con el mundo:** papel ante el conflicto central y el tema de la Ficha que encarna.
- **Secretos y rumores:** señales visibles y rumores. La verdad va en `80_Secretos` (secreto ocasional, por tirada).
- **Ganchos:** situaciones abiertas para desarrollar.
- **Citas:** voces del mundo sobre la entidad.
- **Imagen:** descripción visual y prompt.
- **Enlaces pendientes:** toda entidad que la ficha nombra va enlazada; las que aún no existen quedan como enlaces pendientes con su tipo (por su propiedad de relación o por el registro), y las nuevas, dentro del rango del módulo.

## Definición de terminado (cada módulo)
1. **Los tres archivos del módulo:**
   - `tipo.md` y `plantilla.md`, con `relevancia` y, si el tipo las tiene, fechas numéricas;
   - `modulo.json`, con familia, `completa` si es de una familia, emoji, rango de enlaces pendientes nuevos (`huecos_propios`), `profundidad`, `mapa` si es un lugar que lo lleva, carpeta, fechas, recíprocas y relaciones;
   - `profundidad`: qué secciones son de la profundidad (desde qué relevancia) y cuáles opcionales por naturaleza (0); las demás son el núcleo;
   - `reciprocas`: solo relaciones bilaterales por naturaleza (parentesco, vecindad, pertenencia, contención, un pacto), nunca actitudes (rivalidad, miedo, desprecio).
2. **Imagen:** la fila y la sección del tipo en `generar-imagen/referencias/prompt.md`: qué muestra y su encuadre, válidos con cualquier técnica (incluidas las de papel 📄). Si es un lugar con mapa, su clase de mapa en `generar-imagen/referencias/mapas.md`.
3. **Tabla de ingredientes:** `expandir-mundo/assets/Tablas/<Tipo>.md`, y los paquetes que lo usen en `Paquetes.md`.
4. **Ficha de ejemplo:** da "Correcta" en `check_note.py` (en una bóveda de prueba), y `check_modules.py` no da errores ni avisos nuevos.
5. **Nada de un mundo concreto:** ni en los ejemplos, ni en las tablas, ni en los comentarios. Se comprueba con una búsqueda que ignora las tildes y cruzando los ejemplos con lo que salió en las pruebas.
6. **Prueba del usuario** en un mundo de prueba, en una sesión nueva. Después se revisa, se limpia y se hace commit.

**Dónde se desarrolla y se prueba:** en la raíz de este repositorio, que tiene además un mundo de prueba que git ignora:
- `World_Building/`: la bóveda, con su propio repositorio git dentro. Las skills hacen sus commits ahí, con `git -C World_Building`. Se abre en Obsidian desde esa carpeta.
- `CLAUDE.md`: el del mundo de prueba.
- `.claude/skills/`: las skills de `skills/`, enlazadas (junctions en Windows), así que cada cambio se prueba al instante.

La prueba se hace en una sesión nueva abierta en la raíz. Para un mundo extra (por ejemplo, para probar `inicializar-mundo` desde cero) está `pruebas/<mundo>/`, también ignorada, con sus propios enlaces a las skills.

## Infraestructura (hecha)
- [x] **Familias de tipos y carpeta según categoría,** validadas por `check_note.py`.
- [x] **Imagen propia de cada tipo** (formato, carpeta y prefijo) y **propiedad `imagen` común**.
- [x] **Relevancia** del 1 al 5 en todas las entidades.
- [x] **Fechas numéricas** en el eje del calendario: año 0 y año actual en la Ficha.
- [x] **Relaciones recíprocas** declaradas en `modulo.json`, que el auditor exige solo si el otro tipo tiene la propiedad inversa. Solo las bilaterales por naturaleza (parentesco, vecindad, pertenencia, un pacto); las actitudes, como la rivalidad, no se espejan solas.
- [x] **Profundidad según la relevancia** (`profundidad` en `modulo.json`, `check_note.py --depth`), probada con una criatura de relevancia 2 y una mazmorra de relevancia 3.
- [x] **`completa`:** un módulo de una familia solo completa las propiedades que le corresponden.
- [x] **Reglas declarativas** en `modulo.json`: escalas, valores permitidos, la situación temporal (`tiempo`) y las propiedades que solo valen con ciertos valores de otra (`solo_si`).
- [x] **Biblioteca común `vault_lib.py`** y sus scripts:
  - `build_context.py`: el contexto de cada creación;
  - `generate_names.py`: nombres por perfil fonético;
  - `check_note.py`, `check_modules.py` y `audit_world.py`: la validación de cada nota, de los módulos y del mundo entero.
- [x] **Entrevista inicial:** "Decide tú" en las preguntas, un modo de entrevista ("solo lo esencial", "decide tú todo") y el calendario dividido en año 0 y año actual.
- [x] **Técnicas artísticas para las imágenes:** 27 técnicas independientes de la ambientación del mundo; general, por tipo, variada por sorteo o pedida para una imagen.
- [x] **Informe final en todos los generadores** (`report.py`): una instantánea antes de generar y, al terminar, qué se creó y qué cambió, los enlaces pendientes completados, las decisiones pendientes, los commits y el estado del mundo.
- [x] **Enlaces pendientes:**
  - toda entidad que una nota nombra va enlazada cada vez que la nombra (también con su nombre corto), a su nota o, si aún no existe, como enlace pendiente con su nombre real y su tipo;
  - lo que es una entidad se enlaza aunque esté dentro de otra o sea un colectivo; solo los términos van al Glosario sin enlace;
  - el registro `00_Sistema/Enlaces_Pendientes.md` lo genera `pending_links.py`;
  - `check_note.py` cuenta los enlaces pendientes nuevos de cada nota, exige su tipo y avisa de los nombres propios, las entidades del Glosario y las menciones que quedaron sin enlace;
  - una confirmación pendiente (`Confirmar`) bloquea solo su sujeto, el primer enlace de la línea;
  - el motor equilibra completar y crear según los enlaces pendientes por entidad (simulado: se estabiliza en torno a 1,5), con un presupuesto de enlaces nuevos por nota.
- [x] **Estadísticas del mundo** (`00_Sistema/Estadisticas.md`, tipo `meta`): `world_stats.py` la rehace entera con cada entrada de la Bitácora (`report.py --log`, `log_entry.py`) y al crear el mundo: entidades por tipo, estado y relevancia, secretos y archivadas, enlaces pendientes (listos, por confirmar y sin tipo), imágenes, mapas y los que toca redibujar, Glosario, preguntas, huérfanas, lo más nombrado que falta y lo más enlazado. Las cifras principales van en el frontmatter, para un tablero futuro. No cuenta como nota que nombra entidades. Probada con la obra: se rehízo sola al terminar, enlazada desde `MOC_Inicio`; tras la prueba, lo más nombrado que falta lleva el mismo tipo que el registro de enlaces pendientes (el módulo que lo creará: asentamiento, no lugar).
- [x] **Bitácora del mundo** (`00_Sistema/Bitacora.md`), probada con una mazmorra: la crónica para el autor, de lo más reciente a lo más antiguo. La crea `inicializar-mundo` con la creación del mundo; `report.py --log` añade la entrada de cada creación, profundización o tanda (con sus ciclos y la remisión al Registro de Generación); `log_entry.py`, las sueltas (una imagen o un mapa aparte, un cambio pedido fuera de las skills). Las notas que existen van enlazadas y los enlaces pendientes, como texto; la Bitácora no cuenta para los enlaces pendientes y la IA nunca la lee.
- [x] **Imágenes con Gemini en Chrome:** `generar-imagen` genera con Gemini en el navegador del usuario y mueve la descarga a la bóveda con `fetch_download.py`. Se probó Puter por API y se descartó por su límite mensual.
- [ ] **Imágenes por API:** reemplazar la vía del navegador por una API u otra vía más eficiente, que genere por script.
- [x] **Grafo de Obsidian:** `inicializar-mundo` deja `.obsidian/graph.json` con un grupo de color por tipo (`tag:#<tipo>`, con el `color` de cada módulo), un filtro sin 00_Sistema, los README ni los MOC, y sin adjuntos ni etiquetas como nodos; los enlaces pendientes, en gris. Con los nombres visibles desde más lejos (`textFadeMultiplier` -1), sin flechas (ensucian el grafo: se activan a mano y el script no las toca), y dos marcadores de grafo en `.obsidian/bookmarks.json` con el filtro, los colores y lo que se muestra: «Grafo sin secretos» (sin la carpeta ni la etiqueta del módulo `secreto`, para enseñar el mundo sin spoilers) y «Grafo completo». `graph_colors.py` lo aplica a un mundo existente o con tipos nuevos, conservando los grupos y el filtro propios del usuario. `check_note.py` avisa si una nota pierde la etiqueta de su tipo.
- [x] **Notas internas** (`tipo: meta`): Preguntas Abiertas y los registros no son entidades, y el validador las salta.

## Motor de generación
- [x] **`expandir-mundo`:**
  - selector según el estado del mundo, que empieza creando el foco de la Ficha;
  - tablas con pesos y oráculos;
  - ingredientes derivados del canon;
  - paquetes;
  - registro y un commit por ciclo;
  - límite de borradores sin revisar;
  - modo prueba en una rama aparte.
- [x] **Lo insólito:** chispas raras (una de cada tres creaciones) con su grado de verdad, contrastes, conexiones inesperadas y rarezas en todas las tablas.
- [x] **Profundizar:** una nota en borrador que nombran muchas notas (3 piden relevancia 3; 6, relevancia 4; 10, relevancia 5), o cuya relevancia ya pide secciones que no tiene, gana las secciones que le faltan sin reescribir lo escrito (`--deepen-chance`, 0.25). El mundo crece en extensión y en profundidad.
- [ ] **Conectar:** lo que debería estar unido por una ruta y no lo está (vecinos sin camino, lo importante de una región sin camino a su capital, regiones vecinas sin ruta, lugares a los que no llega nada; `routes.py --unconnected`) se une con una ruta nueva (`--connect-chance`, 0.2, que baja con la densidad como la de crear algo nuevo). Una ruta suelta llega anclada a lo que más necesita unirse. Hecha; se tilda cuando se pruebe en una tanda del motor.
- [x] **Canon de base primero:** los enlaces pendientes que nombra la Ficha o que nombran tres notas o más (como el conflicto central) se crean antes que los demás, con el mismo nombre del enlace.
- [ ] **Más tablas y paquetes,** a medida que lleguen los módulos.
- [ ] **Tablas propias de cada mundo** en su `06_Generacion/Tablas`, propuestas a partir de su Ficha.

## Mapas
Además del concept art (que sigue siendo obligatorio y la primera imagen de la nota), los lugares que lo merecen tienen mapa. **El mapa no es la imagen: es la leyenda numerada de la nota.** La imagen es una *edición* de esa leyenda; el mundo crece en la leyenda y el dibujo se rehace cuando ha cambiado bastante.

- **Qué lleva mapa** (`mapa` en `modulo.json`: clase, categorías y relevancia mínima):

  | Entidad | Mapa | Desde |
  |---|---|---|
  | lugar: ruina, mazmorra, cueva, pecio, fortaleza, templo, torre, zona peligrosa, explotación (mina, cantera) | plano de interior, por niveles | relevancia 2 |
  | lugar: edificio, posada, mercado, puerto, taller, residencia | plano de interior | relevancia 3 |
  | lugar: isla, bosque, montaña, desierto, agua, paraje | mapa de paraje | relevancia 4 |
  | asentamiento: metrópoli, ciudad, villa | plano urbano | relevancia 3 |
  | asentamiento: aldea, caserío, campamento, refugio, colonia, estación, otro | plano urbano | relevancia 4 |
  | región | mapa de territorio | relevancia 4, y la imagen cuando hay al menos 5 zonas que situar |
  | el mundo | mapa del mundo | a pedido y en `finalizar-mundo` |

- **La leyenda** (sección `## Mapa`): `- **N.** **Nombre** · <orientación> — una línea. Conecta con 2 y 5.` (una viñeta con el número en negrita, porque Obsidian renumera las listas numeradas al leerlas).
  - Números estables: solo se añaden al final; nunca se renumeran ni se reutilizan (una zona destruida queda marcada).
  - Lo que es una entidad va enlazado (a su nota o como enlace pendiente); lo demás, como texto.
  - Orientación: una de 9 (noroeste, norte, noreste, oeste, centro, este, suroeste, sur, sureste); en una mazmorra, con su nivel (`nivel 2, norte`). Las conexiones son físicas y van en los dos sentidos.
  - Como mucho 12 marcadores por mapa: una mazmorra mayor va por niveles (numeración continua); el detalle de un barrio va en el mapa del barrio, cuando sea un lugar propio.
  - Solo indexa lo que la nota cuenta (en una mazmorra, las salas menores son detalles inventados).
- **Cómo crece:** cada mapa muestra solo su nivel directo (la región, sus asentamientos y lugares; la ciudad, sus barrios y lugares notables; la mazmorra, sus salas), así que un lugar nuevo afecta como mucho al mapa de donde está. Al crearlo, `map_key.py --add` lo añade a la leyenda de ese lugar, «sin cartografiar». Edición nueva con 3 zonas sin cartografiar o más, o con un cuarto de las cartografiadas: la acción `cartografiar` del motor o el usuario. Primero se intenta editar la edición anterior en Gemini; si no sale, se redibuja desde la leyenda. Las ediciones anteriores se conservan.
- **Variedad:** la forma, el tamaño, los niveles o pisos y las zonas (salas, barrios, partes, accidentes) se tiran en `expandir-mundo/assets/Tablas/Mapas.md` con azar real (`roll_tables.py --count`), como semilla que manda lo que cuenta la nota.
- **Lo escondido:** los pasos ocultos (`Paso oculto a 7.`, en las dos zonas) y las trampas (`Trampa: …`) que la nota conoce van en la leyenda y en el mapa, con los símbolos de la Guía Visual (línea de puntos, triángulo); lo que nadie conoce es un secreto y no va en el mapa. Las trampas se tiran combinando mecanismo, disparador, efecto y quién la puso y para qué (unas 9.000 combinaciones), para que no se repitan.
- **Caminos:** dentro de un mapa, las conexiones de la leyenda; entre lugares, las rutas con nota. El bloque «Rutas» de cada leyenda lo deriva de las notas de las rutas `map_key.py --sync-routes` (la zona por la que pasa cada una, en orden, «sigue» donde sale del mapa y «se pierde» donde acaba en nada), conecta sus zonas y cuenta para la edición siguiente; cada ruta se dibuja con el estilo de su categoría. No todo tiene que estar conectado.
- **Estilo:** la Guía Visual del mundo, con una técnica de mapas fija (la general si es sobre papel; si no, se elige una vez entre las de papel). Marcadores: círculo negro con fondo blanco, exactamente los números de la leyenda, una vez cada uno, y ningún otro texto. Formato A4: vertical 3:4 u horizontal 4:3, según la forma del lugar.
- **Comprobación de cada imagen:** la IA la mira toda, no solo los mapas: los elementos de su descripción visual uno por uno, sin texto ni marco, la técnica y el formato (en un mapa, además, cuenta los marcadores y busca repetidos y faltantes, el texto de más y lo característico de cada zona); si falla, pide la corrección en el mismo chat, hasta dos veces. El resultado queda en la nota: en la línea del prompt del concept art y en la de la edición del mapa.
- **Lo anterior, archivado:** al aceptar una imagen, `fetch_download.py keep` la deja con el nombre de siempre y mueve a `02_Activos/Anteriores` la que había (`_ed1` en un mapa, `_v1` en un concept art regenerado) y los intentos descartados (`_descartada`). La nota enlaza lo anterior («Ediciones anteriores» en su sección Mapa, «Versiones anteriores» en su sección Imagen), para volver si lo nuevo no gusta.

Etapas:
- [x] 1. Datos: regla `mapa`, sección `## Mapa`, validación en `check_note` y `check_modules`, `map_key.py`.
- [x] 2. `generar-imagen`: modo mapa (técnica de mapas, plantillas, A4) y comprobación con corrección (también del concept art).
- [x] 3. `crear-entidad`: la leyenda al crear, el mapa tras el concept art y la entrada en la leyenda del lugar donde está.
- [ ] 4. Motor: acción `cartografiar`. Hecha; se tilda cuando se pruebe en una tanda del motor.
- [ ] 5. Las rutas en los mapas que cruzan (con el módulo #21; el bloque «Rutas» ya se probó, falta ver una edición nueva que las dibuje); las rutas no tienen mapa propio; más adelante, el mapa del mundo (con `finalizar-mundo`) y, quizá, un «mapa del director» en el secreto que cambia la planta de un lugar (la sala que nadie conoce).

## Entidades por orden de prioridad
Las últimas entidades (desde la 21) se tildan al terminarlas, con su commit; su prueba queda pendiente aparte, en esta lista, para hacerla cuando estén todas.

**Pruebas pendientes:**
- [ ] `diagnosticar-mundo` con un mundo con contenido: el diagnóstico, `--fix`, y en una copia con cosas atrasadas (una plantilla instalada vieja, una nota sin una propiedad nueva de su tipo, una línea de menos en el `CLAUDE.md` y en una guía), `--templates`, `--migrate` y la fusión del `CLAUDE.md` y las guías con `--details`.
- [ ] `finalizar-mundo` con un mundo de verdad (el de una tanda del motor): el diagnóstico, empezar el cierre, un pilar como misterio, una confirmación rechazada, menores disueltos, el motor en modo cierre (y el error si una creación abre un pendiente), los borradores, un mapa atrasado por una sola zona, cerrar con su resumen, crear con el mundo cerrado (debe fallar) y reabrir.
- [ ] `narrar` con un mundo con contenido: una escena y un relato con personajes y lugares que existen, una crónica que siga a otra en una serie, una que pida usar un secreto, una que choque con el canon (debe avisar) y su ilustración.
- [ ] `consultar-mundo` con un mundo con contenido: preguntas de cada fila de su tabla, una sobre algo pendiente, otra que toque un secreto (con y sin spoilers) y una que no conste.
- [ ] `revisar-mundo` con borradores reales (los de una tanda del motor): una tanda con las cuatro decisiones, una corrección por «Other», un lugar con mapa quitado del mundo (su zona retirada y sus menciones reescritas) y otro archivado para rehacerlo, y el motor creándolo de nuevo.
- [ ] `inicializar-mundo` con un mundo nuevo (en `pruebas/<nombre>/`): uno que sea una sola ciudad, con algo que ya tenga nombre propio, y una tanda corta del motor: el foco como asentamiento completando su enlace, sus barrios y lo de fuera marcado `fuera` sin crearse.
- [x] `ruta` (#21): una región y una ruta entre su capital y otro asentamiento, con el bloque «Rutas» en la leyenda de la región. Tras la prueba, la ruta dejó de tener mapa propio (el itinerario sobraba): se ve en los mapas de lo que cruza, y sus puntos con peso entran en la leyenda de su región.
- [x] `material` (#22): un recurso que la región ya nombra y su mina (categoría `explotacion`, con mapa interior).
- [x] `flora` (#23): una planta que calma una afección y se confunde con una gemela venenosa, con su hábitat y su secreto.
- [x] `obra` (#24): un cantar de relevancia 3 que cuenta un hecho a su manera, con su fragmento, su autor atribuido y su versión enfrentada. Salió con su fragmento, el autor atribuido y en duda, dos versiones enfrentadas y la obra que le responde, y la recíproca en el astro del que trata. Tras la prueba, esa recíproca quedó escrita: de lo que trata, solo la lista quien tiene unas `obras` que lo describen (un astro), nunca un personaje, cuyas `obras` son las que hizo.
- [x] `ecosistema` (#25): con la planta de la prueba de flora, su pieza clave y la reciprocidad con sus zonas, su flora y sus recursos.
- [x] `astro` (#26): un cometa por venir, sin tocar el calendario.
- [ ] El grafo de Obsidian: los marcadores «Grafo sin secretos» y «Grafo completo» (los colores por tipo y los nombres de lejos ya se vieron; las flechas se quitaron porque ensucian).
- [x] Una tanda del motor en modo prueba desde la bóveda limpia (`/expandir-mundo prueba 3 --skip-canon --deepen-chance 0 --map-chance 1 --connect-chance 1`): creó el foco (la región, con su paisaje y su mapa, 9/9 marcadores), completó su gran ruta (con su secreto y una imagen corregida, la descartada archivada) y una obra que la ruta nombraba. Todo coherente y el auditor, a cero. Tras la prueba: un enlace pendiente que también nombraba una propiedad que admite cualquier tipo (el `afecta_a` de un secreto) se quedaba sin módulo y bloqueado; los secretos se cuentan aparte en todas partes (auditor, registro, informe, Estadísticas y densidad del motor); el informe dice de qué carpeta es cada README; y una corrección de una imagen que salió bien va al informe, no a la nota.
- [ ] `conectar` y `cartografiar` en una tanda: en 3 rondas desde cero no llegan (`conectar` necesita un lugar con nota sin camino, y `cartografiar`, 3 elementos sin dibujar en el mapa de la región). Hace falta una tanda más larga, de unas 6 rondas, con las mismas opciones.
- [x] Lo arreglado tras la prueba de las entidades 21-26 que se vio en la de la obra: la comprobación anotada en la imagen (tras la prueba, lo que quedó mal va aparte, en «con fallos», y no mezclado con lo comprobado), el intento descartado archivado por `keep` en `02_Activos/Anteriores` sin enlazar, y el secreto marcado aparte (🔒) en el contexto de lo que nombra.
- [x] De lo arreglado, en la tanda del motor: los puntos con peso de una ruta entran en la leyenda de su región (la ruta añadió su punto de partida, «sin cartografiar», y su bloque «Rutas»), y el informe del chat va sin `[[...]]`.
- [ ] Que una edición nueva de un mapa archive la anterior y la enlace en «Ediciones anteriores»: con `cartografiar`, en la tanda larga.

### Fase 1 — Lugares base
- [x] **1. `region` 🗺️ — grandes regiones, territorios políticos y planos.**
  - **Carpeta:** `Grandes_Regiones`, `Paises_y_Territorios` o `Planos_y_Dimensiones`, según la categoría.
  - **Imagen:** paisaje panorámico apaisado (`Lugares`).

### Fase 2 — Canon base
- [x] **2. `fenomeno` 🌫️ — fuerzas y anomalías extraordinarias,** a menudo el conflicto central de un mundo.
  - **Carpeta:** `Fenomenos_Extraordinarios`.
  - **Ficha:** alcance, origen, permanencia, peligrosidad; cómo se manifiesta; reglas y límites; efectos sobre seres, objetos y lugares; zonas afectadas; cómo protegerse; qué se sabe y qué se cree; quién lo estudia o lo explota.
  - **Imagen:** plano atmosférico del fenómeno sobre el paisaje, apaisado (`Escenas`).
- [x] **3. `especie` 🧬 — especies inteligentes.** Si el usuario pide una especie que la Ficha no nombra, se le pregunta antes de crearla.
  - **Carpeta:** `Especies_Inteligentes`.
  - **Ficha:** longevidad (con números, para las edades), tamaño, madurez; anatomía y variaciones; sentidos y capacidades; ciclo vital; psicología típica; culturas que forman; relación con otras especies; origen (mito frente a verdad); distribución; prejuicios.
  - **Imagen:** lámina de concepto de cuerpo entero de un miembro típico, vertical (`Seres`).
- [x] **4. `cultura` 🎭 — pueblos y culturas.**
  - **Carpeta:** `Pueblos_y_Culturas`.
  - **Ficha:** especie, territorio e idioma; identidad y valores; estructura social; vida cotidiana; ritos y festividades; arte; creencias; oficios; forma de hacer la guerra; relación con otros pueblos; migraciones; estereotipos.
  - **Crea su perfil de nombres** en `06_Generacion/Nombres/`, que usará `generate_names.py`.
  - **Imagen:** tres miembros con atuendo tradicional, plano medio, apaisado (`Escenas`).
- [x] **5. `idioma` 🗣️ — idiomas, escrituras y jergas.**
  - **Carpeta:** `Idiomas_y_Escrituras`.
  - **Ficha:** hablantes, familia y escritura; **fonética y patrones de nombres**; gramática esencial; vocabulario básico; frases comunes; dialectos.
  - **Alimenta** los perfiles de nombres de las culturas que lo hablan.
  - **Imagen:** muestra caligráfica de glifos inventados, cuadrado (`Iconos`).
- [x] **6. `calendario` 📅 — calendarios y cómputo del tiempo.**
  - **Carpeta:** `Eras_y_Periodos`.
  - **Ficha:** el año 0 y cómo se escriben los años; meses, semana, estaciones y festividades en tablas que leen los scripts; el día y la noche; historia, uso social y quién lo guarda.
  - **Calendario de referencia:** el eje de la Ficha (uno por mundo). Si el año 0 y el presente están por definir, se le preguntan al usuario y se resuelve el pilar en la Ficha, el `CLAUDE.md`, Preguntas Abiertas y el Registro de Canon (`referencias/pilares.md`, que sirve para cualquier pilar).
  - **Calendarios de cultura:** cada pueblo puede tener el suyo, con su año 0 situado en el eje.
  - **Fecha exacta:** `fecha_exacta` con los nombres del calendario («15 de Siega de 412 UE»), validada por script.
  - **Script:** `world_calendar.py` muestra los calendarios, valida fechas y convierte años.
  - **Imagen:** rueda del calendario con glifos inventados, cuadrado (`Iconos`).
- [x] **7. `era` ⏳ — eras, edades y periodos.**
  - **Carpeta:** `Eras_y_Periodos`.
  - **Ficha:** inicio y fin en el eje del calendario; situación (actual, pasada, legendaria o profetizada) y alcance; qué la define; cómo empezó y cómo terminó; cronología; potencias, pueblos y figuras; cómo se vivía; cómo se la recuerda.
  - **Línea del tiempo:** eras encadenadas y anidadas, que `build_context.py` lista en orden y que `check_note.py` y `audit_world.py` vigilan.
  - **Imagen:** escena alegórica de la era, apaisado (`Escenas`).
- [x] **8. `evento` 📜 — acontecimientos y conflictos.**
  - **Carpeta:** `Guerras_y_Conflictos` o `Acontecimientos`, según la categoría.
  - **Ficha:** fecha, duración, lugar, bandos y resultado; causas; desarrollo por fases con fechas; momentos clave; participantes; consecuencias; cómo se recuerda, con al menos dos versiones enfrentadas.
  - **Tiempo declarativo:** la situación y la cronología se validan con la regla `tiempo` del módulo. El auditor vigila las batallas dentro de su guerra, las causas antes que sus consecuencias y los participantes vivos.
  - **Imagen:** escena dramática del momento clave, apaisado (`Escenas`).

### Fase 3 — Lugares y poder
- [x] **9. `asentamiento` 🏘️ — ciudades, villas, aldeas, campamentos y estaciones** (familia `lugar`).
  - **Carpeta:** `Ciudades_y_Asentamientos`.
  - **Ficha:** categoría, población, situación, fundación y abandono; aspecto al llegar, barrios, gobierno y ley, economía, defensas, gente, lugares y personajes notables, vida cotidiana, historia, problemas y tensiones.
  - **Completa** el lugar de nacimiento, la residencia y la ubicación de los personajes, la capital y los asentamientos de una región, el territorio de un pueblo y los vecinos.
  - **Motor:** se crea desde cero dentro del foco (una ciudad grande o una capital nueva, `Confirmar`), con su tabla y sus paquetes.
  - **Imagen:** plano general desde el camino de llegada, apaisado (`Lugares`).
- [x] **10. `lugar` 📍 — edificios, sitios, ruinas, mazmorras y parajes** (familia `lugar`).
  - **Carpeta:** `Lugares_y_Estructuras`, `Ruinas_y_Zonas_Peligrosas` o `Geografia_y_Clima`, según la categoría.
  - **Ficha:** ubicación, dueño, ocupantes, situación, construcción y abandono; exterior; recorrido por zonas; actividad; peligros y defensas; tesoros y recursos; accesos; historia.
  - **Motor:** se crea desde cero en el foco, con su tabla y sus paquetes.
  - **Imagen:** su vista más emblemática, por fuera o por dentro, apaisado (`Lugares`).
- [x] **11. `faccion` 🛡️ — organizaciones, gobiernos e instituciones.**
  - **Carpeta:** `Gobiernos_y_Estados`, `Facciones_y_Organizaciones` o `Instituciones_y_Linajes`, según la categoría.
  - **Ficha:** sede, líder, miembros, fundación, lema; propósito (lo que dicen y lo que buscan de verdad); doctrina y costumbres; estructura y rangos; miembros notables; recursos e influencia; métodos; símbolos; aliados y enemigos; historia.
  - **Campos para el motor:** `objetivo`, `recursos` (del 1 al 5) y `rivales`.
  - **Imagen:** emblema o estandarte, cuadrado (`Iconos`).
- [x] **12. `objeto` 🗝️ — artefactos, armas, herramientas, vehículos, prendas, consumibles y monedas,** como pieza única o como tipo de objeto.
  - **Carpeta:** la de `60_Objetos_y_Recursos` que corresponda a la categoría.
  - **Ficha:** rareza, valor, material, tamaño; aspecto; uso; propiedades especiales con sus límites y su precio; origen; poseedores; dónde está y quién lo busca; variantes.
  - **Imagen:** el objeto solo, centrado, cuadrado (`Objetos`).
- [x] **13. `creencia` 🕯️ — religiones, cultos e ideologías.** La nota cuenta lo que creen sus fieles, nunca si tienen razón.
  - **Carpeta:** `Creencias_y_Religiones`.
  - **Ficha:** fieles, centro, fundación; doctrina; deidades o principios; culto y rituales; clero; lugares sagrados; símbolos y textos; festividades; moral; herejías; relación con el poder.
  - **Imagen:** símbolo sagrado, cuadrado (`Iconos`).
- [x] **14. `deidad` ✨ — dioses y entidades superiores.** Encaja con el pilar de las entidades superiores de la Ficha; la verdad, si se decide, va en un secreto.
  - **Carpeta:** `Deidades_y_Entidades`.
  - **Motor:** solo desde enlaces pendientes (`crear_desde_cero: false`); si no la pidió el usuario, `Confirmar`.
  - **Imagen:** figura de cuerpo entero tal como la imaginan sus fieles, vertical (`Personajes`).
- [x] **15. `linaje` 🌳 — casas nobles, dinastías, clanes y familias.**
  - **Carpeta:** `Instituciones_y_Linajes`.
  - **Ficha:** categoría, situación, alcance, lema y `poder`; origen y árbol familiar; sucesión con su disputa; rasgos y tradiciones; posesiones, símbolos, alianzas y enemistades; historia.
  - **La prueba dejó dos reglas:** quien sostiene el conflicto o un gancho de la nota (un testigo, una reliquia, un antepasado conocido por su apodo) va enlazado, y toda mención va enlazada, no solo la primera.
  - **Imagen:** blasón o marca de familia, cuadrado (`Iconos`, `Blason_`).

### Fase 4 — Naturaleza y amenazas
- [x] **16. `afeccion` 🦠 — enfermedades, plagas, mutaciones, corrupciones y adicciones.**
  - **Carpeta:** `Enfermedades_y_Afecciones`.
  - **Reglas:** fases, contagio, un remedio a medias, uno falso y un misterio. Nada gráfico.
  - **La prueba dejó dos ajustes:** una confirmación solo bloquea su sujeto, y el registro puede concretar el módulo dentro de una familia (`--set X=region`).
  - **Imagen:** lámina de estudio de sus señales, cuadrado (`Laminas`, `Afeccion_`); técnica sugerida: `codice`.
- [x] **17. `criatura` 🐺 — monstruos, bestias y fauna.** Nunca un pueblo encubierto: si habla y tiene cultura, es una especie.
  - **Carpeta:** `Fauna` o `Criaturas_y_Monstruos`.
  - **Ficha:** anatomía y comportamiento; capacidades y debilidades (una real y una creencia falsa); señales de su presencia; cómo se caza, se evita o se domestica; lo que se obtiene de ella; origen y avistamientos.
  - **La prueba dejó un ajuste:** una referencia con nombre común («la ciudad», «la tormenta») no es una mención por su nombre y no se enlaza.
  - **Imagen:** cuerpo entero en su hábitat, apaisado (`Seres`, `Criatura_`).

### Fase 5 — Reglas y cultura profunda
- [x] **18. `sistema` ⚙️ — sistemas de poder, tecnología, leyes del universo y conceptos.**
  - **Carpeta:** `Sistemas_de_Poder`, `Tecnologia`, `Leyes_del_Universo` o `Conceptos_Fundamentales`, según la categoría.
  - **Ficha:** reglas y límites (al menos dos límites duros), costes y riesgos, uso y aprendizaje, manifestaciones, quién lo controla, impacto en la sociedad, lo que se sabe y lo que se cree.
  - **Los pilares mandan:** los de poderes y tecnología de la Ficha. Las reglas comunes van en una raíz, y cada tradición es una rama.
  - **La prueba dejó tres ajustes:** el sistema no se llama como la fuerza que mueve (el auditor avisa de un nombre que el Glosario registra como entidad y como término), el validador salta las notas internas y el registro concuerda en singular.
  - **Imagen:** el poder, la técnica o la ley en uso, con su efecto y su precio, apaisado (`Escenas`, `Sistema_`).
- [x] **19. `mito` 📖 — mitos, leyendas, profecías, cuentos y rumores.** La nota cuenta lo que se cree, nunca si es cierto; la verdad va en un secreto.
  - **Carpeta:** `Mitos_y_Leyendas`.
  - **Ficha:** el relato con la voz de quien lo cuenta, sus versiones, qué enseña o justifica y a quién le conviene, cómo se cuenta, su huella en el mundo, lo que se sabe y lo que se cree.
  - **Profecías:** `cumplimiento` y `plazo`, que solo valen en ellas (regla `solo_si`). El auditor avisa de una profecía pendiente con el plazo vencido.
  - **La prueba dejó dos ajustes:** el validador acepta un relato citado en varios párrafos, y el detector cuenta como mención de otra entidad un nombre que la nota usa para enlazarla, aunque coincida con su propio título.
  - **Imagen:** la escena clave del relato tal como la imaginan quienes lo cuentan, apaisado (`Escenas`, `Mito_`); técnicas sugeridas: `tapiz` o `manuscrito`.
- [x] **20. `costumbre` 🎉 — leyes de los pueblos, tradiciones, festividades, ritos de paso, tabúes y normas de trato.** Probado con un tabú de relevancia 2.
  - **La prueba dejó un ajuste:** los scripts encuentran la bóveda aunque se ejecuten desde la carpeta de una skill (`vault_path`, que la busca en los directorios superiores).
  - **Carpeta:** `30_Sociedad_y_Cultura/Leyes_y_Costumbres`.
  - **Ficha:** en qué consiste (paso a paso, con gestos, objetos y comidas); cuándo y dónde; quién participa; qué significa para quien la sigue (nunca si funciona); normas y castigos (`rigor`, del 1 al 5); cómo se vive; variantes; quién la defiende y quién la discute; origen e historia.
  - **Festividades y calendario:** una festividad lleva su `calendario` y su `fecha` («15 de <Mes>» o una regla movible), la misma de la tabla «Festividades» del calendario; `check_note.py` avisa si no coinciden. Completa las `festividades` del calendario y las `costumbres` del mito.
  - **Recíproca** con los pueblos y las creencias (que ganan la propiedad `costumbres`), los mitos, el calendario y sus costumbres relacionadas.
  - **Motor:** tabla `Costumbre.md` (categorías que se combinan) y los paquetes «Fiesta de un pueblo» y «Ley y quien la impone».
  - **Imagen:** la costumbre en plena práctica, en su momento más reconocible, apaisado (`Escenas`, `Costumbre_`).
- [x] **21. `ruta` 🧭 — caminos, sendas, pasos, rutas por agua, por aire o bajo tierra, rutas espaciales y portales** (familia `lugar`).
  - **Carpeta:** `Rutas_y_Conexiones`.
  - **Ficha:** qué une o adónde no lleva; el recorrido por tramos, con sus días; cómo se recorre (temporada, peaje, salvoconducto, el rito del portal); quién la recorre y qué lleva; peligros y controles; atajos y desvíos; historia.
  - **Trazado:** `lineal` (une su partida y su destino), `sin_salida` (los senderos que no llevan a ninguna parte), `circular` y `red` (con sus ramales). **Situación** (en uso, en declive, cortada, abandonada, perdida, en construcción) y **certeza** (cierta o dudosa: la ruta que solo cuenta un texto antiguo, con su fuente).
  - **Tiempos de viaje como datos:** `dias` y `medio`, y la tabla Recorrido con los días de cada tramo, que valida `check_note.py`. Con ellos, `routes.py` arma el grafo de distancias: las rutas de un lugar, el camino más rápido entre dos y lo que debería estar unido y no lo está. `build_context.py` da a cada lugar sus rutas y lo más cercano, y a cada ruta, cuánto se tardaba sin ella.
  - **Mapas:** sin mapa propio (el itinerario se quitó tras la prueba: sobraba). La ruta se ve en los mapas de las regiones que cruza (bloque «Rutas»), y sus puntos con peso (la ciudad de su destino) entran en la leyenda de su región.
  - **Motor:** tabla `Ruta.md`, paquetes y la acción `conectar`, que une lo que debería estar unido.
  - **Imagen:** vista a lo largo de la ruta, con viajeros, apaisado (`Lugares`, `Ruta_`).

  Etapas: [x] 1. módulo, recorrido, grafo y contexto · [x] 2. mapas (el bloque «Rutas» en las leyendas) · [x] 3. motor (tabla `Ruta.md`, ocho paquetes y la acción `conectar`). Su prueba, en «Pruebas pendientes».

### Fase 6 — Detalle del mundo
- [x] **22. `material` 💎 — metales, piedras, gemas, cristales, maderas, materias de seres vivos, sustancias, compuestos exóticos y recursos de la tierra.**
  - **Carpeta:** `Minerales_y_Materiales_Naturales` (las materias) o `Recursos_Naturales` (agua, suelo, energía, alimento), en `50_Naturaleza`, según la categoría. Lo procesado (el lingote, la tela) es un objeto.
  - **Ficha:** cómo es y cómo se reconoce; dónde se encuentra; cómo se saca y se trabaja; usos; propiedades extraordinarias (solo si las tiene, según su sistema); riesgos; comercio (valor, quién compra y vende, por dónde viaja, falsificaciones); lo que se cree; historia. `naturaleza`, `rareza` (hasta `legendario`, con sus fuentes), `situacion` (de en explotación a agotado o prohibido) y `peligrosidad`.
  - **Conexiones:** recíproco con sus yacimientos (región, asentamiento y lugar ganan `recursos`), sus criaturas y sus sistemas (`materiales`, que ya existían), sus objetos (el objeto gana `materiales`) y sus rutas (`mercancias`). El lugar gana la categoría `explotacion` (minas, canteras, salinas), con mapa interior desde relevancia 2 y su tabla de labores.
  - **Motor:** tabla `Material.md` y cinco paquetes (mina y su gente, fiebre del metal, materia prohibida, lo que vale una bestia, el agua de todos).
  - **Imagen:** lámina de espécimen, en bruto y trabajado (`Laminas`, `Material_`); técnica sugerida `codice`.
- [x] **23. `flora` 🌿 — árboles, arbustos, hierbas, trepadoras, cultivos, hongos y plantas del agua.**
  - **Carpeta:** `50_Naturaleza/Flora`. Lo que se saca de ella (la madera, la resina) es un material; el preparado, un objeto.
  - **Ficha:** cómo es y cómo se reconoce (y con qué se confunde: la gemela que mata); dónde y cómo crece, con su ciclo; usos y cómo se prepara; peligros; cultivo y recolección; propiedades extraordinarias (solo si las tiene); lo que se cree; historia. `naturaleza`, `uso`, `situacion` (hasta `legendaria`, con sus fuentes) y `peligrosidad`.
  - **Conexiones:** recíproca con su hábitat (región y lugar ganan `flora`), sus materiales (`plantas`) y sus parientes.
  - **Motor:** tabla `Flora.md` y cuatro paquetes (remedio del monte, la cosecha, veneno de la casa, bosque vivo).
  - **Imagen:** lámina botánica, la planta entera y sus partes (`Laminas`, `Flora_`); técnica sugerida `codice`.
- [x] **24. `obra` 🎨 — textos, documentos, poemas, canciones, representaciones, pinturas, esculturas y mapas del mundo.**
  - **Carpeta:** `30_Sociedad_y_Cultura/Arte_y_Expresion`. La obra es lo que dice o muestra; un ejemplar que importa como cosa es un objeto.
  - **Ficha:** qué es; lo que dice, con **un fragmento** con su voz; quién la hizo y por qué; cómo se recibe (lecturas enfrentadas, quién la persigue); ejemplares y versiones; historia. Cuenta su versión de los hechos, no la verdad. `autoria` (conocida, atribuida, anónima, colectiva), `difusion` y `situacion` (de viva a perdida o destruida).
  - **Conexiones:** recíproca con sus autores (el personaje gana `obras`), sus creencias (la creencia gana `textos`) y sus mitos, idiomas y sistemas (`obras`, que ya existían); `trata_de` de cualquier tipo. Es la fuente natural de las rutas, los materiales y las plantas legendarios.
  - **Motor:** tabla `Obra.md`, cuatro paquetes (el libro prohibido, cantar de gesta, crónicas enfrentadas, el mural del templo) y la ruta del texto antiguo con su texto.
  - **Imagen:** la obra misma (el mural, la estatua, el mapa) o su interpretación (la canción cantada, el libro abierto), apaisado (`Escenas`, `Obra_`).
- [x] **25. `ecosistema` 🌲 — biomas y ecosistemas** (familia `lugar`, `contenedor: false`).
  - **Carpeta:** `50_Naturaleza/Ecosistemas`. No es un sitio concreto (eso es un lugar), sino el sistema vivo que se da en uno o en varios.
  - **Ficha:** cómo es; la vida, con **quién come a quién** y **su pieza clave**; cómo se vive en él; peligros; equilibrio y cambios (lo que lo amenaza, si cae su pieza clave); historia. `naturaleza`, `alcance`, `situacion` (de estable a desaparecido) y `peligrosidad`.
  - **Conexiones:** recíproco con sus zonas (región y lugar ganan `ecosistemas`), su flora y sus criaturas (`habitat`), sus recursos (`yacimientos`) y sus fenómenos (`zonas_afectadas`). Completa hábitats, zonas y yacimientos que describen un tipo de tierra.
  - **`contenedor: false`** (nuevo en `modulo.json`, también en la ruta): un tipo de la familia `lugar` que no contiene a otros no es el foco del mundo ni la región de nadie.
  - **Motor:** tabla `Ecosistema.md` y tres paquetes (tierra viva, el equilibrio roto, los que viven de la tierra).
  - **Imagen:** paisaje del bioma, con su vida, apaisado (`Lugares`, `Ecosistema_`).
- [x] **26. `astro` 🌙 — soles, lunas, planetas, estrellas, constelaciones, cometas, fenómenos del cielo y la forma del cielo.**
  - **Carpeta:** `70_Sistemas_y_Cosmologia/Cosmos_y_Astros`. Como se ve desde el mundo; un mundo que se visita o se habita es una región.
  - **Ficha:** cómo se ve; su ciclo y lo que rige; lo que se sabe (con la técnica del mundo) y lo que se cree, por separado; en la cultura; historia. `naturaleza`, `visibilidad`, `situacion` (de estable a desaparecido, o por venir: el cometa que se espera) y `ciclo`.
  - **Conexiones:** recíproco con sus calendarios (el calendario gana `astros`), sus deidades (la deidad gana `astros`), su astro central y sus satélites (`orbita`, `satelites`) y sus astros relacionados.
  - **Motor:** no se crea desde cero (`crear_desde_cero: false`): el cielo es la base de calendarios, fes y mitos. Tabla `Astro.md` para completar los que ya nombran las notas; sin paquetes.
  - **Imagen:** el astro sobre un paisaje del mundo, como se ve desde él, apaisado (`Escenas`, `Astro_`).

### Hechos desde el principio
- [x] `personaje` 👤 — individuos con nombre propio.
- [x] `secreto` 🔒 — verdades ocultas (en `80_Secretos`).

## Skills futuras
- [ ] **`finalizar-mundo`.** Hecha; se tilda cuando se pruebe con un mundo de verdad. Lleva un mundo a su cierre y lo deja impecable. Las decisiones del usuario:
  - **Tres estados** (`estado_mundo`, en la Ficha): `abierto`, `en_cierre` (el mundo ya no crece: ninguna nota abre enlaces pendientes nuevos, el motor solo completa y dibuja, `crear-entidad` solo completa) y `cerrado` (no se crea nada). El bloqueo va en el arranque de los generadores (`report.py --snapshot`) y en el selector; reabrir deja constancia.
  - **Cerrado sigue permitiendo** consultar, narrar e ilustrar.
  - **Los pendientes menores** (los nombra una sola nota, poco y sin peso) se proponen para disolver (`dissolve_link.py`: pasan a texto en todas las notas y salen de las propiedades; quedan como término del Glosario; una línea en el Registro de Canon); el resto se crea, y lo que es otro nombre se fusiona.
  - **Para cerrar, todo** (`close_world.py`): sin pilares por definir ni preguntas abiertas (pueden quedar misterios a propósito), sin pendientes ni borradores, cada nota impecable (check_note sin errores ni avisos y sin anotaciones de trabajo: «por definir», «por confirmar», «sin cartografiar», restos de plantilla), el auditor limpio, todas las imágenes, todos los mapas al día (sin un solo cambio por dibujar, más estricto que la regla de siempre) y lo más alto del mapa con el suyo, sin imágenes sueltas (se apartan como `_suelta`) ni notas en la Bandeja de Entrada.
  - **Al cerrar,** el resumen del mundo terminado (de las Estadísticas) y lo que hizo el cierre (lo que pasó a canon, se archivó, se quitó o se disolvió, y cómo se cerraron las preguntas).
  - Las fases: el diagnóstico, los pilares, las confirmaciones y las preguntas, los pendientes, los borradores (`revisar-mundo`), las notas y el auditor, las imágenes y los mapas, lo suelto y el cierre. Siempre empieza por la lista y sigue por el primer criterio en rojo.
- [ ] **`diagnosticar-mundo`.** Hecha; se tilda cuando se pruebe. La salud de la bóveda, con las comprobaciones que comparte con `finalizar-mundo` (`health.py`, en `crear-entidad`), pero con el criterio de un mundo abierto:
  - **Salud:** las notas (`check_note`, sin contar las propiedades nuevas de su tipo), las imágenes rotas o sueltas y los errores del auditor.
  - **Al día con las skills:** el `CLAUDE.md` y las guías frente a su plantilla de `inicializar-mundo` (las líneas que les faltan, sin las reglas de contenido ni lo que sale de la entrevista), las plantillas instaladas, las propiedades nuevas de cada tipo en las notas, la Ficha (`estado_mundo`), el grafo, las notas del sistema (Bitácora, Estadísticas, registro), los archivos del motor y las skills instaladas.
  - **Atención:** borradores, enlaces pendientes, preguntas, pilares, mapas por dibujar, imágenes que faltan, avisos del auditor y la Bandeja de Entrada, con la skill que lo resuelve.
  - **Arreglos:** `--fix` (los seguros, sin preguntar), `--templates`, `--migrate` (con el mundo cerrado, no) y `--tidy` (con visto bueno); el `CLAUDE.md` y las guías los incorpora Claude con lo que muestra `--details`. Solo añaden o rehacen lo que mantienen las skills, y dejan su entrada en la Bitácora; sin opciones, no cambia nada.
- **Ideas para más adelante** (sin decidir):
  - `preparar-partida`: material para rol (sesiones, encuentros, ganchos) si el mundo se usa para jugar;
  - `exportar-mundo`: un compendio del mundo (PDF, web o wiki);
  - cronologías y genealogías generadas a partir de eventos, linajes y personajes.

## Al cerrar el proyecto
- [x] Repositorio propio (`skills-world-building`) y primer README.
- [ ] Elegir una licencia, para que quede claro cómo se puede usar.
- [ ] README final: cada skill, con ejemplos.
- [ ] Una última revisión de que no quede nada de un mundo concreto en las skills.

## Fuera de esta lista
- **Relación como entidad propia:** se diseña cuando el motor pida relaciones ricas.
- **Economía y comercio:** se cubre con facción, objeto, ruta y costumbre.
- **Vistas de tarjetas con imágenes** en los índices (Bases).
