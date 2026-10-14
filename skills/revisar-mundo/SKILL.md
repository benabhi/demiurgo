---
name: revisar-mundo
description: Repasa con el usuario los borradores del mundo (lo que crearon crear-entidad y el motor): le dice cuántos hay, él elige cuántos revisar, y aplica lo que decide de cada uno: pasa a canon, sigue en borrador, se archiva para rehacerlo o se quita del mundo, con sus imágenes, sus secretos, su zona en los mapas y las notas que lo nombran. Úsala para "revisa los borradores", "/revisar-mundo", "pasa a canon…", "archiva…" o cuando el motor se detiene por tener demasiados borradores sin revisar.
---

# Revisar el mundo

Todo lo que crean `crear-entidad` y el motor nace como `borrador`; solo el usuario lo hace canon. Esta skill le dice cuántos borradores hay, le deja elegir cuántos revisar y los repasa de lo que más pesa a lo que menos, en pantallas de 4, aplicando lo que decide de cada uno.

Uso: `/revisar-mundo`, y te dice cuántos hay y te pregunta cuántos revisar. Si lo dices al pedirlo, no pregunta: `/revisar-mundo 12`, `/revisar-mundo personajes`, «solo lo del motor», «solo lo mío».

## Leer sin gastar tokens
- La cola y la ficha de cada borrador las da un script: no leas las notas enteras para presentarlas.
- Lee una nota solo para cotejarla (Paso 2) o para aplicar una corrección.
- Para lo demás, los scripts de `crear-entidad`: `search_vault.py`, `build_context.py`, `audit_world.py --focus`.

## Paso 1: cuántos
```bash
python <directorio de esta skill>/scripts/review_queue.py --summary
```
Da el recuento, sin fichas: cuántos borradores hay (del motor y a mano), los secretos, los ya revisados que siguen en borrador, cuántos hay de cada tipo, los que más pesan y cuánto le falta al motor para detenerse. Muéstralo en pocas líneas.

Si el usuario no dijo cuántos revisar, pregúntalo con AskUserQuestion: «¿Cuántos revisamos ahora?». Las opciones dependen de cuántos hay:
- **4:** una pantalla.
- **8:** dos pantallas; solo si hay más de 8 (si no, «Todos» ya los cubre).
- **Todos:** con el número (por ejemplo, «Todos (23)»), en pantallas de 4.
- **Solo los del motor:** con el número; solo si hay borradores de los dos orígenes.
- **«Other»:** un número, un tipo («los personajes»), o lo que el usuario quiera.

Si hay 4 o menos, no preguntes: revísalos todos.

## Paso 1b: la tanda
```bash
python <directorio de esta skill>/scripts/review_queue.py --limit <los que eligió> [--type <tipo>] [--origin procedural|manual]
```
Dice cuáles entran en la tanda. De cada uno da una ficha:
- su tipo, relevancia, origen y fecha, y su resumen;
- quién lo enlaza, y cuántas de esas notas están en canon;
- lo que propuso al crearse y espera confirmación en Preguntas Abiertas;
- sus secretos, su imagen y su mapa;
- los enlaces pendientes que solo nombra él (si se quita del mundo, desaparecen);
- los avisos del auditor sobre él.

El orden: primero lo que más pesa (relevancia y notas que lo enlazan), porque fijarlo en canon ancla lo demás; cada secreto, detrás de su entidad; al final, lo que ya se revisó y siguió en borrador.

## Paso 2: cotejar
Antes de mostrar cada ficha, una comprobación breve, sin leer de más:
- **La Ficha** (ya está en el contexto): ¿la contradice en especies, tecnología, poderes, tono o vetos?
- **El canon:** si la enlazan notas en canon, o ella enlaza a alguna, ¿choca con lo que cuentan? Mira `build_context.py --target <Nota>` y lee solo lo que haga falta.
- **La Guía de Canon:** ¿respeta los sistemas del mundo?, ¿sus términos nuevos están en el Glosario (`search_vault.py`)?

Si encuentras algo, añádelo a su ficha («Ojo: …»). Si no, nada: no inventes problemas.

## Paso 3: mostrar y decidir
Muestra en el chat las fichas de una pantalla (hasta 4), con los enlaces en Markdown tal como los da el script (nunca `[[...]]`) y los secretos marcados 🔒. Después, una sola llamada a AskUserQuestion, con una pregunta por borrador:
- **Encabezado:** su nombre, abreviado si pasa de 12 caracteres.
- **Opciones:**
  - **Canon:** pasa a canon, y lo que propuso queda confirmado.
  - **Sigue en borrador:** se queda como está y vuelve al final de la cola.
  - **Archivar y rehacer:** se archiva la nota, y la entidad vuelve a ser un enlace pendiente para crearla de nuevo, distinta.
  - **Quitar del mundo:** se archiva y la entidad desaparece del mundo; se reescriben sus menciones.
- **«Other»:** una corrección («más joven», «otro nombre», «que no sea noble»), o el motivo de lo que eligió.

Un secreto no lo enlaza nadie, así que archivarlo de una forma o de la otra es lo mismo: ofrece Canon, Sigue en borrador y Archivar (y aplícalo como `--quitar`).

## Paso 4: aplicar
```bash
python <directorio de esta skill>/scripts/review_apply.py --canon <Notas> --keep <Notas> --rehacer <Notas> --quitar <Notas> [--reason "<motivo>"]
```
Cada nota, por su nombre de archivo sin `.md`. `--reason` lleva el motivo que dio el usuario al Registro de Canon y a la nota archivada; con motivos distintos, una llamada por motivo.
- **Canon:** `estado: canon` y la fecha. Las «Confirmar: …» que propuso, o de las que es el sujeto, quedan hechas. Una línea en el Registro de Canon.
- **Sigue en borrador:** anota `revisado` con la fecha (la cola lo deja para el final).
- **Archivar, de las dos formas:**
  - la nota va a `00_Sistema/03_Archivados`, con `estado: archivado` y una línea bajo el título que dice cuándo y por qué;
  - sus imágenes (la suya, su mapa y sus versiones anteriores) van a `02_Activos/Anteriores` con `_archivada`, y la nota archivada las sigue enlazando;
  - los secretos que solo afectan a lo que se archiva van con ello;
  - una línea en el Registro de Canon.
- **Rehacer:** la nota archivada pasa a llamarse `<Nota>_archivada`, así sus menciones vuelven a ser enlaces pendientes, con su tipo: el motor, o `/crear-entidad <tipo> hueco=<Nota>`, la creará de nuevo con el mismo nombre. Si el usuario dijo cómo la quiere, anótalo para quien la cree: `add_entries.py --question "Al rehacer [[<Nota>]]: <lo que pidió>"`.
- **Quitar:** la nota archivada conserva su nombre, así sus menciones no quedan pendientes y nada la vuelve a crear; el auditor avisa de cada una hasta que se reescribe. Su zona en la leyenda del mapa que la contiene se retira (se quita en la edición siguiente). El script lista las menciones que hay que reescribir.
- Al final, rehace el registro de enlaces pendientes y propone las líneas de la Bitácora.

## Paso 5: lo que queda por hacer a mano
- **Quitar:** reescribe una por una las menciones que lista el script.
  - La frase deja de depender de lo que se quitó, o lo nombra sin nombre propio («una mina del norte»), y sale de sus propiedades de relación.
  - Si la nota está en `canon`, deja una línea en el Registro de Canon.
  - Después, `audit_world.py --focus <notas>`: no debe quedar ningún aviso de «se quitó del mundo».
- **Corrección:** aplícala como lo haría `crear-entidad` (su `tipo.md`, los enlaces, `check_note.py`, el Glosario), sin rehacer lo que no se pidió. La nota sigue en borrador (`--keep`), salvo que el usuario diga que pase a canon.
- **Carpeta nueva:** si el script avisa de que creó `02_Activos/Anteriores`, regístrala en la Guía de Organización.

## Paso 6: siguiente pantalla y cierre
- Sigue con la pantalla siguiente hasta completar los que eligió el usuario.
- Al terminar, una sola entrada en la Bitácora para toda la tanda, con las líneas que propuso el script en cada pantalla, juntas:
  ```bash
  python <crear-entidad>/scripts/log_entry.py --title "Revisión de borradores" --line "…" --line "…"
  ```
  Rehace también las Estadísticas: lo archivado deja de contar como entidad y pasa a «archivadas».
- Informe en el chat, con los enlaces en Markdown y la ruta del archivo, nunca `[[...]]`:
  - qué pasó a canon y qué confirmaciones quedaron hechas;
  - qué sigue en borrador;
  - qué se archivó y de qué forma, con sus imágenes y sus secretos;
  - qué menciones se reescribieron;
  - cuántos borradores quedan, y si el motor ya puede seguir (se detiene con 20 borradores suyos sin revisar).

  Dile cuántos quedan y pregúntale si sigue con otra tanda, y de cuántos.

## Reglas
- Solo el usuario decide: nunca pases nada a canon ni lo archives sin su respuesta.
- No se borra nada: lo archivado se conserva, con sus imágenes.
- Una nota en canon no se revisa aquí. Para cambiarla, se edita y se deja constancia en el Registro de Canon.
- La skill es genérica: nada de un mundo concreto en sus textos ni en sus ejemplos.
