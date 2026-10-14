---
name: diagnosticar-mundo
description: Diagnostica la bóveda de un mundo. Dice qué está mal (notas que no pasan la validación, imágenes rotas o sueltas, errores del auditor), qué se quedó atrás respecto a las skills (el CLAUDE.md, las guías y las plantillas, las propiedades nuevas de cada tipo, la Ficha, el grafo, las notas del sistema, los archivos del motor, las skills instaladas) y qué pide atención (borradores, enlaces pendientes, preguntas, mapas por dibujar, imágenes que faltan). Aplica solo los arreglos seguros y propone los demás. Úsala para "¿cómo está la bóveda?", "¿está todo bien?", "health check", "actualicé las skills", "/diagnosticar-mundo".
---

# Diagnosticar el mundo

Dice cómo está la bóveda: qué está mal, qué se quedó atrás respecto a las skills y qué pide atención. Arregla solo lo seguro y propone el resto.

Usa las mismas comprobaciones que `/finalizar-mundo` (`health.py`, de `crear-entidad`), pero con el criterio de un mundo abierto: los enlaces pendientes, los borradores y las preguntas no son errores, sino un mundo que crece.

Uso: `/diagnosticar-mundo`, o «¿cómo está la bóveda?». Conviene después de actualizar las skills (`git pull`), al retomar un mundo tras un tiempo o si algo parece raro.

## Qué mira
- **Salud:** lo que está mal.
  - Las notas que no pasan `check_note.py` (las propiedades que les faltan por ser anteriores a su plantilla van en «Al día»).
  - Las imágenes enlazadas que no existen.
  - Los errores del auditor.
  - Las imágenes sueltas: las de `02_Activos` que ninguna nota usa.
- **Al día con las skills:** lo que cambió en las skills desde que se creó la bóveda.
  - El `CLAUDE.md` y las guías de `04_Convenciones`, frente a su versión actual en `inicializar-mundo`: las líneas que les faltan. No mira las reglas de contenido ni lo que sale de las respuestas de la entrevista.
  - Las plantillas instaladas en `01_Plantillas`: las propiedades y las secciones nuevas de su tipo.
  - Las notas a las que les faltan propiedades nuevas de su tipo.
  - La Ficha: su estado (`estado_mundo`).
  - El grafo: el color de los tipos nuevos.
  - Las notas del sistema: la Bitácora, las Estadísticas y el registro de enlaces pendientes.
  - Los archivos del motor (`06_Generacion`), si ya se usó.
  - Las skills instaladas: las que no están en `.claude/skills` del proyecto ni en `~/.claude/skills`.
- **Atención:** lo que no es un error pero espera algo, con la skill que lo resuelve. Los borradores (y si el motor está cerca de detenerse), los enlaces pendientes, las preguntas abiertas, los pilares por definir, los mapas por dibujar, las entidades sin imagen, los avisos del auditor y la Bandeja de Entrada.

## Paso 1: diagnosticar
Ejecuta `python <directorio de esta skill>/scripts/diagnose.py` (con `--vault <carpeta>` si la bóveda no está en `World_Building/`). Solo lee: no cambia nada.

Si el mundo está en cierre, recuérdalo: entonces manda la lista de `/finalizar-mundo`. Si está cerrado, sus notas ya no cambian: `--migrate` se niega, y los demás arreglos solo tocan el sistema (las notas del sistema, las plantillas, el grafo).

## Paso 2: los arreglos seguros
Si hay líneas con ✗ y `(--fix)`, aplícalos sin preguntar con `diagnose.py --fix`. Solo completan o rehacen lo que las skills mantienen solas, sin tocar lo escrito:
- ponen el estado en la Ficha (`estado_mundo: abierto`) si falta;
- crean la Bitácora si falta;
- rehacen el registro de enlaces pendientes y las Estadísticas;
- copian los archivos del motor que falten (nunca sobrescriben);
- añaden al grafo el color de los tipos nuevos. Si Obsidian tiene un grafo abierto, guarda el suyo encima: avisa al usuario de que lo cierre y abra el marcador «Grafo completo».

## Paso 3: lo que pide visto bueno
Pregunta con AskUserQuestion antes de cada uno de estos arreglos (una pregunta por arreglo, todas en la misma llamada), con lo que dice el diagnóstico:
- **`--templates`:** añade a las plantillas instaladas las propiedades y las secciones nuevas de su tipo. Solo añade, pero el usuario pudo personalizarlas.
- **`--migrate`:** añade a las notas las propiedades nuevas de su tipo, vacías (`""` o `[]`) y en su sitio. Di a cuántas notas afecta. Después, `check_note.py` puede pedir un valor en alguna (una propiedad obligatoria solo en ciertos casos): rellénalo con lo que ya dice la nota o déjalo anotado para `/revisar-mundo`.
- **`--tidy`:** aparta a `02_Activos/Anteriores`, con `_suelta`, las imágenes que ninguna nota usa. No borra nada.
- **El `CLAUDE.md` y las guías:** `diagnose.py --details` muestra cada línea que falta, entera, con su sección y la línea tras la que va. Enséñaselas al usuario y, con su visto bueno, incorpóralas con Edit:
  - si la línea nueva es otra versión de una que ya está (la skill cambió la redacción), reemplaza la vieja en lugar de duplicarla;
  - si el usuario la quitó a propósito, déjala fuera;
  - una guía que no está se rehace desde su plantilla (`--details` dice cuál), con los datos de la Ficha en sus marcadores.

Las opciones se combinan en una sola ejecución (`--fix --templates --migrate`). Lo que el usuario no quiera queda en el diagnóstico; no insistas.

## Paso 4: lo que esta skill no arregla
Los errores de las notas y lo de «Atención» se resuelven con su skill:
- **notas con errores y avisos del auditor:** si son pocos y claros, corrígelos con el visto bueno del usuario; si no, propón `/revisar-mundo`;
- **borradores:** `/revisar-mundo`;
- **enlaces pendientes:** `/expandir-mundo` o `/crear-entidad`;
- **mapas por dibujar y entidades sin imagen:** `/generar-imagen`;
- **preguntas abiertas y pilares por definir:** las decide el usuario cuando quiera, o todas al cerrar el mundo con `/finalizar-mundo`;
- **la Bandeja de Entrada:** son ideas sueltas del usuario; ofrece convertirlas en entidades con `/crear-entidad`;
- **las skills que faltan:** el README de Demiurgo (https://github.com/benabhi/demiurgo) explica cómo instalarlas.

## Paso 5: informe
Vuelve a ejecutar `diagnose.py`, sin opciones, y da un informe breve:
- **el estado de la bóveda:** lo que está bien, en una línea, y cada ✗ que queda con su motivo (lo que el usuario no quiso, lo que pide otra skill);
- **lo arreglado,** con enlaces que se abran (`[Nombre](<bóveda>/<ruta>)`): las notas, las plantillas y las guías que cambiaron;
- **lo de «Atención»,** con la skill que lo resuelve.

Los arreglos del script dejan solos su entrada en la Bitácora («Diagnóstico de la bóveda»). Lo que incorpores tú al `CLAUDE.md` o a las guías anótalo con `python <crear-entidad>/scripts/log_entry.py --title "Guías al día" --line "<qué se añadió y dónde>"`.

## Reglas
- **Sin `--fix` ni otra opción, no cambia nada.** Las opciones nunca borran ni sobrescriben lo escrito: solo añaden, completan o rehacen lo que mantienen las skills.
- **No decide nada del mundo:** no resuelve preguntas, no crea entidades y no cambia el estado del mundo.
- **No hace commits.** Si la bóveda es un repositorio git, los cambios quedan para que el usuario los revise.
- **En el chat,** los enlaces van en Markdown con la ruta del archivo; nunca `[[...]]`.
