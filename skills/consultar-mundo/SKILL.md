---
name: consultar-mundo
description: Responde preguntas sobre el mundo con lo que dice la bóveda, sin leerla entera ni inventar. Sirve para saber qué es algo o quién es alguien, qué hay en un lugar, cuánto se tarda entre dos sitios, qué pasó y cuándo, qué se cree y qué es verdad, o qué falta por decidir. Cita las notas, distingue el canon de los borradores y aparta los secretos; «sin spoilers», no los muestra. Úsala para cualquier pregunta sobre el mundo ("¿quién gobierna…?", "¿qué hay en…?", "¿cuánto se tarda de… a…?", "¿qué pasó en…?", "/consultar-mundo …"). No crea ni cambia nada.
---

# Consultar el mundo

Responde preguntas sobre el mundo con lo que dice la bóveda. No la lee entera ni inventa: cada respuesta sale de los scripts de consulta y de las secciones que hagan falta, y cita sus notas.

Uso: `/consultar-mundo <pregunta>`, o cualquier pregunta sobre el mundo.

## Reglas
- **Solo lo que dice la bóveda.** Si algo no consta, dilo y no lo rellenes. Puedes ofrecer crearlo o anotarlo (ver «Cómo responder»), pero nunca lo hagas sin que el usuario lo pida.
- **No cambia nada:** ni notas, ni registros, ni la Bitácora.
- **Canon y borrador:** di de qué nota sale cada cosa y si esa nota es canon o borrador. Si la respuesta se apoya en borradores, avísalo en una línea: todavía pueden cambiar.
- **Lo que se cree y lo que es:** las notas cuentan lo que se sabe o se cree en el mundo. Atribúyelo («según los pescadores…», «se dice que…»), y los rumores van como rumores.
- **Los secretos:** el usuario es el autor y puede saber la verdad, pero esta va aparte, al final y marcada 🔒. Si pide la respuesta «sin spoilers», «como jugador», «lo que sabe un habitante» o para enseñarla a otros, usa `--no-secrets` en todas las consultas y no digas que hay secretos.
- **Contradicciones:** si dos notas no coinciden, dilo, y di cuál es canon. Manda la canon más reciente, según la Guía de Canon.
- **Lo pendiente:** algo que se nombra y aún no tiene nota se responde con lo que dicen de ello las notas que lo nombran, avisando de que no tiene nota.
- **En el chat,** los enlaces van en Markdown con la ruta del archivo, tal como los dan los scripts; nunca `[[...]]`.

## Qué consulta responde cada pregunta
Las consultas son de esta skill (`<directorio de esta skill>/scripts/query_world.py`) y de `crear-entidad` (`<crear-entidad>/scripts/`):

| Pregunta | Consulta |
|---|---|
| ¿Qué es? ¿Quién es? ¿Dónde está? ¿Con quién se relaciona? | `query_world.py --about <Nombre>` |
| Un detalle (su historia, su gobierno, qué enseña) | `query_world.py --section <Nombre> <Sección>` (las secciones las dan `--about` y `--outline`) |
| ¿Qué hay en un lugar? ¿Quién vive o manda allí? | `query_world.py --in <Lugar>` |
| ¿Qué pasó antes o después? ¿Qué hubo entre dos años? | `query_world.py --timeline [--from AÑO] [--to AÑO] [--type evento]` |
| ¿Cuánto se tarda de un sitio a otro? ¿Cómo se llega? | `routes.py <A> <B>`, o `routes.py <Lugar>`: sus rutas y lo más cercano |
| ¿Hay algo sobre un tema? ¿Existe algo que se llame así? | `search_vault.py "<texto>"`: entidades, enlaces pendientes, Glosario y preguntas |
| ¿Qué significa un término? | `search_vault.py "<término>" --in glosario` |
| ¿Cuántos hay? ¿Qué falta? ¿Qué es lo más nombrado sin nota? | `world_stats.py --print` y `search_vault.py --type <tipo>` |
| ¿Qué hay en el mapa de un lugar? | `map_key.py <Lugar>` |
| ¿Qué está por decidir? | `search_vault.py "<tema>" --in preguntas` |

Los nombres valen como nombre de archivo, como título o como alias. Si una consulta no encuentra algo, prueba con `search_vault.py`, que mira también los resúmenes y los nombres parecidos.

## Cómo responder
1. Elige la consulta, o las dos o tres que hagan falta. No leas notas enteras: para un detalle, `--section`.
2. Responde primero, en pocas líneas y con la voz de la Ficha. Después:
   - **Fuentes:** cada nota con su enlace y su estado. Lo que no tiene nota, en texto.
   - **🔒 La verdad (solo para ti):** si un secreto cambia la respuesta, salvo que se haya pedido sin spoilers.
3. Si no consta, dilo y ofrece, sin hacerlo:
   - crearlo, o profundizar la nota que debería contarlo (`/crear-entidad`);
   - anotar la duda en Preguntas Abiertas (`add_entries.py --question`).

## Ejemplos
- «¿Quién gobierna Puerto Gris?»: `--about Puerto_Gris` da su `gobierno` y su `gobernante`; si son enlaces pendientes, el `--about` de cada uno dice lo que se sabe de ellos.
- «¿Qué hay en el valle?»: `--in <Valle>`.
- «¿Qué pasó antes de la guerra?»: `--timeline --to <año de la guerra>`.
- «¿Cuánto se tarda del puerto a la capital?»: `routes.py Puerto_Gris <Capital>`.
- «¿Qué sabe un pescador del puerto sobre el culto?»: `--about <Culto> --no-secrets`, y se responde con lo que se dice, no con la verdad.
