# {{MUNDO}} — Reglas del proyecto

Proyecto de worldbuilding del mundo **{{MUNDO}}**. La bóveda de Obsidian está en `{{BOVEDA}}/`; la raíz del proyecto contiene solo soporte (skills, este archivo, git).

## Idioma de la conversación
**{{idioma}}, siempre.** Respuestas, resúmenes, preguntas, avisos y mensajes de avance mientras trabajas van en ese idioma, aunque las herramientas, los archivos, las skills o los mensajes del sistema estén en otro. No cambies de idioma a mitad de una tarea. (El código de los scripts sigue en inglés: ver "Código y scripts".)

## Ficha del mundo
La identidad y los pilares del mundo están en la Ficha, que se carga a continuación. Es la fuente de verdad: nada la contradice.

@{{BOVEDA}}/00_Sistema/Ficha_del_Mundo.md

## Estructura
- Mapa: `{{BOVEDA}}/00_Sistema/MOC_Inicio.md` y el `README.md` de cada carpeta (qué va y qué no).
- Convenciones: `{{BOVEDA}}/00_Sistema/04_Convenciones/` (Organización, Nombres, Canon, Estilo y Tono, Glosario, Registro de Canon).
- Cada nota vive en una sola carpeta, según qué es; las relaciones se expresan con enlaces.
- Las narraciones (relatos, escenas, crónicas y documentos, con `/narrar`) van en `90_Narrativa`: no son entidades; cuentan el mundo, no lo cambian.
- No crees, renombres ni muevas carpetas sin que se pida. Las skills que añadan estructura la registran en la Guía de Organización.
- Grafo de Obsidian: un color por tipo de entidad (por la etiqueta del tipo en `tags`), los nombres visibles desde lejos y sin las notas del sistema (las flechas, a mano: ensucian); en Marcadores, «Grafo sin secretos» (para enseñar el mundo sin spoilers) y «Grafo completo», que además repone la configuración si se pierde. Lo aplica `graph_colors.py` de `crear-entidad`: vuelve a ejecutarlo si llega un tipo nuevo, sin un grafo abierto en Obsidian (uno abierto guarda el suyo encima).

## Consultar la bóveda sin leerla entera
La bóveda crece sin límite. No la recorras ni leas carpetas enteras, y no leas enteros el Glosario, Preguntas Abiertas, el registro de enlaces pendientes ni la Bitácora. Usa los scripts de la skill `crear-entidad`:
- para buscar algo (entidades, enlaces pendientes, Glosario o preguntas), `search_vault.py "<texto>"`, o `--type <tipo>`;
- para el contexto de una entidad, `build_context.py --target <Nota>`;
- para distancias y caminos entre lugares, `routes.py <A> <B>` (o `routes.py <Lugar>`);
- para saber cuánto hay en el mundo (entidades por tipo, enlaces pendientes, mapas por dibujar), `world_stats.py --print`;
- para añadir al Glosario o a Preguntas Abiertas, `add_entries.py`.

Para responder una pregunta sobre el mundo, `/consultar-mundo` (su `query_world.py`: qué es algo, qué hay en un lugar, la cronología y una sección de una nota).
Para saber cómo está la bóveda (qué está mal, qué se quedó atrás al actualizar las skills y qué pide atención), `/diagnosticar-mundo`.

Lee entera solo la nota que necesites y, de una nota larga, solo la sección que te hace falta.

## Nombres de archivo
1. Título con `_` en lugar de espacios: `Torre_del_Alba.md`.
2. Solo ASCII: sin tildes ni diéresis, `ñ`→`n`, sin apóstrofes, comillas ni signos.
3. La ortografía real va en el `H1` y en `aliases`.
4. Nombres únicos en toda la bóveda; ante un choque, añade un calificador (`Aria_Ciudad`).
5. Prefijos reservados: `Plantilla_` y `MOC_`.

## Notas
- Frontmatter base obligatorio: `tipo`, `estado`, `aliases`, `tags`, `relevancia` (de 1 a 5, ver la Guía de Organización) y `ultima_revision` (`origen` es opcional). Si existe una plantilla del tipo en `00_Sistema/01_Plantillas/`, úsala.
- Usa solo tipos de la tabla "Tipos registrados" de la Guía de Organización.
- Propiedades en `snake_case` sin tildes; tags en minúsculas sin tildes.
- `ultima_revision` es la fecha real (`AAAA-MM-DD`). Las fechas del mundo se guardan como número de años en el eje del calendario de la Ficha (negativas antes del año 0); en el texto se escriben con el formato de la Ficha y, si existe un calendario de referencia (tipo `calendario`), con los nombres de sus meses («15 de Siega de 412 UE»).
- Las notas describen el mundo en su presente; el pasado va en su sección de historia.
- La relevancia decide cuánto desarrollo lleva la nota: el frontmatter va siempre completo, pero las secciones de profundidad (ganchos, citas, secretos…) solo desde cierta relevancia (`check_note.py --depth`). No inventes para llenar.
- Las relaciones no son espejos: si A teme a B, la nota de B cuenta la relación desde B (o no la cuenta). Solo se espejan las bilaterales por naturaleza (parentesco, vecindad, pertenencia, un pacto).
- Enlaces con `[[...]]`: toda entidad que una nota nombra (persona, lugar, facción, hecho, fe, obra…) se enlaza cada vez que se nombra (también con su nombre corto), a su nota o, si aún no existe, como enlace pendiente con su tipo (el registro está en `00_Sistema/Enlaces_Pendientes.md`). Lo que es una entidad se enlaza aunque esté dentro de otra o sea un colectivo; solo los términos (rangos, títulos, oficios…) van al Glosario sin enlace. Los secretos no se enlazan.

## Flujo de trabajo
1. Antes de crear, busca duplicados en la bóveda y en el Glosario (con `search_vault.py`).
2. Toda nota nace como `borrador`; solo el usuario la promueve a `canon`, por tandas, con `/revisar-mundo`.
3. Registra los términos nuevos en el Glosario y los cambios de canon en el Registro de Canon.
4. Nunca borres ni sobrescribas notas: lo obsoleto se mueve a `03_Archivados` (lo hace `/revisar-mundo`, con sus imágenes, que van a `02_Activos/Anteriores`).
5. Si una petición contradice la Ficha o una nota `canon`, avisa antes de escribir.
6. Lo no decidido va a `Preguntas_Abiertas`; no decidas tú los pilares por definir.
7. Al terminar de generar, da siempre un informe claro: lo creado y lo modificado (con enlaces que se abran), lo que inventaste, lo que queda por confirmar y los enlaces pendientes. En el chat, los enlaces van en Markdown con la ruta del archivo (`[Nombre]({{BOVEDA}}/<carpeta>/Nota.md)`), que se abren con un clic; nunca `[[...]]`, que solo funciona dentro de Obsidian. Lo que aún no tiene nota (un enlace pendiente) va en texto. Y deja constancia en la Bitácora (`00_Sistema/Bitacora.md`): las skills la escriben solas con `report.py --log`; un cambio suelto que pida el usuario fuera de las skills se anota con `log_entry.py` de `crear-entidad`.
8. El estado del mundo está en la Ficha (`estado_mundo`): en cierre (`/finalizar-mundo`), solo se cierran cabos y ninguna nota abre enlaces pendientes nuevos; cerrado, no se crea nada (sí se puede consultar, narrar e ilustrar).

## Código y scripts
- Los scripts (de las skills o del proyecto) se escriben en inglés: nombres de archivo, funciones, variables y opciones de línea de comandos (`find_gaps.py --note`).
- Los comentarios, las docstrings y todo mensaje para el usuario (salidas, ayudas, errores) van en español.

## Verdad y creencia
- Las notas de lore cuentan lo que se sabe o se cree. La verdad oculta va en `80_Secretos`.
- Las notas de lore nunca enlazan a secretos; los secretos enlazan a lo que afectan.

## Reglas de contenido
Derivadas de la entrevista inicial. Si cambia un pilar en la Ficha, actualiza también esta lista.

{{REGLAS}}{{POR_DEFINIR}}
