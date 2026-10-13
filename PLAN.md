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
- [ ] **`inicializar-mundo` a fondo:**
  - mejores preguntas, con una ronda para lo que el usuario ya tiene con nombre propio (especies, pueblos, lugares, facciones, dioses);
  - identificar las entidades de sus respuestas y confirmarle el tipo de cada una;
  - una Ficha que nazca con esas entidades enlazadas como enlaces pendientes con su tipo, para que el motor empiece por ellas;
  - revisar la estructura y el `CLAUDE.md` que genera.

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
- [x] **Bitácora del mundo** (`00_Sistema/Bitacora.md`), probada con una mazmorra: la crónica para el autor, de lo más reciente a lo más antiguo. La crea `inicializar-mundo` con la creación del mundo; `report.py --log` añade la entrada de cada creación, profundización o tanda (con sus ciclos y la remisión al Registro de Generación); `log_entry.py`, las sueltas (una imagen o un mapa aparte, un cambio pedido fuera de las skills). Las notas que existen van enlazadas y los enlaces pendientes, como texto; la Bitácora no cuenta para los enlaces pendientes y la IA nunca la lee.
- [x] **Imágenes con Gemini en Chrome:** `generar-imagen` genera con Gemini en el navegador del usuario y mueve la descarga a la bóveda con `fetch_download.py`. Se probó Puter por API y se descartó por su límite mensual.
- [ ] **Imágenes por API:** reemplazar la vía del navegador por una API u otra vía más eficiente, que genere por script.
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
  | ruta: camino, sendero, paso, fluvial, marítima, subterránea, aérea, espacial (los portales, no) | itinerario: la franja de tierra a lo largo de la ruta | relevancia 3, y la imagen desde 3 puntos |

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
- **Comprobación de cada imagen:** la IA la mira (en un mapa, cuenta los marcadores y busca repetidos y faltantes, el texto de más y lo característico de cada zona); si falla, pide la corrección en el mismo chat, hasta dos veces, y anota lo que quede mal.

Etapas:
- [x] 1. Datos: regla `mapa`, sección `## Mapa`, validación en `check_note` y `check_modules`, `map_key.py`.
- [x] 2. `generar-imagen`: modo mapa (técnica de mapas, plantillas, A4) y comprobación con corrección (también del concept art).
- [x] 3. `crear-entidad`: la leyenda al crear, el mapa tras el concept art y la entrada en la leyenda del lugar donde está.
- [ ] 4. Motor: acción `cartografiar`. Hecha; se tilda cuando se pruebe en una tanda del motor.
- [ ] 5. Las rutas (con el módulo #21: el itinerario y las rutas en los mapas que cruzan; hecho, se tilda con su prueba); más adelante, el mapa del mundo (con `finalizar-mundo`) y, quizá, un «mapa del director» en el secreto que cambia la planta de un lugar (la sala que nadie conoce).

## Entidades por orden de prioridad
Las últimas entidades (desde la 21) se tildan al terminarlas, con su commit; su prueba queda pendiente aparte, en esta lista, para hacerla cuando estén todas.

**Pruebas pendientes:**
- [ ] `ruta` (#21): una región y una ruta entre dos de sus asentamientos (el itinerario y el bloque «Rutas» de la leyenda de la región), y la acción `conectar` en una tanda del motor.
- [ ] `material` (#22): un material de relevancia 3 con su yacimiento (una mina, que lleva mapa interior) y la reciprocidad con la región y los objetos.

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
  - **Mapas:** el itinerario de la ruta (la franja de tierra a lo largo del camino) y las rutas en los mapas de las regiones que cruzan.
  - **Motor:** tabla `Ruta.md`, paquetes y la acción `conectar`, que une lo que debería estar unido.
  - **Imagen:** vista a lo largo de la ruta, con viajeros, apaisado (`Lugares`, `Ruta_`).

  Etapas: [x] 1. módulo, recorrido, grafo y contexto · [x] 2. mapas (itinerario y bloque «Rutas» en las leyendas) · [x] 3. motor (tabla `Ruta.md`, ocho paquetes y la acción `conectar`). Su prueba, en «Pruebas pendientes».

### Fase 6 — Detalle del mundo
- [x] **22. `material` 💎 — metales, piedras, gemas, cristales, maderas, materias de seres vivos, sustancias, compuestos exóticos y recursos de la tierra.**
  - **Carpeta:** `Minerales_y_Materiales_Naturales` (las materias) o `Recursos_Naturales` (agua, suelo, energía, alimento), en `50_Naturaleza`, según la categoría. Lo procesado (el lingote, la tela) es un objeto.
  - **Ficha:** cómo es y cómo se reconoce; dónde se encuentra; cómo se saca y se trabaja; usos; propiedades extraordinarias (solo si las tiene, según su sistema); riesgos; comercio (valor, quién compra y vende, por dónde viaja, falsificaciones); lo que se cree; historia. `naturaleza`, `rareza` (hasta `legendario`, con sus fuentes), `situacion` (de en explotación a agotado o prohibido) y `peligrosidad`.
  - **Conexiones:** recíproco con sus yacimientos (región, asentamiento y lugar ganan `recursos`), sus criaturas y sus sistemas (`materiales`, que ya existían), sus objetos (el objeto gana `materiales`) y sus rutas (`mercancias`). El lugar gana la categoría `explotacion` (minas, canteras, salinas), con mapa interior desde relevancia 2 y su tabla de labores.
  - **Motor:** tabla `Material.md` y cinco paquetes (mina y su gente, fiebre del metal, materia prohibida, lo que vale una bestia, el agua de todos).
  - **Imagen:** lámina de espécimen, en bruto y trabajado (`Laminas`, `Material_`); técnica sugerida `codice`.
- [ ] **23. `flora` 🌿 — plantas y hongos.** Carpeta `Flora`; imagen: lámina botánica (`Laminas`), técnica sugerida `codice`.
- [ ] **24. `obra` 🎨 — obras, canciones, textos y documentos del mundo.** Carpeta `Arte_y_Expresion`; imagen: la obra o su interpretación (`Escenas`).
- [ ] **25. `ecosistema` 🌲 — biomas y ecosistemas** (familia `lugar`). Carpeta `Ecosistemas`; imagen: paisaje del bioma, apaisado (`Lugares`).
- [ ] **26. `astro` 🌙 — cuerpos celestes y fenómenos del cielo.** Carpeta `Cosmos_y_Astros`; imagen: el astro sobre un paisaje nocturno, apaisado (`Escenas`).

### Hechos desde el principio
- [x] `personaje` 👤 — individuos con nombre propio.
- [x] `secreto` 🔒 — verdades ocultas (en `80_Secretos`).

## Skills futuras
- [ ] **`finalizar-mundo`**, cuando estén todas las entidades. Lleva un mundo a un estado cerrado:
  - recorre los enlaces pendientes y, en cada uno, crea la entidad o lo disuelve (si no merece nota, queda como texto o como término del Glosario) hasta que no quede ninguno;
  - resuelve con el usuario las confirmaciones y las preguntas abiertas;
  - completa las imágenes que falten y deja el auditor sin errores ni avisos;
  - cierra con un informe del mundo terminado.

  Queda por decidir cómo se reparte en tandas (con presupuesto y por prioridad, como el motor) y si ofrece un modo de solo revisión.
- **Ideas para más adelante** (sin decidir):
  - `revisar-mundo`: repasar los borradores con el usuario, por tandas, y promoverlos a canon o archivarlos;
  - `consultar-mundo`: responder preguntas sobre el mundo con los scripts de consulta, sin leer la bóveda;
  - `narrar`: relatos, escenas o crónicas ambientados en el mundo, coherentes con el canon;
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
