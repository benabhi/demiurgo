<div align="center">
  <img style="width: 400px;" src="https://i.ibb.co/zVbZRpN2/logo.jpg" alt="Logo">
</div>

<br />

**Un kit de skills de [Claude Code](https://claude.com/claude-code) para construir mundos de ficción en Obsidian: entidad a entidad, a tu ritmo, o dejando que el mundo crezca solo, ciclo a ciclo, sin perder la coherencia.**

En la literatura y en el habla común, un *demiurgo* es quien ordena un universo: el escritor, el director de cine o el poeta capaz de dar forma a una obra magna. Ese es tu papel. Tú decides cómo es el mundo y qué es canon; las skills de Demiurgo lo ordenan, lo conectan, lo completan y lo mantienen coherente mientras crece.

Sirve para mundos de cualquier género (fantasía, ciencia ficción, histórico, terror…) y de cualquier tamaño, de una sola ciudad a varios mundos o planos. Todo vive **en una bóveda de Obsidian**: cada entidad es una nota enlazada con las demás, con el desarrollo que pide su importancia, su imagen y, si es un lugar que lo merece, su mapa.

> **Pensado para Obsidian.** Las skills escriben notas Markdown con propiedades (frontmatter), enlaces `[[…]]`, índices automáticos con el plugin **Bases** y una estructura de carpetas pensada para un mundo. Sin Obsidian las notas se pueden leer, pero se pierden la navegación por enlaces, las propiedades y los índices.

## Cómo crece un mundo
De dos maneras, que se combinan:
- **Incremental:** pides lo que quieres (`/crear-entidad personaje un herrero del puerto`) y la nota enlaza todo lo que nombra. Lo que aún no existe queda como **enlace pendiente**, un hilo del que tirar después: el mundo se expande desde lo que ya dice.
- **Procedural:** el motor (`/expandir-mundo 5`) hace crecer el mundo por ciclos. En cada uno elige qué desarrollar según el estado del mundo (completar lo que ya se nombra, crear algo nuevo, profundizar lo que ganó peso, redibujar un mapa o unir dos lugares con una ruta), tira los ingredientes en tablas con azar real, crea, valida y hace un commit.

Y a lo largo de su vida:
1. **Nace** con `/inicializar-mundo`: una entrevista sobre sus pilares crea la bóveda, sus guías, su Ficha y sus reglas.
2. **Crece** con `/crear-entidad` y `/expandir-mundo`, con sus imágenes y sus mapas (`/generar-imagen`).
3. **Se asienta** con `/revisar-mundo`: todo nace como borrador y tú decides qué pasa a canon.
4. **Se usa** con `/consultar-mundo`, que responde con lo que dice la bóveda, y con `/narrar`, que escribe relatos, escenas y crónicas ambientados en él.
5. **Se cuida** con `/diagnosticar-mundo`: su salud, y al día con cada versión de las skills.
6. **Se termina** con `/finalizar-mundo`: sin cabos sueltos, y cerrado.

## Qué hace
- **Una entrevista inicial** sobre los pilares del mundo (premisa, género, tono, poderes, tecnología, dioses, especies, calendario…) y lo que ya tiene nombre propio, que crea la bóveda: carpetas con su README, guías de convenciones, índices, la **Ficha del Mundo** y un `CLAUDE.md` con las reglas que salen de tus respuestas.
- **28 tipos de entidad**, cada uno con su ficha, sus reglas y su validación: personajes, regiones, asentamientos, lugares, rutas (caminos, pasos, rutas por mar o por aire, portales), facciones, linajes, objetos, creencias, deidades, especies, culturas, idiomas, calendarios, eras, eventos, fenómenos, afecciones, criaturas, sistemas (poderes, tecnología, leyes del universo), mitos, costumbres (leyes, fiestas, ritos y tabúes), materiales y recursos, flora, ecosistemas, astros, obras (textos, canciones, pinturas, mapas antiguos) y secretos.
- **Del tamaño que quieras:** una sola ciudad (con sus barrios), una región, un continente o un mundo entero, o varios mundos o planos. En una ciudad o una región, todo se crea dentro, y lo de fuera se nombra como referencia sin crearse. Lo que ya tenías con nombre propio entra en la Ficha, y el motor empieza por ello.
- **Un mundo entrelazado:** toda entidad que una nota nombra va enlazada. Las que todavía no existen quedan como **enlaces pendientes** con su tipo, y el mundo crece completándolos. Las relaciones no son espejos: si alguien teme a un dragón, el dragón no tiene por qué temerle.
- **Rutas y distancias:** las rutas unen los lugares con sus tiempos de viaje, tramo a tramo, y con ellas un grafo de distancias dice cuánto se tarda de un sitio a otro y por dónde, para que el mundo no se contradiga. También hay senderos que no llevan a ninguna parte, rutas circulares, redes, portales y rutas perdidas que solo cuenta un texto antiguo.
- **Profundidad según la relevancia:** un antagonista central tiene una ficha extensa y un campesino, lo esencial; nada se inventa para llenar una plantilla. Cuando una entidad gana peso en el mundo, el motor la profundiza.
- **Un motor de generación** que elige qué crear, profundizar, cartografiar o unir con una ruta según el estado del mundo, tira ingredientes con azar real, crea las entidades, las valida y hace un commit por ciclo.
- **Imágenes** de cada entidad (retratos, paisajes, emblemas, escenas…) con la técnica artística que elijas: acuarela, óleo, grabado, cómic… Cada una se comprueba contra lo que se pidió (en un mapa, sus números uno por uno) y se corrige si falla; el resultado queda anotado en la nota.
- **Mapas** de las mazmorras, ruinas, ciudades y regiones que lo merecen, con su leyenda numerada en la nota y en el mismo estilo que el resto de las imágenes. Las rutas no tienen mapa propio: se dibujan en los mapas de las regiones que cruzan, y la ciudad nueva al final de un camino entra en el mapa de su región. Su forma, sus pisos y sus salas o barrios salen de tablas con azar real, para que no haya dos iguales. Crecen con el mundo: cada lugar nuevo se añade a la leyenda y el mapa se redibuja cuando ha cambiado bastante, sin perder el dibujo anterior, que queda archivado y enlazado en la nota.
- **Coherencia por script:** cada nota se valida al crearla, un auditor revisa el mundo entero (fechas, relaciones recíprocas, nombres repetidos…) y cada generación termina con un informe.
- **Pensado para mundos grandes:** la IA no lee la bóveda entera. Busca con scripts (entidades, enlaces pendientes, Glosario, preguntas), añade al Glosario y a otras notas sin leerlas, y valida y audita solo lo que tocó. Así un mundo de miles de notas no se come los tokens.
- **Un grafo que se lee de un vistazo:** al crear el mundo, el grafo de Obsidian queda configurado con un color por tipo de entidad (verdes los lugares, azules la gente, cálidos la fe y los relatos…), los nombres visibles desde lejos, sin las notas del sistema que lo enredan y con los enlaces pendientes en gris. En Marcadores quedan dos vistas: «Grafo sin secretos», para enseñar el mundo sin spoilers, y «Grafo completo».
- **Una bitácora del mundo** (`00_Sistema/Bitacora.md`): cada creación, entidad, tanda del motor, imagen o mapa deja una entrada breve con su fecha, lo creado y lo modificado, para ver de un vistazo cómo fue creciendo el mundo.
- **Estadísticas del mundo** (`00_Sistema/Estadisticas.md`): cuántas entidades hay por tipo y por relevancia, los enlaces pendientes, las imágenes y los mapas que toca redibujar, lo más nombrado que falta y lo más enlazado. Se rehace sola al terminar cada tarea, y sus cifras van también en el frontmatter, para un tablero.
- **Pregúntale al mundo:** `/consultar-mundo` responde con lo que dice la bóveda (qué es algo, qué hay en un lugar, cuánto se tarda de un sitio a otro, qué pasó y cuándo), cita sus notas, distingue el canon de los borradores y aparta los secretos, o los oculta para enseñar el mundo sin spoilers.
- **Cuéntalo:** `/narrar` escribe relatos, escenas, crónicas y documentos (cartas, diarios, canciones) ambientados en el mundo. Antes reúne lo que necesita y comprueba fechas, lugares y quién vive en cada momento; lo que inventa se queda en la narración, no usa los secretos salvo que lo pidas, y al final te ofrece ilustrar el momento clave.
- **Un mundo que se termina:** `/finalizar-mundo` lo cierra sin cabos sueltos. Por fases y contigo, decide los pilares y las preguntas que faltan (o los deja como misterios a propósito), crea, disuelve o fusiona cada enlace pendiente, revisa todos los borradores y completa imágenes y mapas, hasta que cada nota pasa la validación sin anotaciones de trabajo. Mientras tanto el mundo deja de crecer; cerrado, ya no se crea nada (sí se consulta, se narra y se ilustra), y se puede reabrir.
- **Un chequeo de la bóveda:** `/diagnosticar-mundo` dice qué está mal, qué se quedó atrás al actualizar las skills (el `CLAUDE.md`, las guías y las plantillas, las propiedades nuevas de cada tipo, el grafo, las notas del sistema) y qué pide atención, con la skill que lo resuelve. Arregla solo lo seguro y te propone el resto.
- **Tú decides qué es canon:** todo nace como borrador. `/revisar-mundo` te los muestra por tandas, de lo que más pesa a lo que menos, y cada uno pasa a canon, sigue en borrador o se archiva, con sus imágenes, sus secretos y su sitio en los mapas. Nada se borra.
- **Lo que se sabe frente a lo que es:** las notas cuentan lo que el mundo sabe o cree, y la verdad oculta va aparte, en `80_Secretos`.

## Las skills
| Skill | Para qué |
|---|---|
| `inicializar-mundo` | Entrevista y bóveda inicial: estructura, guías, Ficha del Mundo y `CLAUDE.md`. |
| `crear-entidad` | Crea una entidad (`/crear-entidad personaje un herrero del puerto`), completa un enlace pendiente (`/crear-entidad region hueco=Nombre_del_Enlace`) o profundiza una nota que ganó importancia. |
| `expandir-mundo` | Hace crecer el mundo por ciclos (`/expandir-mundo 3`), o en una rama aparte para revisarlo antes (`/expandir-mundo prueba`). |
| `generar-imagen` | La imagen de una entidad y el mapa de un lugar. La invoca `crear-entidad` sola; también sirve para regenerarla (`/generar-imagen Nombre_de_la_Nota acuarela`) o para dibujar un mapa (`/generar-imagen Nombre_de_la_Nota mapa`). |
| `revisar-mundo` | Repasa los borradores por tandas (`/revisar-mundo`): cada uno pasa a canon, sigue en borrador o se archiva, para rehacerlo o para quitarlo del mundo. |
| `consultar-mundo` | Responde preguntas sobre el mundo con lo que dice la bóveda (`/consultar-mundo ¿quién gobierna el puerto?`), citando sus notas, sin leerla entera. |
| `narrar` | Relatos, escenas, crónicas y documentos ambientados en el mundo, coherentes con su canon (`/narrar escena la noche en que volvió el cometa`), en `90_Narrativa`. |
| `diagnosticar-mundo` | La salud de la bóveda y si está al día con las skills (`/diagnosticar-mundo`): arregla lo seguro, propone lo demás y dice qué pide atención. |
| `finalizar-mundo` | Cierra el mundo sin cabos sueltos (`/finalizar-mundo`): lo deja impecable por fases, con el usuario, y lo cierra; o lo reabre. |

Las nueve forman Demiurgo y van juntas: `expandir-mundo`, `revisar-mundo`, `consultar-mundo`, `narrar`, `diagnosticar-mundo` y `finalizar-mundo` usan los scripts de `crear-entidad`.

## Requisitos
- **Claude Code.**
- **Obsidian**, con el plugin principal **Bases** activado (los índices de cada sección lo usan).
- **Python 3.10 o posterior.** Los scripts solo usan la biblioteca estándar.
- **Git**, recomendado: el motor hace un commit por ciclo y el modo prueba trabaja en una rama.
- **Para las imágenes**, opcional:
  - la extensión Claude in Chrome, conectada a tu Chrome;
  - una cuenta de Google con acceso a Gemini, con la sesión iniciada en ese Chrome.

  Por ahora las imágenes se generan con Gemini en el navegador; más adelante se cambiará por una API u otra vía más eficiente.

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/benabhi/demiurgo.git
   ```
2. Pon las nueve carpetas de `skills/` donde Claude Code busca las skills:
   - en `~/.claude/skills/`, para tenerlas en todos tus proyectos;
   - o en `<tu proyecto>/.claude/skills/`, solo para un mundo.

   Mejor enlazarlas que copiarlas: así se actualizan con `git pull`. Después de actualizarlas, `/diagnosticar-mundo` dice qué cambió para tu bóveda y la pone al día.
   - **Windows**, con PowerShell y sin permisos de administrador (un *junction* por skill):
     ```powershell
     New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
     Get-ChildItem "C:\ruta\demiurgo\skills" -Directory | ForEach-Object { New-Item -ItemType Junction -Path "$HOME\.claude\skills\$($_.Name)" -Target $_.FullName }
     ```
   - **macOS y Linux:**
     ```bash
     mkdir -p ~/.claude/skills
     for skill in /ruta/demiurgo/skills/*/; do ln -s "${skill%/}" ~/.claude/skills/; done
     ```

## Cómo empezar un mundo
1. Crea una carpeta para el mundo y abre Claude Code en ella. Conviene que sea un repositorio git.
2. Ejecuta `/inicializar-mundo`. Tras la entrevista crea la bóveda en `World_Building/` y el `CLAUDE.md` del mundo en la raíz.
3. Abre `World_Building/` como bóveda en Obsidian y activa el plugin principal Bases.
4. Crea las primeras entidades con `/crear-entidad <tipo> <idea>`. Lo más útil al principio es el foco del mundo y su conflicto central.
5. Deja que el mundo crezca con `/expandir-mundo`.
6. Revisa lo creado con `/revisar-mundo`: por tandas, cada borrador pasa a canon, sigue en borrador o se archiva (para rehacerlo o para quitarlo del mundo).

Los scripts buscan la bóveda en `World_Building/`. Si la tuya está en otra carpeta, todos aceptan `--vault <carpeta>`.

Los comandos git de las skills (los commits del motor y su modo prueba) van al repositorio que contiene la bóveda. Puede ser el del proyecto o uno propio de la bóveda.

## Cómo es la bóveda
- `00_Sistema/`: la Ficha del Mundo, el índice de inicio, las preguntas abiertas, las convenciones (organización, nombres, canon, estilo, Glosario), las plantillas, los activos (imágenes) y el registro de enlaces pendientes.
- De `10_Mundo/` a `70_Sistemas_y_Cosmologia/`: las entidades, cada una en su carpeta según lo que es.
- `80_Secretos/`: la verdad oculta, que las notas de lore no enlazan.

Cada nota nace como `borrador` y solo tú la promueves a `canon`.

## Idioma
Las skills, las carpetas y las convenciones están en español. El idioma del contenido del mundo y de la conversación se elige en la entrevista.

## Estado
Demiurgo está en desarrollo:
- ya están todos los tipos de entidad; los últimos (de las rutas a los astros) esperan su prueba en un mundo real;
- la entrevista inicial ya distingue el alcance del mundo (una ciudad, una región, un mundo o varios) y recoge lo que ya tiene nombre propio, y espera su prueba;
- `revisar-mundo` (repasar los borradores y pasarlos a canon o archivarlos), `consultar-mundo` (preguntas sobre el mundo), `narrar` (relatos y escenas), `finalizar-mundo` (cerrar el mundo) y `diagnosticar-mundo` (la salud de la bóveda) están hechas y esperan su prueba;
- faltan las imágenes por API.

El plan está en [PLAN.md](PLAN.md).

## Licencia
Por definir.
