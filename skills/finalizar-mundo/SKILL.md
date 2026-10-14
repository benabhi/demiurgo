---
name: finalizar-mundo
description: Lleva un mundo a su cierre y lo deja impecable. Por fases y con el usuario, resuelve los pilares por definir y las preguntas abiertas (pueden quedar misterios a propósito), cierra cada enlace pendiente (lo crea, lo disuelve o lo fusiona), revisa todos los borradores, completa imágenes y mapas, y deja cada nota sin errores ni anotaciones de trabajo. Mientras dura el cierre, el mundo deja de crecer; cuando todo está en verde, queda cerrado, y crear falla hasta que se reabra. Usar para "cierra el mundo", "/finalizar-mundo", "¿qué falta para terminar el mundo?" o "reabre el mundo".
---

# Finalizar el mundo

Un mundo cerrado no tiene cabos sueltos: todo lo que nombra existe, todo está revisado y en canon, cada pregunta tiene respuesta (o es un misterio a propósito), y cada nota, imagen y mapa está completo. Esta skill lo lleva hasta ahí por fases, siempre con el usuario, y lo cierra.

Uso: `/finalizar-mundo` (dice qué falta y sigue por donde quedó), o `/finalizar-mundo reabrir <motivo>`.

## El estado del mundo
Está en la Ficha, en `estado_mundo`, y es una de tres:
- **`abierto`:** se crea de todo. Sin la propiedad, el mundo está abierto.
- **`en_cierre`:** el mundo ya no crece; solo se cierran cabos.
  - Ninguna nota abre enlaces pendientes nuevos: lo menor se nombra sin nombre propio. El informe de cada creación lo comprueba.
  - `crear-entidad` solo completa enlaces pendientes.
  - El motor entra en modo cierre: completa enlaces pendientes sin abrir ninguno y dibuja los mapas con cualquier cambio sin dibujar. No crea nada nuevo, ni rutas, ni profundiza.
- **`cerrado`:** no se crea nada. `crear-entidad` y el motor se niegan a empezar. Se puede consultar (`consultar-mundo`), narrar (`narrar`) e ilustrar (`generar-imagen`).

## La lista del cierre
```bash
python <directorio de esta skill>/scripts/close_world.py
```
Da el estado del mundo, cada criterio en verde o en rojo, y lo siguiente que toca. Para cerrar, todo en verde:
- **Pilares por definir:** decididos, o sin definir a propósito (un misterio).
- **Preguntas abiertas:** ninguna. Cada una queda confirmada, rechazada, respondida o como misterio.
- **Enlaces pendientes:** ninguno. Lo de fuera de un mundo que es una ciudad o una región (tipo `fuera`) es referencia a propósito y no cuenta.
- **Borradores:** ninguno, todo pasó por `revisar-mundo`.
- **Notas impecables:** todas pasan `check_note` sin errores ni avisos. Ninguna, tampoco el Glosario, tiene anotaciones de trabajo: «por definir», «por confirmar», «sin cartografiar», restos de plantilla.
- **El auditor:** sin errores ni avisos.
- **Imágenes:** cada entidad tiene la suya (los secretos no llevan).
- **Mapas:** todos al día, sin un solo cambio por dibujar, y lo más alto del mapa con el suyo.
- **Ni imágenes sueltas ni notas en la Bandeja de Entrada.**

Muéstrala en el chat en pocas líneas: los criterios en rojo, con su detalle, y lo siguiente.

## Paso 0: empezar
Si el mundo está abierto, explica en pocas líneas qué cambia en el cierre (deja de crecer, solo se cierran cabos) y pregunta con AskUserQuestion si empezamos. Si dice que sí:
```bash
python <directorio de esta skill>/scripts/close_world.py start
```
El mundo pasa a `en_cierre`. Queda una línea en el Registro de Canon y una entrada en la Bitácora.

## Las fases
Cada vez se sigue por el primer criterio en rojo. El usuario puede parar cuando quiera: la lista dice siempre qué falta. Las preguntas al usuario van en pantallas de 4 (AskUserQuestion), y lo que él decide se aplica antes de seguir.

### 1. Los pilares por definir
Van primero, porque las fechas de todo dependen del calendario. Por cada uno:
- **Decidirlo:** el usuario da el valor, o elige entre tres propuestas coherentes con la Ficha. Se escribe en la Ficha y en las reglas de `CLAUDE.md`, con una línea en el Registro de Canon. Después:
  ```bash
  python <directorio de esta skill>/scripts/close_world.py resolve "<pilar>" respondida --note "<lo decidido>"
  ```
  El calendario se crea con `/crear-entidad calendario` (ver `referencias/pilares.md` de `crear-entidad`). Después, las notas que dicen «el calendario está por definir» pasan a tener sus fechas.
- **Misterio:** `resolve "<pilar>" misterio --note "<por qué>"`. La Ficha queda en «Sin definir, a propósito».

### 2. Las confirmaciones y las preguntas
- **Una confirmación** se confirma o se rechaza:
  - **Confirmar:** `resolve "<texto>" confirmado`. Su sujeto queda libre para crearse.
  - **Rechazar:** `resolve "<texto>" rechazado`. Después, lo que la afirmaba deja de afirmarlo: si su sujeto es un enlace pendiente, se disuelve (fase 3); si tiene nota, se archiva con `/revisar-mundo`; y las notas que lo cuentan se corrigen.
- **Una pregunta** se responde o queda como misterio:
  - **Responder:** propón una respuesta coherente con el mundo y el usuario la aprueba o la cambia. Va donde corresponde: en la nota de lo que trata, o en un secreto si es una verdad oculta. Después, `resolve "<texto>" respondida --note "<dónde quedó>"`.
  - **Misterio:** `resolve "<texto>" misterio --note "<por qué>"`. Si su verdad existe, puede ir en un secreto.

### 3. Los enlaces pendientes
La lista los separa: los que se pueden crear, los que esperan una confirmación (fase 2), los que no tienen tipo y los que no tienen módulo. Aparte señala los **menores**: los que nombra una sola nota, poco y que no pesa mucho.
- **Menores:** propónselos al usuario para disolverlos, por pantallas. Los que elija, se disuelven:
  ```bash
  python <crear-entidad>/scripts/dissolve_link.py <Enlace> --term <clase> "<definición>" --reason "<por qué no tiene nota>"
  ```
  El enlace pasa a texto en todas las notas y sale de las propiedades de relación. En el mapa, su zona se queda con el nombre y sin enlace. Queda como término del Glosario, con una clase que no sea un tipo de entidad («nombre de lugar», «relato», «expresión»), así ninguna nota tiene un nombre propio suelto. Si es mejor que esas menciones no tengan nombre propio, reescríbelas y disuelve sin `--term`. La decisión queda en el Registro de Canon. Los que el usuario no elija, se crean.
- **Otro nombre de algo que ya existe:** se fusiona con `rename_link.py <Viejo> <Nuevo>`.
- **Sin tipo:** se le da (`pending_links.py --set <Enlace>=<tipo>`) o se disuelve.
- **Sin módulo:** se disuelve, porque ningún tipo lo crea.
- **El resto se crea:** `/expandir-mundo <n>` (en cierre, solo completa y sin abrir ninguno nuevo; se detiene con 20 borradores del motor sin revisar, y entonces se revisan), o `/crear-entidad <tipo> hueco=<Enlace>` para uno concreto. Si el informe de una creación dice que se abrieron enlaces pendientes nuevos, se corrige antes de seguir: lo nuevo, sin nombre propio, o disuelto.

### 4. Los borradores
`/revisar-mundo`, eligiendo «Todos», hasta que no quede ninguno. Un borrador archivado para rehacerlo vuelve a ser un enlace pendiente, que se crea en la fase 3. Uno quitado del mundo deja menciones que se reescriben.

### 5. Notas impecables y el auditor
Corrige lo que señala la lista:
- **Los avisos y errores de `check_note`.**
- **Las anotaciones de trabajo:**
  - un «por definir» o un «por confirmar» se cambia por lo decidido, o se quita;
  - en el Glosario, una definición «(por confirmar)» pasa a ser la confirmada, o el término sale.
- **Lo que señala `audit_world.py`.**

Cada corrección se hace como lo haría `crear-entidad`. Si la nota está en canon, deja su línea en el Registro de Canon.

### 6. Imágenes y mapas
- Las imágenes que faltan: `/generar-imagen <Nota>`.
- Los mapas atrasados, aunque les falte una sola zona: `/generar-imagen <Nota> mapa`, o el motor, que en cierre los dibuja.
- Lo más alto del mapa tiene que tener el suyo: el mapa del mundo, o el de la ciudad en un mundo que es una ciudad.

### 7. Lo suelto
- **Imágenes sueltas:** `close_world.py tidy` las aparta a `02_Activos/Anteriores` con `_suelta`. No se borran.
- **Bandeja de Entrada:** cada nota va a donde corresponde, como entidad o como parte de una, o al archivo.

### 8. Cerrar
Con todo en verde:
```bash
python <directorio de esta skill>/scripts/close_world.py close
```
El mundo pasa a `cerrado`, con su línea en el Registro de Canon y su entrada en la Bitácora, y las Estadísticas se rehacen. El script da el resumen del mundo terminado (de las Estadísticas) y lo que hizo el cierre: cuánto pasó a canon, se archivó, se quitó o se disolvió, y cómo se cerraron las preguntas.

## Informe
En el chat, con los enlaces en Markdown y la ruta del archivo, nunca `[[...]]`:
- en cada sesión, la lista con lo que queda en rojo, lo que se hizo y lo siguiente;
- al cerrar, el resumen del mundo terminado y lo que hizo el cierre.

Al cerrar, si la bóveda está en git, ofrece un commit del mundo cerrado con una etiqueta (`mundo-cerrado-<fecha>`). Hazlo solo si el usuario dice que sí, y sin los archivos de `.obsidian`.

## Reabrir
`/finalizar-mundo reabrir <motivo>`:
```bash
python <directorio de esta skill>/scripts/close_world.py reopen --reason "<motivo>"
```
El mundo vuelve a `abierto`, con su línea en el Registro de Canon y su entrada en la Bitácora.

## Reglas
- Lo que importa lo decide el usuario: los pilares, las confirmaciones, las respuestas, lo que se disuelve y lo que se archiva.
- No se borra nada: lo archivado y las imágenes apartadas se conservan.
- En cierre, ninguna nota abre enlaces pendientes nuevos.
- La lista manda: el mundo solo se cierra con todo en verde, y siempre se empieza por ella.
- La skill es genérica: nada de un mundo concreto en sus textos ni en sus ejemplos.
