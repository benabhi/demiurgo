---
name: expandir-mundo
description: Motor de generación de un mundo en su bóveda de Obsidian. En cada ciclo elige qué desarrollar según el estado del mundo (enlaces pendientes más nombrados, foco de la Ficha, paquetes, equilibrio entre completar lo pendiente y crear algo nuevo), tira ingredientes en tablas con azar real, arma el contexto de lo ya creado, crea las entidades con crear-entidad, valida y audita, registra el ciclo y hace un commit. Úsala para "expande el mundo", "genera más del mundo", "/expandir-mundo 3" o "/expandir-mundo prueba" (en una rama aparte para revisar antes).
---

# Expandir mundo

Hace crecer el mundo de forma coherente, ciclo a ciclo. Los scripts aportan el azar real y los datos; Claude, la escritura y el criterio.

Uso:
- `/expandir-mundo` hace **un ciclo**.
- `/expandir-mundo 5` hace **cinco seguidos**, y se detiene antes si se alcanza el límite de revisión.
- `/expandir-mundo prueba 3` usa el **modo prueba**: trabaja en una rama git aparte para revisar y luego fusionar o descartar.
- Si se añade "sin imagen", no se generan imágenes ni mapas en esa tanda: va más rápida y no usa el navegador (el selector va con `--no-maps`).
- Si se indica una técnica ("en acuarela", "como cómic"), todas las imágenes de la tanda la usan en lugar de la de la Guía Visual.
- Con `/loop` sigue sola hasta el límite de borradores sin revisar.

**El ciclo:** qué crear → ingredientes → contexto → componer → validar → registrar → commit.

**Cómo crece el mundo:** cada nota enlaza a las entidades que nombra, y las que aún no existen quedan como **enlaces pendientes** (ver `referencias/huecos.md` de `crear-entidad`). En cada ciclo, el motor completa uno de ellos o crea algo nuevo, y lo que crea nombra a su vez entidades nuevas. Para que el mundo no se llene de enlaces vacíos ni se quede sin hilos de los que tirar, el selector mira cuántos enlaces pendientes hay por entidad:
- con pocos, crea algo nuevo más a menudo y cada nota puede abrir bastantes enlaces nuevos;
- con muchos, casi siempre completa lo pendiente y cada nota abre los mínimos.

Además, el mundo crece **en profundidad** (las notas que ganan peso se profundizan), **en sus mapas** (se redibujan cuando han cambiado bastante) y **en sus conexiones**: el selector ve lo que debería estar unido por una ruta y no lo está (dos aldeas vecinas sin camino, una ruina a la que no llega nada) y crea la ruta que lo une.

## Archivos
- `scripts/setup_generation.py`: prepara `00_Sistema/06_Generacion` la primera vez, sin sobrescribir nunca.
- `scripts/select_target.py`: elige qué desarrollar (enlaces pendientes puntuados, paquetes o una entidad nueva) y cuántos enlaces nuevos puede abrir cada nota, o pide detenerse.
- `scripts/roll_tables.py`: tira en las tablas de ingredientes (con `--count`, varios resultados distintos: las salas de una mazmorra, los barrios de una ciudad) y deriva ingredientes del canon.
- `scripts/log_cycle.py`: añade la entrada del ciclo al registro de generación sin leerlo entero.
- Los scripts de `crear-entidad`: `build_context.py`, `search_vault.py`, `find_gaps.py`, `generate_names.py`, `add_entries.py`, `add_relation.py`, `rename_link.py`, `pending_links.py` (el registro de enlaces pendientes), `check_note.py`, `audit_world.py` y `report.py` (el informe final).

**Sin leer la bóveda entera:** el motor trabaja con mundos que crecen mucho. Sigue "Leer la bóveda sin gastar tokens" de `crear-entidad`: busca con `search_vault.py`, añade al Glosario, a las preguntas y a las otras notas con los scripts, y valida y audita solo lo del ciclo.
- `assets/`: tablas, paquetes, registro y README por defecto, que se copian a la bóveda la primera vez. Después el usuario los edita allí.

## Paso 0: preparar (una vez por tanda)
1. **Bóveda:** por defecto `World_Building/`. La Ficha del Mundo y `CLAUDE.md` mandan.
   - **El estado del mundo** (`estado_mundo`, en la Ficha): `cerrado`, el motor no genera (el selector se detiene); `en_cierre` (`/finalizar-mundo`), entra en **modo cierre**: solo completa enlaces pendientes, sin abrir ninguno nuevo (`enlaces_nuevos` 0–0), y dibuja los mapas con cualquier cambio sin dibujar; nada nuevo, ni rutas, ni profundizar. Cuando no queda nada que pueda crear, se detiene y remite a `/finalizar-mundo`.
2. **Instantánea para el informe:** antes de tocar nada, ejecuta `python <crear-entidad>/scripts/report.py --snapshot` y guarda la ruta que imprime. Con ella, el informe final junta todos los ciclos y no confunde lo generado con cambios del usuario sin confirmar.
3. **Carpeta de generación:** ejecuta `python <directorio de esta skill>/scripts/setup_generation.py`. Crea lo que falte en `06_Generacion`, la registra en la Guía de Organización y enlaza el registro desde `MOC_Inicio`.
4. **Git:** el repositorio del mundo es el que contiene la bóveda. Todos los comandos git del motor van con `git -C <bóveda>` (por defecto `git -C World_Building`) y con rutas relativas a la bóveda, así funciona tanto si la bóveda está dentro del repositorio del proyecto como si tiene uno propio. Si no está en ningún repositorio, avisa: sin git no hay commits por ciclo ni modo prueba.
5. **Modo prueba:** crea antes del primer ciclo la rama `prueba/<AAAA-MM-DD-HHMM>` con `git -C <bóveda> switch -c`.
6. **Pilares por definir:** si la Ficha deja sin definir pilares que afectan a lo que se va a crear (el calendario, las especies), se puede seguir, pero no los decides tú: quedan como preguntas.

## Paso 1: qué crear
```bash
python <directorio de esta skill>/scripts/select_target.py --json
```
Opciones:
- `--review-limit` (20 por defecto);
- `--new-chance`: la probabilidad de crear algo nuevo cuando hay pocos enlaces pendientes por entidad (0.4 por defecto; con muchos, baja al 40 % de ese valor);
- `--skip <enlace>` (repetible);
- `--skip-canon`;
- `--deepen-chance`: la probabilidad de profundizar una nota que lo necesita en vez de completar o crear (0.25 por defecto);
- `--map-chance`: la probabilidad de dibujar un mapa que toca en vez de completar o crear (0.25 por defecto);
- `--no-maps`: no propone mapas (en una tanda "sin imagen");
- `--connect-chance`: la probabilidad de unir con una ruta lo que debería estar unido y no lo está (0.2 por defecto; con muchos enlaces pendientes baja, como la de crear algo nuevo; con 1, siempre que haya algo que unir).

Solo se eligen enlaces pendientes que tienen tipo y un módulo que los cree. Quedan fuera los que esperan una confirmación en Preguntas Abiertas, los que coinciden con otro nombre de una entidad existente, los de fuera del mundo (tipo `fuera`) y, en un mundo que es una sola ciudad, las regiones (`descartados` dice por qué).

Toda elección, salvo `detener`, trae además:
- **`densidad`:** enlaces pendientes que se pueden crear por entidad (los secretos no cuentan como entidades).
- **`presupuesto`:** `amplio`, `medio` o `justo`.
- **`enlaces_nuevos`:** cuántos enlaces pendientes nuevos debe abrir cada nota, por tipo (por ejemplo `personaje: 3–5`). Respétalo al componer (Paso 4).

El resultado dice qué hacer:
- **`detener`:** hay demasiados borradores procedurales sin revisar. Para la tanda y avisa al usuario: se revisan con `/revisar-mundo`, que los pasa a canon o los archiva.
- **`crear_foco`:** la Ficha nombra un foco (`foco_texto`) que aún no existe como lugar. Se crea antes que nada, porque lo demás se generará dentro de él:
  - usa el módulo de `modulos` que encaje con el texto del foco (un continente, una cordillera o un territorio es una `region`), con relevancia alta;
  - si su nombre no aparece en el texto del foco, añade ese texto a sus `aliases`: así el selector lo reconoce como foco;
  - si trae `hueco`, la Ficha ya lo enlaza (en «Lo que ya tiene nombre»): créalo completando ese enlace pendiente (`hueco=<Enlace>`), así el archivo se llama como el enlace;
  - los `modulos` siguen la escala de la Ficha: en un mundo que es una sola ciudad, un asentamiento (o un lugar, si es una estación, un barco o una mazmorra); en uno que es una sola región, una región;
  - si ningún módulo encaja (un foco que no es un lugar, por ejemplo), anótalo en el registro y vuelve a ejecutar el selector con `--skip-focus`.
- **`crear_canon`:** un enlace pendiente (`referencia`) que nombra la Ficha o que nombran al menos tres notas: el conflicto central, la especie, el gran hecho. Es canon de base, así que va antes que lo demás:
  - crea la nota con **el mismo nombre de archivo que el enlace**, para que todas las notas que ya la nombran la encuentren sin reemplazar nada (si es un nombre de rol, ponle nombre y reemplázalo);
  - lee lo que dicen de ella esas notas (`find_gaps.py --link <referencia>`) y construye sobre la Ficha: lo que la Ficha deja abierto queda abierto, y los hechos grandes nuevos van como `Confirmar: …`;
  - relevancia alta (4 o 5);
  - si la Ficha pide aprobación para ese tipo de entidad (las especies nuevas, por ejemplo), sigue la regla del módulo: anota `Confirmar: …` con la referencia como primer enlace de la línea (eso la bloquea) y vuelve a ejecutar el selector;
  - si en realidad ningún módulo encaja, vuelve a ejecutar el selector con `--skip <referencia>`.
- **`completar_hueco`:** indica el enlace pendiente (`hueco`), el tipo esperado, los módulos que pueden crearlo y las notas que lo nombran (`nombrado_por`, de la más relevante a la menos). Antes de seguir, lee lo que dicen de él esas notas (`find_gaps.py --link <hueco>`). Si en realidad ningún módulo encaja (el selector propone una `region` para lo que las notas describen como una aldea, por ejemplo), no lo fuerces: anótalo en el registro y vuelve a ejecutar el selector con `--skip <hueco>`.
- **`profundizar`:** una nota en borrador (`nota`) que pide más desarrollo, con su relevancia actual y la nueva (`relevancia_actual`, `relevancia_nueva`) y las secciones que le faltan (`secciones`). Sale cuando la nombran tantas notas que su relevancia se quedó corta (3 notas piden relevancia 3; 6, relevancia 4; 10, relevancia 5) o cuando su relevancia ya pide secciones que no tiene. Así el mundo crece también en profundidad, no solo en extensión.
- **`cartografiar`:** un lugar con leyenda (`nota`) al que le toca dibujar su mapa: la primera edición (una región que ya tiene las zonas mínimas) o una nueva (`edicion`), con los niveles que hay que dibujar (`niveles`). Así los mapas siguen al mundo mientras crece, sin redibujarse en cada ciclo.
- **`conectar`:** lo que debería estar unido por una ruta y no lo está (`routes.py --unconnected`), con su `motivo`, su `partida` y su `destino`:
  - `vecinos`: dos asentamientos vecinos sin ningún camino entre ellos;
  - `capital`: un asentamiento importante sin camino hasta la capital de su región (o hasta el asentamiento con rutas más importante);
  - `regiones`: dos regiones vecinas que ninguna ruta une (la partida y el destino son las regiones: la ruta va de un lugar de una a uno de la otra, los de la frontera);
  - `aislado`: un lugar importante al que no llega nada (`destino` vacío: la ruta llega a él desde donde diga su contexto).

  Así el mundo se teje: cada ruta une lo que ya existe y, con sus paradas, sus peligros y quien la controla, nombra lo que vendrá.
- **`paquete`:** un grupo de entidades que se crean juntas (ver `Paquetes.md`), en la región foco.
- **`nueva_entidad`:** crea una entidad del tipo indicado en la región foco. En un mundo que es una sola ciudad, un asentamiento nuevo es un barrio de la ciudad foco (categoría `barrio`, con la ciudad en `ciudad`; no se tira la categoría), y nunca se propone una región. Nunca propone tipos que no se crean desde cero (`crear_desde_cero: false` en su módulo, como las especies). Una ruta nueva viene con `conexion`, lo que más necesita unirse: úsala. Si no la trae, la ruta parte de un lugar que ya existe en el foco (hacia un lugar nuevo, sin salida o circular).

`paquete` y `nueva_entidad` salen cuando toca crear algo nuevo o cuando no hay enlaces pendientes que se puedan crear.

Anota la semilla y las razones para el registro.

## Paso 2: ingredientes
```bash
python <directorio de esta skill>/scripts/roll_tables.py --file <Tipo> --file Oraculos --file Insolito --derive <Nota>
```
- **`--file <Tipo>`:** la tabla del tipo que vas a crear, si existe (`--list` muestra cuáles hay). Si el mundo tiene tablas propias en `06_Generacion/Tablas` que encajan con lo que se crea, añádelas con otro `--file`.
- **`--derive`:** la primera nota de `nombrado_por` (la más relevante de las que nombran el enlace pendiente) o, si no hay ninguna, la región foco. Así los ingredientes salen de lo que ya existe allí. En `crear_foco` no hay de dónde derivar: omítelo. En `crear_canon`, deriva de la región foco.
- **Mapas:** si lo que se crea lleva mapa (un lugar, un asentamiento o una región a los que les toca por su categoría y su relevancia), tira también su forma y sus zonas en `Mapas`, con las tablas de su clase y `--count` (ver «Variedad» en `crear-entidad/referencias/mapas.md`).
- **Rutas:** de `Ruta`, tira primero `Categoría` y `Trazado` (si no los fijan la geografía o el contexto) y después solo las tablas que tocan: `Sin salida: dónde se pierde`, `Circular: por qué vuelve`, `Portal: cómo se cruza` y, en una ruta perdida o dudosa, las dos de `Ruta perdida`.
- **Lo insólito** (`Insolito`) se tira siempre:
  - la **chispa** solo se usa si sale `hay_chispa=Sí` (una de cada tres veces, de media), y entra al mundo según su `grado_de_verdad`: como rumor, exageración, verdad a medias o verdad literal. Si la verdad literal choca con las reglas de la Ficha, vuelve a tirar solo el grado (`--table "Grado de verdad"`);
  - el **contraste** se integra en la entidad;
  - la **conexión inesperada** se ata a una entidad del contexto (Paso 3). Si implica un hecho importante, va como `Confirmar: …`.

  Lo insólito es lo que más riqueza da al mundo: no lo suavices hasta volverlo genérico. Intégralo con naturalidad en la ficha (en la historia, los rumores, los ganchos o las citas) y menciónalo en el registro del ciclo.

Los ingredientes son una **semilla, no una orden**:
- Lo que fijan el paquete o las notas que nombran el enlace pendiente manda. Si lo describen como una capital, es una ciudad, diga lo que diga la tabla.
- Si un ingrediente choca con el canon o con el contexto, vuelve a tirar solo esa tabla (`--table <Nombre>`) y anota el motivo.
- Los oráculos (motivación, complicación, giro…) se **interpretan** en el contexto del mundo; no se copian literalmente.
- Nunca inventes un resultado: todo sale de `roll_tables.py`.

## Paso 3: contexto
```bash
python <crear-entidad>/scripts/build_context.py --target <enlace pendiente, entidad relacionada o región foco>
```
Es todo lo que necesitas saber del mundo para esta creación. Lee entera solo la nota que haga falta en detalle.

En `conectar`, el objetivo es la partida (o el lugar aislado), y además `python <crear-entidad>/scripts/routes.py <partida> <destino>` dice si ya hay un camino entre ellos, más largo, y cuánto se tarda: la ruta nueva lo respeta (es más directa, o explica por qué no).

## Paso 4: componer
Sigue el protocolo completo de `crear-entidad` en **modo semilla**, con los ingredientes y el contexto, salvo su instantánea y su informe final (el informe se da una sola vez, al terminar la tanda):
- `origen: procedural` y `estado: borrador`.
- **Enlace pendiente** (`crear_canon` y `completar_hueco`): modo `hueco=<Enlace>`. La nota se llama como el enlace; si es un nombre de rol, ponle nombre y reemplázalo en todas las notas que lo usan.
- **Presupuesto:** cada nota abre los enlaces pendientes nuevos que diga `enlaces_nuevos` para su tipo, recortados al rango de su relevancia (`check_note.py --depth`), todos con tipo. Lo demás que nombre va sin nombre propio, o reutiliza lo que ya existe o ya está pendiente (el registro `Enlaces_Pendientes`).
- **Paquete:** crea primero la entidad principal y después las demás. Cada una se enlaza con las anteriores (a su nota, no como pendiente) y usa su contexto. Respeta las cantidades y los papeles. La principal tiene una relevancia igual o mayor que la de las demás.
- **Nueva entidad:** dentro de la región foco.
- **Conectar:** crea una `ruta` en modo semilla, con `partida=[[<partida>]]` y `destino=[[<destino>]]`. En `aislado`, el lugar aislado es el destino y la partida, el lugar con rutas más cercano que diga el contexto. En `regiones`, un lugar de cada región. Su categoría, su trazado y lo demás salen de la geografía que cruza y de las tablas: entre dos puertos, una ruta marítima; a través de una sierra, un paso; si los poderes del mundo lo permiten y la tirada lo pide, un portal. Después, como toda ruta, `map_key.py --sync-routes`.
- **Cartografiar:** no se crea nada ni hay ingredientes ni contexto (sáltate los pasos 2 y 3): pide a `generar-imagen` el mapa de la `nota` (modo mapa, ver su `referencias/mapas.md`), con la técnica de mapas del mundo. Después, valida la nota, registra el ciclo y haz el commit como siempre.
- **Profundizar:** modo `profundizar=<Nota> relevancia=<relevancia_nueva>` de `crear-entidad` («Profundizar una nota»): añade las `secciones` que faltan sin reescribir lo que ya está. La nota no cambia de nombre ni de `origen`.
- **Anclaje:** lo creado de la nada (un paquete, una entidad nueva) queda enlazado desde alguna nota existente (su asentamiento, su región…), como pide `crear-entidad`.
- **Imagen:** automática, salvo que la tanda sea "sin imagen", y con la técnica de la tanda si se indicó una.
- **Reglas de `crear-entidad` que siguen valiendo:**
  - toda entidad nombrada lleva enlace (a su nota o como enlace pendiente);
  - nombres con `generate_names.py`;
  - hechos grandes como `Confirmar: …`;
  - secretos por tirada;
  - reciprocidad y Glosario, con `add_relation.py` y `add_entries.py`;
  - el registro de enlaces pendientes, regenerado con `pending_links.py` (con `--set` para los que solo nombra el cuerpo).

## Paso 5: validar
- `check_note.py` sobre cada nota creada o modificada.
- `audit_world.py --focus` con esas mismas notas: muestra lo suyo y lo del mundo en general, y del resto solo el recuento.

Corrige los errores antes de seguir.

## Paso 6: registrar
Añade la entrada del ciclo al registro de generación con `log_cycle.py`. El script la pone arriba, con su número y la fecha de hoy (el título `## Ciclo <N> — <AAAA-MM-DD>`), sin que tengas que leer el registro. Pásale el cuerpo de la entrada por la entrada estándar (o con `--file`):
```markdown
- **Acción:** crear el foco «texto» → <tipo> · o · crear [[Referencia]] → <tipo> (canon de base) · o · completar [[Enlace]] → <tipo> · o · paquete «Nombre» · o · nueva entidad <tipo> · o · profundizar [[Nota]] (relevancia <n> → <m>) · o · cartografiar [[Nota]] (edición <n>, niveles <…>) · o · conectar [[Partida]] y [[Destino]] (<motivo>) → [[Ruta]]
- **Por qué:** <razones del selector> (semilla <n>)
- **Equilibrio:** densidad <n> enlaces pendientes por entidad · presupuesto <amplio, medio o justo> · enlaces pendientes nuevos abiertos: <n>
- **Ingredientes:** <clave=valor, …> (semilla <n>); re-tiradas y su motivo
- **Lo insólito:** la chispa y su grado de verdad, y cómo se integró (o "sin chispa")
- **Contexto:** [[Nota]], [[Nota]]
- **Creadas:** [[Nota]], … (los secretos sin enlace, solo su nombre)
- **Modificadas:** [[Nota]] (qué cambió)
- **Avisos:** los del auditor, o "ninguno"
```
El script imprime el número del ciclo, que va en el mensaje del commit.

## Paso 7: commit
Un ciclo es un commit, así cada ciclo se puede revertir por separado (`git revert <hash>`).
- Añade **solo** los archivos que creó o modificó el ciclo, más el registro de generación y el de enlaces pendientes, con rutas relativas a la bóveda (`git -C <bóveda> add <rutas>`), nunca `git add -A`. Si el usuario tiene otros cambios sin guardar, se quedan fuera.
- El commit también va en el repositorio de la bóveda: `git -C <bóveda> commit`.
- El mensaje es `Generación <N>: <entidad principal>`, con la línea de co-autoría que indique la sesión.

## Al terminar la tanda: informe
El usuario tiene que ver con claridad qué se generó.
1. Ejecuta:
   ```bash
   python <crear-entidad>/scripts/report.py --baseline <ruta de la instantánea> --log "Expandir el mundo: <N> ciclos" --cycles <primero>-<último>
   ```
   Si no hay instantánea, usa `--since <commit en que empezó la tanda>`. Los números de ciclo son los que imprimió `log_cycle.py`. Si la tanda se detuvo antes, el título lo dice: `Expandir el mundo: 2 de 5 ciclos (límite de revisión)`.

   `--log` añade a la **Bitácora** (`00_Sistema/Bitacora.md`) una entrada breve de la tanda, para el autor del mundo: la acción de cada ciclo, lo creado y lo modificado, y la remisión al Registro de Generación. Haz su commit: `git -C <bóveda> add -A 00_Sistema && git -C <bóveda> commit -m "Bitácora: tanda de <N> ciclos"` (en modo prueba, en la rama de la prueba).

   El informe junta todos los ciclos, con enlaces que se abren con un clic:
   - entidades nuevas (resumen, relaciones, quién las enlaza y enlaces pendientes que introducen) y secretos aparte;
   - notas modificadas con los enlaces añadidos y quitados, y enlaces pendientes completados;
   - decisiones pendientes (`Confirmar`), preguntas nuevas y términos del Glosario;
   - los commits de los ciclos, que se deshacen por separado;
   - el estado del mundo: auditor, borradores pendientes, enlaces pendientes que ya se pueden crear (y cuántos por entidad) y los que no tienen tipo.
2. Muéstralo tal cual. Encima, resume la tanda en pocas líneas (las notas, con enlaces Markdown a su archivo, como hace el script; en el chat, `[[...]]` no se abre):
   - ciclos hechos y la acción de cada uno (completar un enlace pendiente, paquete, nueva entidad, profundizar, cartografiar o conectar), con el motivo del selector;
   - cómo quedó el equilibrio: densidad y presupuesto al empezar y al terminar;
   - los ingredientes o giros de las tablas que más marcaron lo creado;
   - si se detuvo antes y por qué (límite de revisión, error).
3. Si hay decisiones pendientes, recuerda que los enlaces pendientes que dependen de ellas quedan bloqueados hasta que el usuario decida.
4. En **modo prueba**, pregunta si se fusiona la rama en la principal o se descarta (en el repositorio de la bóveda, con `git -C <bóveda>`): es la única decisión del flujo.

## Reglas
- **Canon:** nunca contradice el canon ni decide pilares por definir. Los hechos grandes nuevos van a Preguntas Abiertas como `Confirmar: …`.
- **Límite de revisión:** no genera si hay más borradores procedurales sin revisar que el límite. Así no se construye sobre lo que el usuario aún no aprobó.
- **Azar real:** ingredientes y decisiones al azar siempre por script, con semilla anotada.
- **Archivos del usuario:** las tablas, perfiles y paquetes de `06_Generacion` son del usuario. Se leen y se usan, pero no se reescriben.
- **Skill genérica:** nada de un mundo concreto en `assets/`.
