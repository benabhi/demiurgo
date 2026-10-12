---
name: crear-entidad
description: Crea entidades del mundo (personajes, regiones, secretos y los tipos que se vayan añadiendo) como notas en la bóveda de Obsidian, con el desarrollo que pide su relevancia, coherentes con la Ficha del Mundo y las convenciones del proyecto, con su imagen. Úsala para "crea un personaje…", "crea la región…", "/crear-entidad <tipo> …", para completar un enlace pendiente (un hueco: una entidad que otra nota ya nombra y que aún no tiene nota) creándola, o para profundizar una nota que ganó importancia ("profundiza a…"). Cada tipo de entidad es un módulo en tipos/.
---

# Crear entidad

Crea una entidad a partir de un pedido conversacional, de una semilla de atributos o de un enlace pendiente, con la profundidad que pide su relevancia.

Toda entidad que la nota nombra va enlazada: a su nota, si existe, o como **enlace pendiente**, si no. Así el mundo crece desde lo que ya nombra (ver `referencias/huecos.md`).

Uso: `/crear-entidad <tipo> [concepto o atributos]`.

## Leer la bóveda sin gastar tokens
La bóveda puede llegar a tener miles de notas. **Nunca la recorras ni leas carpetas enteras.** Tampoco leas enteros el Glosario, Preguntas Abiertas, el registro de enlaces pendientes ni el índice de entidades, porque crecen con el mundo. Para todo eso hay scripts en `<directorio de esta skill>/scripts/`:
- **Buscar** si algo ya existe, está pendiente, está en el Glosario o tiene preguntas: `search_vault.py "<texto>"`. No distingue tildes ni mayúsculas, y muestra también los nombres parecidos (posibles duplicados). Por tipo: `search_vault.py --type <tipo> [texto]`.
- **Contexto** de lo que vas a crear: `build_context.py --target <nombre>`, que tiene un tope de palabras.
- **Añadir** al Glosario y a Preguntas Abiertas sin leerlos: `add_entries.py --glossary <Término> <Tipo> "[[Nota]]" <Definición>`, `--question <texto>` y `--confirm <texto>`.
- **Vínculos inversos** en otras notas, sin leerlas: `add_relation.py <Nota> <propiedad> <Destino>`.
- **Cambiar un enlace** en toda la bóveda (un nombre de rol por el definitivo): `rename_link.py <Viejo> <Nuevo>`.
- **La leyenda del mapa** de un lugar, sin leer la nota: `map_key.py <Nota>` la muestra con su estado, y `--add` le añade una zona (ver `referencias/mapas.md`).
- **Validar y auditar** solo lo tuyo: `check_note.py <notas>` y `audit_world.py --focus <notas>`.

Lee entera solo la nota que vas a escribir; de las demás, solo lo que el contexto no resuma bien. De una nota larga, lee solo la sección que necesites: búscala con `grep -n "^## <Sección>" <nota>` y lee ese tramo de líneas.

## Tipos disponibles
Cada carpeta de `tipos/` es un módulo con tres archivos:
- `tipo.md`: las reglas del tipo;
- `plantilla.md`: la ficha;
- `modulo.json`, que leen los scripts:
  - `tipo` y `familia` (por ejemplo, `region` es de la familia `lugar`);
  - `completa` (opcional, en módulos de una familia): qué propiedades de otras fichas puede completar (una región completa la `region` de un personaje, no su `residencia`);
  - `emoji`;
  - `huecos_propios`: cuántos enlaces pendientes nuevos puede abrir cada nota (los que solo nombra ella) con relevancia 4 o 5; con menos relevancia, el rango se reduce (ver «Profundidad»);
  - `profundidad`: la relevancia mínima desde la que va cada sección que no es del núcleo (`"Citas": 3`); las que no figuran van siempre;
  - `mapa` (opcional, en los lugares): qué categorías llevan mapa, de qué clase (`interior`, `urbano`, `paraje` o `territorio`), desde qué relevancia y, si hace falta, con cuántas zonas como mínimo para dibujarlo (`zonas_minimas`). Ver `referencias/mapas.md`;
  - `carpeta` (fija, o según una propiedad como el rol o la categoría);
  - `crear_desde_cero` (opcional): `false` si el motor no debe inventar entidades de ese tipo, solo crear las que ya nombra el canon (las especies, por ejemplo);
  - `escalas` y `valores` (opcionales): propiedades numéricas con su rango (`peligrosidad` del 1 al 5) y propiedades con valores permitidos (`naturaleza`, `situacion_vital`), que valida `check_note.py`;
  - `fecha_exacta` (opcional): qué fecha del tipo precisa su propiedad `fecha_exacta`, el día con los nombres del calendario de referencia (en el personaje, su `nacimiento`);
  - `fechas`: sus propiedades de fecha; las dos primeras son el inicio y el fin (`nacimiento` y `muerte`, `inicio` y `fin`, `fundacion` y `abandono`), y `check_note.py` comprueba que el fin no sea anterior al inicio;
  - `tiempo` (opcional, en tipos con situación temporal como la era, el evento o el asentamiento): qué valores de `situacion` son el presente, el pasado y el futuro, y qué tabla es su cronología; `check_note.py` valida con ello sus fechas frente al año actual;
  - `solo_si` (opcional): propiedades que solo se usan con ciertos valores de otra (en el mito, `cumplimiento` y `plazo` solo en las profecías); fuera de esa condición quedan vacías y dentro son obligatorias, salvo las fechas. `check_note.py` lo comprueba;
  - qué tipo o familia de entidad va en cada propiedad de relación.

Módulos disponibles:
- `personaje` 👤 — individuos con nombre propio.
- `region` 🗺️ — grandes regiones, territorios políticos y planos (familia `lugar`).
- `asentamiento` 🏘️ — metrópolis, ciudades, villas, aldeas, campamentos, refugios, colonias y estaciones (familia `lugar`): cómo se ve, quién manda, de qué vive, quién vive allí y qué problemas tiene. Completa los lugares de nacimiento y residencia de los personajes y la capital y los pueblos de una región.
- `lugar` 📍 — sitios concretos (familia `lugar`): edificios (templos, fortalezas, posadas, talleres, torres…), ruinas y zonas peligrosas (mazmorras, pecios, yermos) y parajes naturales (montañas, ríos, bosques, cuevas, islas). Completa las tabernas, templos, faros y escenarios que nombran los asentamientos, las regiones y los eventos.
- `faccion` 🛡️ — gobiernos, consejos, gremios, órdenes, sectas, compañías, ejércitos, bandas, sociedades secretas, movimientos, alianzas e instituciones: qué quieren de verdad, cómo se organizan, con qué cuentan y con quién chocan. Lleva `objetivo`, `recursos` (1 a 5) y `rivales` para el motor.
- `linaje` 🌳 — dinastías, casas nobles, clanes, familias notables y estirpes: de dónde vienen, qué se hereda con el apellido, quién manda y quién heredará (con su disputa), con qué cuentan, sus alianzas y enemistades, y si suben o se hunden. Sus miembros con nota lo llevan en su `linaje`.
- `objeto` 🗝️ — artefactos, reliquias, armas, armaduras, herramientas, vehículos, prendas, joyas, sustancias y monedas, como pieza única o como tipo de objeto: cómo es, para qué sirve, qué tiene de especial (con sus límites y su precio), quién lo hizo, de quién fue y dónde está.
- `creencia` 🕯️ — religiones, cultos, fes populares, filosofías e ideologías: qué enseñan, qué veneran, cómo se practican, quién las administra, sus fiestas, su moral, sus herejías y su relación con el poder. Cuentan lo que creen sus fieles, nunca si tienen razón.
- `deidad` ✨ — dioses, semidioses, espíritus mayores, demonios, ancestros y entidades cósmicas: cómo se la imagina, qué se sabe, qué se cree y qué se discute de ella, sus poderes, su culto y sus manifestaciones. Encaja con el pilar de las entidades superiores de la Ficha; la verdad, si se decide, va en un secreto.
- `cultura` 🎭 — pueblos y culturas: identidad, sociedad, costumbres y su perfil de nombres, que usan sus personajes.
- `idioma` 🗣️ — lenguas, dialectos, jergas, escrituras, señas y códigos: cómo suenan, cómo se escriben, vocabulario y frases. Su fonética alimenta los perfiles de nombres de las culturas que los hablan.
- `especie` 🧬 — especies inteligentes: su biología, longevidad, ciclo vital y relación con las demás. Respeta la regla de especies de la Ficha.
- `afeccion` 🦠 — enfermedades, plagas, mutaciones, corrupciones, maldiciones, adicciones y locuras: cómo se reconocen y avanzan, cómo se transmiten, qué remedios funcionan y cuáles no, el estigma y los casos notables. Recíproca con los fenómenos que la provocan, las especies que la sufren y sus afectados.
- `criatura` 🐺 — fauna, bestias, monstruos, aberraciones, no muertos, espíritus menores y constructos: cómo es, dónde vive, cómo caza, qué puede hacer y qué la frena, las señales de su presencia, cómo se caza o se evita y qué se obtiene de ella. Nunca un pueblo encubierto (eso es una `especie`). Recíproca con su hábitat, los fenómenos que la crean, las afecciones que transmite, las deidades a las que sirve y sus parientes.
- `fenomeno` 🌫️ — fuerzas y anomalías extraordinarias que actúan en el presente (una tormenta perpetua, una zona donde el tiempo se detiene); a menudo, el conflicto central del mundo.
- `sistema` ⚙️ — las reglas profundas del mundo: sistemas de poder (magias, dones y pactos), tecnologías, leyes del universo y conceptos. Qué permite, qué no puede hacer nunca, qué cuesta, cómo se aprende y se usa, quién lo controla y qué cambia en la sociedad. Encaja con los pilares de poderes y tecnología de la Ficha; las tradiciones concretas son ramas de una raíz con las reglas comunes. Recíproco con sus practicantes, sus facciones, sus objetos y sus creencias (`sistemas`).
- `era` ⏳ — eras, edades y periodos de la historia, también los legendarios y los profetizados: cuándo empezaron y terminaron, qué los definió y cómo se recuerdan. Las demás entidades se sitúan en ellas con su propiedad `era`.
- `evento` 📜 — guerras, batallas, catástrofes, fundaciones, tratados, sucesiones y otros hechos con fecha: causas, desarrollo, participantes, consecuencias y sus versiones enfrentadas. Van en `Guerras_y_Conflictos` o en `Acontecimientos`, según su categoría.
- `mito` 📖 — mitos de origen, leyendas, profecías, cuentos populares y rumores: el relato con la voz de quien lo cuenta, sus versiones, qué enseña o justifica, cómo se cuenta y qué huella deja. Cuenta lo que se cree, nunca si es cierto; la verdad va en un secreto. Recíproco con las culturas, las creencias y las deidades que lo cuentan o aparecen en él (`mitos`).
- `calendario` 📅 — cómo se cuenta el tiempo: el año 0, cómo se escriben los años, meses, semana, estaciones y festividades. El de referencia es el eje de la Ficha y da los nombres de las fechas de todas las notas; cada pueblo puede tener el suyo.
- `secreto` 🔒 — verdades ocultas. También se crean como parte de otras entidades.

Si piden un tipo sin módulo, dilo y no lo improvises. Los tipos previstos que ya nombran las relaciones de otros módulos (`pending_links.py` los acepta; hoy, `costumbre`, `ruta`, `material` y `obra`) pueden quedar como enlaces pendientes con su tipo hasta que llegue su módulo.

## Paso 0: preparar
1. Localiza la bóveda (por defecto `World_Building/`). `CLAUDE.md` y la Ficha del Mundo son la fuente de verdad.
2. Lee `tipos/<tipo>/tipo.md`, `tipos/<tipo>/plantilla.md` y `referencias/huecos.md`.
3. **Instantánea para el informe final:** antes de escribir nada en la bóveda, ejecuta `python <directorio de esta skill>/scripts/report.py --snapshot` y guarda la ruta que imprime. Así el informe distingue lo que crea esta skill de los cambios que el usuario ya tenía sin confirmar.
4. **Primer uso del tipo en la bóveda** (no figura en la tabla "Tipos registrados" de la Guía de Organización):
   - Copia `plantilla.md` a `00_Sistema/01_Plantillas/Plantilla_<Tipo>.md` (por ejemplo, `Plantilla_Personaje.md`). Nunca sobrescribas.
   - Añade su fila a "Tipos registrados": `| <tipo> | <carpeta> | Plantilla_<Tipo> | crear-entidad |`.
   - Haz lo mismo con los tipos auxiliares que use (personaje usa `secreto`).
   - Las carpetas nuevas que crees se registran en la tabla "Carpetas añadidas por skills" de la Guía de Organización.
5. Si la plantilla instalada en `01_Plantillas` difiere de la de la skill, menciónalo en el informe final. No la sobrescribas: el usuario pudo personalizarla.

## Paso 1: entrada
- **Conversacional** ("un herrero del puerto"): si falta el concepto, pregúntalo. No preguntes nada más que lo imprescindible.
- **Semilla** (`clave=valor`, normalmente del sistema procedural): respeta los valores dados, rellena el resto y marca `origen: procedural`.
- **Completar un enlace pendiente** (`hueco=<Enlace>`): ejecuta `python <directorio de esta skill>/scripts/find_gaps.py --link <Enlace>` para ver el contexto, el tipo esperado y los módulos que pueden crearlo.
  - La entidad debe encajar con todo lo que dicen las notas que la nombran. Lo que esas notas cuentan de su relación con ella es su punto de vista: si una dice que alguien la teme, no la conviertas en alguien que teme (ver «Relaciones» en el Paso 4).
  - Si el tipo esperado es una **familia** (por ejemplo `lugar`), elige el módulo concreto que encaje con el contexto: una cordillera es una `region`; una taberna no lo es.
  - Si ningún módulo existente encaja (el módulo `asentamiento` aún no existe, por ejemplo), dilo y no fuerces otro tipo.
  - Antes, comprueba con `search_vault.py "<nombre legible>"` que no sea otro nombre de una entidad que ya existe (mira también los nombres parecidos): si lo es, corrige los enlaces en lugar de crear un duplicado.
  - **Con nombre real** (`[[Gran_Sequia]]`, `[[Aldric_Voss]]`): el archivo nuevo se llama **exactamente como el enlace**, para que todos los enlaces existentes la encuentren sin reemplazar nada; el H1 y `aliases` llevan la ortografía real (la del texto del enlace, si lo tiene).
  - **Con nombre de rol** (`<Rol>_de_<Entidad>`, como `[[Madre_de_Aldric_Voss]]`): ponle nombre y, al terminar, reemplaza el enlace en todas las notas (Paso 4).
- **Profundizar una nota** (`profundizar=<Nota>`, con `relevancia=<n>` si cambia; lo pide el motor o el usuario: «profundiza a Aldric», «sube a Aldric a relevancia 4»): la nota ya existe y gana desarrollo. Ver «Profundizar una nota».

## Paso 2: contexto y coherencia
- **Paquete de contexto:** ejecuta `python <directorio de esta skill>/scripts/build_context.py --target <enlace pendiente o entidad principal relacionada>`. Reúne:
  - lo que dicen de ella las notas que la nombran;
  - las entidades relacionadas, con su resumen y ordenadas por relevancia;
  - la cadena de regiones;
  - los nombres ya usados;
  - las preguntas abiertas relacionadas.

  Úsalo en lugar de recorrer la bóveda, y lee entera solo la nota que necesites en detalle.
- **Duplicados:** busca el nombre y el concepto con `search_vault.py`, que mira a la vez las entidades, los enlaces pendientes y el Glosario, también por nombres parecidos.
- Comprueba los pilares de la Ficha y las reglas de contenido de `CLAUDE.md`: especies, tecnología, poderes, tono, crudeza y vetos. Si el pedido los contradice, avisa antes de seguir.
- **Pilares por definir:** si lo que vas a crear necesita uno (el año 0 y el presente, en un calendario), no lo decidas tú: sigue `referencias/pilares.md`.
- **Hechos importantes nuevos:** una civilización, un reino, una facción, una guerra, un acontecimiento histórico o una especie que no estén en el pedido ni en la bóveda.
  - Úsalos solo si el concepto los necesita, como enlaces pendientes.
  - No los registres en el Glosario como hechos establecidos. Si un término inventado depende de un hecho por confirmar (por ejemplo, el nombre de una clase social propuesta), regístralo con "(por confirmar)" en su definición.
  - Anótalos en Preguntas Abiertas con `add_entries.py --confirm "<hecho> (propuesto al crear [[Nota]])"`, uno por hecho; el script escribe `- [ ] Confirmar: …`. El **sujeto** del hecho (la entidad que hay que confirmar, exista o sea un enlace pendiente) va enlazado **primero**: `- [ ] Confirmar: existe el gremio [[Gremio_del_Puerto]] (propuesto al crear [[X]])`, `- [ ] Confirmar: la [[Fiebre_Gris]] la provoca la [[Marea_Roja]] (…)`. Si el sujeto es un enlace pendiente, la confirmación lo bloquea: el motor no lo crea hasta que el usuario decida. Los demás enlaces de la línea son contexto y no se bloquean.
  - Destácalos en el resumen final.

  Así se respeta la autonomía de la Ficha sin detener el flujo.

## Paso 3: crear la nota
- **Relevancia inicial:** la de `tipo.md` según su papel en el mundo. Si ya la nombran varias notas (`find_gaps.py --link` las lista), no baja de lo que pide ese peso: 3 notas, relevancia 3; 6, relevancia 4; 10, relevancia 5. Es la misma regla con la que el motor profundiza, así una nota no nace ya corta.
- **Profundidad según la relevancia.** Decide primero la `relevancia` y ejecuta `python <directorio de esta skill>/scripts/check_note.py --depth <tipo>:<relevancia>` (en un lugar, con su categoría: `--depth lugar:3:mazmorra`): te dice qué secciones lleva la nota, cuántos enlaces pendientes nuevos puede abrir y si le toca mapa.
  - El **frontmatter va siempre completo**, con todas las propiedades de la plantilla, sea cual sea la relevancia.
  - El **núcleo** (las secciones sin relevancia mínima) va siempre. Las secciones de profundidad, solo desde su relevancia. Las que no le tocan se borran de la nota, con su título.
  - Las secciones **opcionales** (las que la `profundidad` del módulo marca con 0, como los ganchos de un idioma) van solo si hay algo real que contar, a cualquier relevancia.
  - **Las cantidades de `tipo.md`** («de 3 a 6 lugares notables», «de 2 a 4 ganchos») son para una nota de relevancia 3 o más. Con relevancia 1 o 2, basta con lo esencial: una o dos entradas donde pide varias.
  - **No inventes para llenar.** En lo que la nota lleva, escribe lo que aporta al mundo: una aldea de relevancia 1 necesita su ubicación, su función y sus vínculos, no una historia épica. Un dato de una tabla o una lista que de verdad no aplica se dice en pocas palabras («ninguna conocida»), no se adorna. Si una sección de profundidad tiene algo real que contar aunque la relevancia no la pida, puede ir.
- Rellena las secciones que lleva siguiendo `tipo.md`. Lo único sin resolver son los enlaces pendientes.
- **Mapa:** si le toca, escribe la leyenda de su sección Mapa con lo que cuenta la nota, como dice `referencias/mapas.md`: hasta 12 zonas por nivel, con su número, su orientación, lo que se ve y sus conexiones. El dibujo se hace en el Paso 6.
- **Toda entidad que nombras lleva enlace, cada vez que la nombras** y no solo la primera, también con su nombre corto (`[[Aldric_Voss|Aldric]]`). Solo quedan sin enlace las menciones de la propia entidad, los títulos y la sección Imagen (ver `referencias/huecos.md`):
  - a su nota, si existe;
  - si no, como enlace pendiente con su nombre real, su texto legible y su tipo. El tipo lo da su propiedad de relación (ponla siempre que haya una); si no la hay, asígnalo en el Paso 4.
  - Lo que es una entidad se enlaza siempre, aunque esté dentro de otra (un cabo, una costumbre de un pueblo) o sea un colectivo («los nueve jueces»). Solo los términos (rangos, títulos, oficios, expresiones…) van al Glosario sin enlace; registrar una entidad en el Glosario, con su tipo de entidad, no la libra del enlace. Los secretos no se enlazan nunca.
- **Cuántos nuevos:** los que dice `check_note.py --depth` (el rango del módulo, reducido según la relevancia). Si el motor indica `enlaces_nuevos`, quédate dentro de los dos rangos; si no se solapan, manda el de la relevancia. Lo menos importante va sin nombre propio («un herrero del puerto»), así no necesita enlace.
- **Reutiliza antes de crear:** si la entidad ya existe, enlaza su nota. Si otra nota ya la nombra como enlace pendiente (búscalo con `search_vault.py "<nombre>" --in pendientes`), usa ese mismo enlace (la frontera de un reino, la capital de una región, el gobierno de un pueblo). Dos enlaces para la misma cosa acabarían siendo dos entidades duplicadas.
- **Nombres:** no los inventes a ojo, porque los modelos repiten patrones. Esto vale también para los de las entidades que dejas pendientes.
  - Genera candidatos con `python <directorio de esta skill>/scripts/generate_names.py --profile <perfil> --count 10` (añade `--surnames` si lleva apellido).
  - Usa el perfil de su cultura si existe: `--profile <Cultura>` encuentra `Nombres_<Cultura>`, que crea el módulo `cultura` (`--list` muestra los disponibles); si no, `Generico`.
  - Elige o adapta uno coherente con la sonoridad de la Ficha. El script ya descarta los nombres usados y los demasiado parecidos.
- Nombre y archivo según la Guía de Nombres. `estado: borrador` y `ultima_revision` con la fecha de hoy, **sin comillas**.
- `relevancia` de 1 a 5 según la Guía de Organización. Las fechas del mundo, como números del calendario (vacías si está por definir). En el texto, si existe el calendario de referencia, las fechas van con sus nombres («15 de Siega de 412 UE»): `build_context.py` lo resume y `world_calendar.py` lo muestra entero.
- Las propiedades de relación solo llevan enlaces; si un dato se desconoce, la propiedad queda vacía y el cuerpo lo explica.
- **`era`** (en los tipos que la tienen): la era a la que pertenece la entidad, la que vivió una persona o en la que surgió un pueblo, una lengua o un lugar. Si ya existe, enlázala (`build_context.py` lista las eras en orden); si no, puede quedar vacía.
- **Enlaces legibles:** en el cuerpo, todo enlace a una nota cuyo archivo lleva guiones bajos lleva su texto real, porque Obsidian mostraría el nombre del archivo: `[[Reino_de_Ejemplo|Reino de Ejemplo]]`, `la [[Capital_de_Reino_de_Ejemplo|capital]]`. En las tablas, `[[Nota\|texto]]`. En las propiedades, el enlace va sin texto.
- Escribe la nota en la carpeta que corresponda según `modulo.json` (fija, o según el rol o la categoría). Nunca sobrescribas una nota existente.

### Profundizar una nota
Una entidad que gana peso en el mundo gana desarrollo: el campesino de ayer puede ser hoy un personaje importante. El motor solo profundiza notas en `borrador`. Una nota `canon` se profundiza solo si lo pide el usuario, porque cambiar su relevancia y su contenido es decisión suya.
1. Lee la nota entera y su contexto (`build_context.py --target <Nota>`), y lo que dicen de ella las notas que la nombran.
2. Si cambia la relevancia, súbela en el frontmatter. Ejecuta `check_note.py --depth <tipo>:<relevancia>`: las secciones que ahora lleva y no tiene son las que hay que escribir.
3. Añade esas secciones **en el orden de la plantilla**, con el mismo cuidado que una nota nueva y siguiendo `tipo.md`. **Lo que ya está escrito no se contradice ni se reescribe:** se construye sobre ello. Solo se amplía una sección existente si lo nuevo lo exige (un gancho que remite a un hecho de su historia).
4. Puede abrir enlaces pendientes nuevos: la diferencia entre el rango de su relevancia nueva y el de la anterior.
5. Sigue con los pasos 4, 5 y 7 (efectos, validar e informe); la imagen ya existe y no se regenera, salvo que se pida. **El mapa sí:** si con la relevancia nueva le toca, escribe su leyenda (es una sección más) y dibuja su primera edición como en el Paso 6.

## Paso 4: efectos en el resto de la bóveda
- **Secretos:** solo si el módulo lo decide (con una tirada) y solo desde relevancia 3: una entidad menor no lleva secreto, salvo que el usuario o el concepto lo pidan. Crea cada uno como nota del tipo `secreto` en `80_Secretos`.
- **Reciprocidad documental:** en cada nota existente que enlazaste por una relación que el módulo declara recíproca (`reciprocas`: padres e hijos, una afección y sus afectados…), añade el vínculo inverso en su propiedad con `add_relation.py <Nota> <propiedad> <Entidad>`, sin leerla. Las demás no se espejan solas: ver el punto siguiente. No toques nada más.
- **Relaciones: el otro lado no es un espejo.** Por eso los módulos solo declaran recíprocas las relaciones bilaterales por naturaleza (el parentesco, la vecindad, la pertenencia, un pacto como una alianza), nunca las actitudes (la rivalidad, el miedo, el desprecio, la admiración): que A tenga a B por rival no hace que B tenga a A por rival. Y que una relación conste en las dos notas no la hace simétrica: si Aldric teme a un dragón, el dragón no teme a Aldric; quizá ni sabe que existe. Si la otra nota necesita la relación en su cuerpo (una fila de su tabla de relaciones), lee y edita solo esa sección y escríbela **desde el punto de vista del otro**: lo que esa entidad sabe, siente o hace respecto de la nueva, o nada si no le importa. Nunca copies ni inviertas la actitud sin pensarlo.

  **Que no se espeje sola no quiere decir que no pueda ser mutua.** Si lo es de verdad, porque lo que cuenta la nota lo sostiene (dos casas que se disputan el mismo puerto, dos fes que se condenan la una a la otra), añádela también en la otra nota: en su propiedad (`add_relation.py <Otra> rivales <Nueva>`) y, si hace falta, en su tabla, contada desde su lado. Si es de un solo lado, solo consta en la nota de quien la siente. Lo mismo al crear una entidad que otra ya tiene por rival: la nueva decide desde su lado si también la tiene por rival. Antes de fijar una relación que importa (desde relevancia 3), pregúntate:
  - ¿por qué existe?;
  - ¿qué cambia en cada entidad por la otra, con consecuencias concretas?;
  - ¿es recíproca de verdad, en lo narrativo, o solo consta en las dos notas?;
  - ¿seguiría teniendo sentido si una de las dos desapareciera?

  Si no cambia nada en ninguna de las dos, basta con el enlace: no hace falta una fila de relación.
- **Leyenda del lugar donde está:** si la entidad es un lugar (un lugar, un asentamiento o una región) y el lugar que la contiene ya tiene nota y leyenda (su `ubicacion`, su `region` o su `region_padre`; `map_key.py <Contenedor>` lo dice; si aún es un enlace pendiente, no hay nada que hacer: tendrá su leyenda al crearse), añádela con `map_key.py <Contenedor> --add "[[Nota|Nombre]]" --position <orientación> --desc "<una línea>"` y, si las hay, sus conexiones (`--connects`), sin leer la nota del contenedor. Si ya estaba (como enlace pendiente), el script no hace nada; si la leyenda está llena (código 3), anota la pregunta. Ver `referencias/mapas.md`.
- **Anclaje:** una entidad creada de la nada (sin un enlace pendiente que la pidiera) no puede quedar huérfana. Si la reciprocidad no la enlaza desde ninguna nota, añade su enlace en al menos una nota existente con la que se relaciona (su asentamiento, su región, su facción), en la propiedad que encaje (`add_relation.py`).
- **Glosario:** registra el nombre y los términos que inventaste con `add_entries.py --glossary <Término> <Tipo> "[[Nota]]" <Definición>` (repetible; con la nota vacía, `""`, para un término sin nota).
- **Enlace pendiente completado:** si llevaba un nombre de rol, reemplázalo por el definitivo en todas las notas con `rename_link.py <Rol_de_Entidad> <Nombre_Real>`. Si llevaba el nombre real, no hay nada que reemplazar.
- **Tipos y registro de enlaces pendientes:** ejecuta `python <directorio de esta skill>/scripts/pending_links.py`, que regenera `00_Sistema/Enlaces_Pendientes.md`. A los enlaces pendientes nuevos que solo aparecen en el cuerpo (o en una propiedad que admite cualquier entidad) dales su tipo en la misma llamada: `--set <Enlace>=<tipo>`, repetible. Vuelve a ejecutarlo si cambias enlaces al validar.
- **Preguntas Abiertas:** anota lo que no pudiste decidir con `add_entries.py --question "<pregunta>"`.

## Paso 5: validar (obligatorio)
Ejecuta el validador sobre **cada nota creada o modificada** (la entidad, sus secretos y las notas donde añadiste vínculos inversos). Las notas internas (Glosario, Preguntas Abiertas, MOC, registros) no son entidades: el validador las salta.
```bash
python <directorio de esta skill>/scripts/check_note.py <Nota_1> <Nota_2> …
```
El validador comprueba:
- el frontmatter (YAML válido, propiedades, estado, fecha sin comillas, propiedades de relación con solo enlaces);
- que la nota esté en la carpeta que le corresponde;
- el título con el emoji del tipo, las secciones que pide su relevancia y que no haya campos vacíos ni texto de plantilla;
- los enlaces pendientes nuevos dentro del rango del módulo para su relevancia, y todos con tipo;
- las menciones sin enlace del cuerpo (aviso): nombres propios desconocidos, entidades del Glosario y entidades que la nota ya enlaza en otra parte;
- que la nota no enlace a secretos y que su imagen exista;
- en un lugar con mapa, su leyenda (números del 1 al N sin repetir ni saltar, orientaciones, conexiones en los dos sentidos, hasta 12 zonas por nivel) y las imágenes de sus ediciones;
- en un calendario, sus tablas de meses, estaciones y festividades, y en cualquier nota, que `fecha_exacta` exista en el calendario de referencia y sea del año que precisa;
- en una era o un evento, que su situación cuadre con el año actual y que su cronología (o su desarrollo) vaya en orden y dentro de sus fechas.

Corrige cada ERROR y vuelve a ejecutarlo hasta que todas salgan "Correcta". No termines con errores. En lo que escribiste, atiende también los avisos:
- **Enlaces pendientes por debajo del mínimo**, en la entidad que acabas de crear. En las notas que solo tocaste (un vínculo inverso, un enlace reemplazado) ese aviso es normal.
- **Menciones sin enlace** (nombres propios, entidades del Glosario o entidades que la nota ya enlaza en otra parte): enlaza cada mención (a su nota o como enlace pendiente) y registra en el Glosario los términos. El detector puede equivocarse con una palabra suelta: si no es un nombre, ignóralo.
- **Enlaces sin texto legible.**

Después ejecuta el auditor del mundo, que revisa lo que no se ve nota a nota, centrado en las notas que creaste o tocaste:
```bash
python <directorio de esta skill>/scripts/audit_world.py --focus <Nota_1> <Nota_2> …
```
Con `--focus` muestra lo de esas notas y lo del mundo en general (el registro de pendientes, por ejemplo); del resto da solo el recuento, para no gastar tokens en lo que no es tuyo.
- Revisa la reciprocidad de las relaciones, las fechas imposibles entre padres e hijos, los nombres casi iguales, los enlaces mal formados, las notas vacías (un clic en un enlace pendiente en Obsidian), los enlaces pendientes sin tipo y el registro de pendientes.
- Corrige los ERRORES que afecten a notas que creaste o tocaste.
- Los avisos (nombres parecidos, entidades huérfanas) se mencionan en el resumen si son tuyos.

## Paso 6: imagen (automática)
Genera la imagen con la skill `generar-imagen`, pasándole la nota recién creada, **sin preguntar**: la imagen forma parte de crear la entidad y el pedido del usuario ya la incluye. Cada tipo tiene su propia imagen (un retrato para el personaje, un paisaje para la región…), definida en `generar-imagen`.
- Solo se omite si el usuario dijo explícitamente que no la quiere ("sin imagen" o "sin retrato"), o si el tipo no lleva imagen (los secretos no la llevan).
- Si el usuario pidió una técnica para la imagen ("con retrato al óleo", "en acuarela"), pásasela a `generar-imagen`; si no, se usa la de la Guía Visual del mundo.
- Si `generar-imagen` no está disponible o falla, deja la sección Imagen con la descripción visual y "Prompt: pendiente".
- **Mapa:** después de la imagen principal, si `map_key.py <Nota>` dice que toca dibujar, pide a `generar-imagen` el mapa (modo mapa). La imagen principal va siempre primero. Si falla, la leyenda queda y el mapa se dibuja más tarde.
- No dibujes ahora la edición nueva del lugar que la contiene, aunque le toque: la hace el motor (`cartografiar`) o el usuario (`/generar-imagen <Contenedor> mapa`). Dilo en el informe.
- Al terminar, vuelve a ejecutar `check_note.py` sobre la nota: `generar-imagen` la modificó.

## Paso 7: informe final
El usuario tiene que ver con claridad qué se generó. Ejecuta:
```bash
python <directorio de esta skill>/scripts/report.py --baseline <ruta de la instantánea>
```
Si no hay instantánea (no se tomó o se perdió), usa `--since HEAD`, que también cuenta lo que ya estaba sin confirmar, o `--notes <Nota> …`.

El informe trae, con enlaces que se abren con un clic:
- cada entidad nueva: resumen, carpeta, relevancia, imagen, relaciones con lo existente, quién la enlaza y los enlaces pendientes que introduce, con su tipo;
- los secretos, aparte;
- las notas modificadas, con los enlaces añadidos y quitados, y los enlaces pendientes completados;
- lo que necesita una decisión (`Confirmar`), las preguntas nuevas y los términos del Glosario;
- el estado del mundo: auditor, borradores pendientes, enlaces pendientes que ya se pueden crear (y cuántos hay por entidad) y los que no tienen tipo.

Muéstralo tal cual y añade debajo solo lo que el script no puede saber, sin repetir lo que ya dice:
- **Decisiones deducidas** que el usuario no indicó (el rol de un personaje, la categoría de una región…), con su motivo.
- **Lo inventado** según la autonomía de la Ficha: lo más importante, no una lista exhaustiva.
- **Tiradas** y su resultado (por ejemplo, "1d4 = 2: sin secreto").
- **Pilares decididos:** si se resolvió alguno (ver `referencias/pilares.md`), qué se decidió y los cambios en la Ficha, `CLAUDE.md`, Preguntas Abiertas y el Registro de Canon.
- **Imagen:** la técnica usada y, si falló, por qué y cómo generarla más tarde.
- **Mapa:** si se dibujó, su edición y su comprobación; las zonas inventadas para la leyenda; en qué leyenda se añadió el lugar (con su número) y si a ese mapa le toca una edición nueva (`/generar-imagen <Contenedor> mapa`).
- **Plantilla:** si la de `01_Plantillas` difiere de la de la skill.
- **Siguiente paso posible:** por ejemplo, crear uno de sus enlaces pendientes con `/crear-entidad <tipo> hueco=<Enlace>`.

Si la skill se ejecuta dentro de `expandir-mundo`, sáltate la instantánea y este paso: el informe se da una sola vez, al terminar la tanda.

## Reglas
- La skill es genérica: el contenido del mundo sale de la Ficha y de la bóveda, nunca de esta skill.
- No borres ni sobrescribas notas. En las existentes solo añades vínculos inversos y anclajes, o reemplazas un enlace pendiente con nombre de rol por el definitivo.
- Toda decisión al azar que pida un módulo se tira con `scripts/roll_dice.py` (por ejemplo, `roll_dice.py 1d4`). Nunca inventes el resultado de una tirada.
- Para añadir un tipo nuevo:
  - crea `tipos/<tipo>/` con `tipo.md`, `plantilla.md` y `modulo.json` (`tipo`, `familia`, `completa` si es de una familia, `emoji`, `huecos_propios`, `profundidad`, `mapa` si es un lugar con mapa, `carpeta`, `fechas`, `crear_desde_cero`, `escalas`, `valores` y `solo_si` si los tiene, `reciprocas` y `relaciones`);
  - declara en `reciprocas` solo relaciones bilaterales por naturaleza (parentesco, vecindad, pertenencia, contención, un pacto); las actitudes (rivales, temidos, admirados) van sin recíproca;
  - en `profundidad`, marca con 0 las secciones narrativas que el tipo no necesita por naturaleza (los ganchos de un idioma): van solo si hay algo real que contar;
  - añade su imagen en `generar-imagen/referencias/prompt.md`;
  - si se relaciona con una familia (`lugar`, por ejemplo) con una propiedad nueva, añádela al `completa` de los módulos de esa familia que puedan completarla;
  - ejecuta `python <directorio de esta skill>/scripts/check_modules.py`: revisa que la plantilla tenga todo lo que nombra el módulo y que cada relación y cada recíproca encajen con los demás módulos.

  El validador y `find_gaps.py` lo reconocen solos.
