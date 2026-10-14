---
name: generar-imagen
description: Genera la imagen de una entidad del mundo (el retrato de un personaje, el paisaje de una región…) con Gemini en el Chrome del usuario (Claude in Chrome), con la ambientación del mundo y la técnica artística elegida (óleo, acuarela, cómic, lápiz a mano alzada, grabado… según su Guía Visual), y la guarda y enlaza en su nota de Obsidian de forma automática. También dibuja el mapa de los lugares que lo llevan (mazmorras, ruinas, ciudades, regiones…) a partir de la leyenda de su nota, con el mismo estilo. La invoca crear-entidad al terminar; también sirve para "genera la imagen de…", "regenera el retrato de… en acuarela", "dibuja el mapa de…" o "cambia la técnica del mundo a óleo".
---

# Generar imagen

Arma un prompt con el estilo del mundo y los datos de la nota, genera la imagen con Gemini en el Chrome del usuario y la guarda en la bóveda, enlazada a la nota. **Todo el flujo es automático.**

> [!todo] Provisional
> Generar con Gemini en el navegador es la única vía por ahora. Se reemplazará más adelante por una API u otra vía más eficiente, que genere por script sin abrir el navegador.

El estilo tiene dos capas: la **ambientación**, que marca el mundo (género, tono, materiales, paleta), y la **técnica**, que elige el usuario de un catálogo de 27 (óleo, acuarela, cómic, lápiz, grabado, vitral, fotograma de cine…).

Además de su imagen principal, los lugares que lo merecen tienen **mapa**: una imagen que dibuja la leyenda numerada de su sección Mapa, con la técnica de mapas del mundo (ver `referencias/mapas.md`). La imagen principal sigue siendo obligatoria y la primera de la nota.

Uso: `/generar-imagen <nota> [técnica]`.
- `/generar-imagen Aldric_Voss` usa la técnica de la Guía Visual.
- `/generar-imagen Aldric_Voss acuarela` usa otra técnica solo para esta imagen: un id o un nombre de `referencias/tecnicas.md`, o una descripción propia ("como un mapa antiguo").
- "Cambia la técnica del mundo a óleo" o "los paisajes, en acuarela" cambian la Guía Visual: la técnica general o la tabla "Técnica por tipo". Solo se tocan esas secciones.
- `/generar-imagen Puerto_Gris mapa` dibuja el mapa del lugar: la primera edición o una nueva, según su leyenda (`/generar-imagen Cripta_Honda mapa nivel 2` dibuja solo ese nivel).
- `/generar-imagen tecnicas` (o "¿qué técnicas hay?") muestra el índice de `referencias/tecnicas.md` tal cual, con el total, y dice qué técnica usa ahora el mundo y cómo pedir otra. No genera nada.

## Autorización
El pedido del usuario (invocar esta skill o crear una entidad con `crear-entidad`) es la autorización explícita para generar **esta** imagen: enviar el prompt a Gemini, descargar la imagen y moverla a la bóveda. Por eso:
- no preguntes antes de generarla;
- no preguntes si la imagen gusta;
- no preguntes antes de guardarla.

Al terminar, informa de lo que hizo (ver "Paso 5: informe").

Solo se para en estos casos: para elegir la técnica al crear la Guía Visual (una vez por mundo), para elegir la técnica de mapas si la general no es sobre papel (también una vez) y cuando el navegador necesita algo que solo puede hacer el usuario (iniciar sesión, aceptar un aviso).

## Requisitos
- **Claude in Chrome:** la extensión de Claude conectada al Chrome del usuario.
- **Una cuenta de Google con acceso a Gemini,** con la sesión iniciada en ese Chrome. La inicia siempre el usuario.
- **Python 3.10 o posterior,** para mover la descarga a la bóveda.

## Archivos de la skill
- `referencias/prompt.md`: qué muestra la imagen de cada tipo (formato, carpeta y prefijo del archivo), qué técnica usa cada imagen, la plantilla del prompt de cada tipo y de dónde sale cada campo.
- `referencias/tecnicas.md`: el catálogo de técnicas artísticas, con sus bloques en inglés y las recomendadas por género.
- `referencias/estilos.md`: la ambientación por género, cómo crear la Guía Visual y su plantilla.
- `referencias/mapas.md`: el modo mapa: qué edición toca, la técnica de mapas, la plantilla del prompt (los marcadores y el formato A4), la edición sobre la anterior, la comprobación y cómo se guarda y se enlaza. La leyenda la mantiene `<crear-entidad>/scripts/map_key.py`.
- `scripts/fetch_download.py`: mueve a la bóveda la imagen descargada desde el navegador, sin sobrescribir.

## Paso 1: preparar
1. Lee la nota de la entidad y su `tipo`. Busca el tipo en la tabla "Resumen por tipo" de `prompt.md`: de ahí salen su formato, su **carpeta** y su **prefijo**. Si el tipo no figura, o no lleva imagen, dilo y detente.
2. **Guía Visual:** lee `00_Sistema/04_Convenciones/Guia_Visual.md`.
   - Si no existe (es el primer uso en este mundo), créala siguiendo "Cómo crear la Guía Visual" de `estilos.md`: la ambientación y la paleta salen de la Ficha, y la técnica se pregunta al usuario **mostrándole el catálogo completo**, no solo las opciones del diálogo. Es la única pregunta del flujo y se hace una sola vez por mundo.
   - Al guardarla, añádela a la lista de convenciones de `MOC_Inicio`.
   - Si es del formato anterior (sin sección "Técnica"), sigue "Guías de la versión anterior" de `estilos.md`. Si sus Restricciones incluyen un formato ("square 1:1") o "single subject", o su Estilo dice "portrait", **ignora esas partes** para tipos que no son retratos: el formato y el sujeto los pone cada tipo.
3. **Técnica de esta imagen:** según "Qué técnica usa cada imagen" de `prompt.md`: la pedida para esta imagen, la del tipo en la Guía o la general (si es "Variada", con una tirada). Si piden una técnica que no está en el catálogo, escribe sus bloques como dice "Técnica propia" en `tecnicas.md`.
4. **Modo mapa** (si se pidió el mapa, o lo pide `crear-entidad` o el motor): ejecuta `python <crear-entidad>/scripts/map_key.py <Nota> --json` para saber qué edición toca y qué niveles se dibujan (ver «Qué edición toca» en `mapas.md`), y usa la **técnica de mapas** de la Guía (si no la tiene, ver «Técnica de mapas»). La carpeta es `Mapas` y el prefijo `Mapa_`. Los pasos que siguen valen igual para el mapa, con lo que dice `mapas.md`.
5. **Primera imagen de este tipo:** si no existe la carpeta del tipo (`00_Sistema/02_Activos/<Carpeta>/`), créala con un `README.md` breve (la de los mapas, ver «Guardar y enlazar» en `mapas.md`). Añade una fila a la tabla "Carpetas añadidas por skills" de la Guía de Organización: `| 00_Sistema/02_Activos/<Carpeta> | Imágenes de <tipo> (<Prefijo><Nota>.<ext>) | generar-imagen |`. Varias carpetas las comparten varios tipos (`Escenas`, `Lugares`…, según "Resumen por tipo" de `prompt.md`): si la carpeta ya existe pero es la primera imagen de este tipo en ella, añade el tipo a la descripción de su fila y a su README (`Imágenes de fenomeno y cultura (Fenomeno_…, Cultura_…)`). Las carpetas de la estructura inicial (como `Iconos`) no se registran en esa tabla, porque no las creó una skill: basta con añadir el tipo a su README.

## Paso 2: prompt
Arma el prompt según la sección del tipo en `prompt.md`:
- la capa del mundo: la técnica de esta imagen y la ambientación y la paleta de la Guía Visual, con los bloques tal cual;
- la capa de la entidad, desde su nota (con el fondo fundido con el papel si la técnica es 📄);
- el formato del tipo, al final.

En modo mapa, el prompt es el de «La plantilla del prompt» de `mapas.md`, uno por nivel: se arma con la leyenda y con lo que la nota cuenta de cada zona.

## Paso 3: generar con Gemini en Chrome
1. Si las herramientas de Claude in Chrome (`mcp__claude-in-chrome__*`) no están cargadas, cárgalas con ToolSearch en una sola llamada. Si existe la skill `anthropic-skills:chrome-browser`, léela antes.
2. Si Chrome no está disponible, ve a "Si algo falla".
3. Abre una **pestaña nueva** y navega a `https://gemini.google.com/app`.
4. Comprueba la sesión. Si aparece "Iniciar sesión" o "Sign in", pide al usuario que inicie sesión por su cuenta y espera. **Nunca introduzcas credenciales.** Si aparece un aviso de términos, de cookies o de novedades, pide al usuario que lo resuelva por su cuenta: no aceptes acuerdos en su nombre.
5. **Espera a que la página termine de cargar** (el cuadro de la petición visible y vacío): lo que se escribe mientras carga se pierde. Escribe en el cuadro `Generate an image: <prompt>`, envíalo y **comprueba que el prompt aparece en la conversación**; si no, vuelve a escribirlo. Después de refrescar no lo reenvíes: la conversación se conserva. En una edición nueva de un mapa, primero intenta editar la anterior (ver «Edición nueva» en `mapas.md`).
6. **Espera la imagen.** Gemini a veces termina de generar pero deja el **recuadro gris** hasta que se refresca la página; la conversación se conserva al refrescar.
   1. Comprueba cada 10 segundos, con una captura o buscando el botón (`find`: "Descargar" / "Download"), si ya aparece el **icono de la flechita de descarga** sobre la respuesta. Es la señal de que la imagen está generada.
   2. Cuando aparezca, si la imagen se ve, sigue con el Paso 3b.
   3. Si sigue el recuadro gris, **refresca la página** y espera 10 segundos.
   4. Si tras el primer refresco sigue gris, **refresca una segunda vez** y espera 15 segundos.
   5. Si aun así no se ve pero el icono de descarga está, intenta descargarla igualmente: la descarga suele funcionar aunque la vista previa falle.
   6. Si en 3 minutos no aparece ni la imagen ni el icono, ve a "Si algo falla".
7. **Si Gemini rechaza la petición o responde solo con texto,** suaviza el prompt (más sugerido, menos explícito) y reintenta una vez en el mismo chat.
8. **Acepta la primera imagen que pase la comprobación** (Paso 3c). Si el usuario quiere otra, la pedirá después (la de ahora se archivará y quedará enlazada en la nota).

## Paso 3b: descargar y guardar
1. Ejecuta `python <directorio de la skill>/scripts/fetch_download.py mark` y guarda la marca que imprime.
2. Pulsa el botón de descarga de la imagen ("Descargar imagen en tamaño completo" / "Download full size image"; aparece al pasar el ratón sobre la imagen).
3. Ejecuta:
   ```bash
   python <directorio de la skill>/scripts/fetch_download.py fetch --since <marca> --dest "<bóveda>/00_Sistema/02_Activos/<Carpeta>" --name <Prefijo><Nombre_de_la_nota>
   ```
   El script imprime el nombre del archivo, el tamaño y el nombre original de la descarga. Si ya existía un archivo con ese nombre, usa `_v2`, `_v3`…; al aceptar una, `keep` le pone el nombre de siempre (Paso 4).
4. Si el script no encuentra la imagen (la descarga no arrancó), pulsa de nuevo el botón y repite el paso 3.
5. Si Chrome abre un diálogo para elegir dónde guardar, la extensión no puede manejarlo. Pide al usuario que guarde en su carpeta de Descargas, o que desactive en Chrome "Preguntar dónde se guardará cada archivo", y repite el paso 3.

## Paso 3c: comprobar la imagen
Toda imagen se comprueba, no solo los mapas. Mira la imagen guardada (léela con la herramienta de lectura de archivos) y compárala con lo que se pidió:
- **Toda imagen:** repasa uno por uno los elementos de su «Descripción visual» (el sujeto y los rasgos que lo definen: «sin ojos», «la corona partida en dos», «la mujer de la capa roja en el puente»); en un retrato, una sola figura; ningún texto, marco ni firma (tampoco un recuadro dibujado alrededor; la marca de agua de Gemini no cuenta); nada que rompa los pilares de la Ficha (una técnica o una época que no tocan); la técnica y la paleta de la Guía; el formato pedido.
- **Un mapa,** además, lo que dice «Comprobación» en `mapas.md`. Lo primero son los marcadores: todos, una vez cada uno.

Si algo falla, pide la corrección **en el mismo chat de Gemini**, nombrando el problema exacto y pidiendo que no cambie nada más. Descarga y guarda la imagen corregida (Paso 3b) y vuelve a comprobar. Como mucho dos correcciones: después, quédate con la mejor, enlázala y anota lo que quedó mal en las incidencias. Los intentos descartados no se borran: los archiva `keep` (Paso 4).

Corrige lo que contradice lo pedido, no lo que podría estar mejor: un detalle pequeño menos logrado no es un fallo.

**El resultado queda en la nota:** en la línea del prompt de la imagen, ` · comprobada: <lo que se comprobó, en pocas palabras>` y, si algo quedó mal tras las correcciones, detrás, ` · con fallos: <solo lo que quedó mal>` (` · comprobada: la mujer de la capa roja, el puente de cuerdas, el río en el fondo · con fallos: el escudo del fondo lleva unos trazos que parecen letras`); en un mapa, en la línea de su edición (`comprobado: 12/12 marcadores, sin repetidos`). Una corrección que salió bien no va en la nota, sino en las incidencias del informe.

## Paso 4: enlazar en la nota
- **Primero, deja la aceptada con su nombre** y archiva lo demás, sin borrar nada:
  ```bash
  python <directorio de la skill>/scripts/fetch_download.py keep --dest "<bóveda>/00_Sistema/02_Activos/<Carpeta>" --name <Prefijo><Nombre_de_la_nota> --new <archivo aceptado> [--label <etiqueta>]
  ```
  - La aceptada queda como `<Prefijo><Nota>.<ext>` (la línea «Vigente»): es el **nombre final**, así que la nota no cambia de enlace, salvo la extensión si cambió.
  - Lo que había con ese nombre va a `02_Activos/Anteriores` con su `--label`: `ed<n>` si era la edición n de un mapa; `descartada` si era un intento de esta misma vez (la primera vez que se dibuja, cuando hubo que corregir); sin `--label` en una imagen regenerada, que queda como `_v1`, `_v2`…
  - Los intentos `_v2`, `_v3`… de esta vez que no se aceptaron quedan como `_descartada`.
  - Si el script crea la carpeta `Anteriores`, regístrala en «Carpetas añadidas por skills» de la Guía de Organización: `| 00_Sistema/02_Activos/Anteriores | Imágenes reemplazadas: ediciones anteriores de los mapas (_ed<n>), versiones anteriores (_v<n>) e intentos descartados (_descartada) | generar-imagen |`.
- **Lo anterior, enlazado:** si `keep` archivó una imagen que no era un descarte, la nota la enlaza para poder volver a ella: en la sección Imagen, `- **Versiones anteriores:** [[Retrato_X_v1.jpg|versión 1]]` (cada una se añade a la lista); en un mapa, en su sección Mapa (ver «Guardar y enlazar» en `mapas.md`). Para volver a una anterior, muévela de `Anteriores` a su carpeta con un nombre `_v<n>` y pásala a `keep` como aceptada: la vigente se archiva a su vez.
- Propiedad `imagen: "[[<nombre final>]]"`, con su extensión real.
- Embed justo debajo del resumen en cita: `![[<nombre final>|300]]` para retratos y otras imágenes cuadradas, `![[<nombre final>|600]]` para las apaisadas. Sustituye al anterior si regeneras.
- En la sección Imagen, `**Prompt:**` con la fecha de generación, la técnica, el modelo y la comprobación (`2026-10-10 · técnica: Boceto en acuarela (acuarela) · modelo: Gemini (navegador) · comprobada: la mujer de la capa roja, el puente de cuerdas, el río en el fondo`) y, debajo, el prompt en un bloque de código, tal cual se generó pero **sin** la orden `Generate an image:`, que es para Gemini. Así se puede reutilizar.
- Actualiza `ultima_revision` (sin comillas).
- **Un mapa** se enlaza como dice «Guardar y enlazar» en `mapas.md`: la propiedad `mapa`, el mapa embebido y la línea de la edición en la sección Mapa, el prompt del mapa en la sección Imagen y, al final, `map_key.py <Nota> --charted`.

## Paso 5: informe
Si la invocó `crear-entidad` o `expandir-mundo`, devuélveles el nombre del archivo, la técnica usada y las incidencias: la imagen sale en su informe final y en su entrada de la Bitácora. Si se invocó sola, añade una entrada a la **Bitácora** (`00_Sistema/Bitacora.md`):
```bash
python <crear-entidad>/scripts/log_entry.py --title "Imagen: <Nombre>" --line "**Nueva imagen** de [[<Nota>|<Nombre>]] en <técnica> (<versión>)."
```
Para un mapa, `--title "Mapa: <Nombre>" --line "**Edición <n> del mapa** de [[<Nota>|<Nombre>]]: <zonas> zonas, comprobado <x>/<y> marcadores."`. Y termina con:
- **Imagen:** enlace al archivo guardado, relativo al directorio de trabajo (`[Retrato_Aldric_Voss.png](World_Building/00_Sistema/02_Activos/Ilustraciones/Personajes/Retrato_Aldric_Voss.png)`), su tamaño y el nombre original de la descarga (los imprime `fetch_download.py`), y una línea sobre lo que muestra.
- **Técnica:** cuál y por qué: pedida para esta imagen, la del tipo, la general o sorteada (con la tirada).
- **Nota actualizada:** enlace a la nota y lo que cambió en ella: la propiedad `imagen`, el embed y el prompt en la sección Imagen.
- **Prompt usado**, en un bloque de código.
- **Comprobación:** qué se comprobó y si algo quedó mal.
- **Versión:** si es una regeneración o una edición nueva, dónde quedó la anterior (archivada en `Anteriores` y enlazada en la nota) y los intentos descartados.
- **Mapa** (si se dibujó): la edición, los niveles dibujados, la comprobación de los marcadores (`12/12, sin repetidos`), si se editó la edición anterior o se redibujó, y los detalles inventados para la leyenda (las salas menores de una mazmorra).
- **Comprobación e incidencias**, si las hubo: inicio de sesión, refrescos por el recuadro gris, reintentos, prompt suavizado y las correcciones que se pidieron en la comprobación, con lo que quedó mal.
- **Marca de agua:** la primera vez en el mundo, avisa de que las imágenes de Gemini llevan una marca de agua visible y SynthID.
- **Guía Visual:** si se creó o cambió en esta ejecución, enlace a ella y la técnica elegida. Recuerda cuántas técnicas hay (están en la sección "Técnicas disponibles" de la Guía) y que se puede pedir otra para una imagen o fijar una por tipo.

## Si algo falla
Si no se puede generar la imagen (Chrome no está disponible, no hay sesión, Gemini la rechaza tras el reintento o no aparece en 3 minutos):
- guarda el prompt en la sección Imagen de la nota;
- deja `imagen` vacío para generarla más tarde;
- explica al usuario qué pasó y cómo seguir: generarla más tarde con `/generar-imagen <nota>`.

Si falla un mapa, la leyenda se queda como estaba y no se ejecuta `map_key.py --charted`: la edición sigue pendiente y se puede dibujar más tarde con `/generar-imagen <nota> mapa`.

Nunca dejes la nota a medias.

## Reglas
- No borres imágenes: la que se reemplaza y los intentos descartados se archivan en `02_Activos/Anteriores` (`keep`), y lo anterior queda enlazado en la nota.
- **Credenciales:** el inicio de sesión en Google lo hace siempre el usuario en su navegador; nunca introduzcas credenciales ni aceptes acuerdos en su nombre.
- La skill es genérica: el estilo de cada mundo vive en su Guía Visual, nunca aquí. El catálogo de técnicas sí es de la skill: una técnica nueva se añade a `tecnicas.md` con su sección (bloques, Color, 📄 si es sobre papel) y en el índice, actualizando los totales del índice y el de la introducción de esta skill.
