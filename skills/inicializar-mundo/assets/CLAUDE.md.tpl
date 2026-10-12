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
- No crees, renombres ni muevas carpetas sin que se pida. Las skills que añadan estructura la registran en la Guía de Organización.

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
- Enlaces con `[[...]]`: toda entidad que una nota nombra (persona, lugar, facción, hecho, fe, obra…) se enlaza cada vez que se nombra (también con su nombre corto), a su nota o, si aún no existe, como enlace pendiente con su tipo (el registro está en `00_Sistema/Enlaces_Pendientes.md`). Lo que es una entidad se enlaza aunque esté dentro de otra o sea un colectivo; solo los términos (rangos, títulos, oficios…) van al Glosario sin enlace. Los secretos no se enlazan.

## Flujo de trabajo
1. Antes de crear, busca duplicados en la bóveda y en el Glosario.
2. Toda nota nace como `borrador`; solo el usuario la promueve a `canon`.
3. Registra los términos nuevos en el Glosario y los cambios de canon en el Registro de Canon.
4. Nunca borres ni sobrescribas notas: lo obsoleto se mueve a `03_Archivados`.
5. Si una petición contradice la Ficha o una nota `canon`, avisa antes de escribir.
6. Lo no decidido va a `Preguntas_Abiertas`; no decidas tú los pilares por definir.
7. Al terminar de generar, da siempre un informe claro: lo creado y lo modificado (con enlaces que se abran), lo que inventaste, lo que queda por confirmar y los enlaces pendientes.

## Código y scripts
- Los scripts (de las skills o del proyecto) se escriben en inglés: nombres de archivo, funciones, variables y opciones de línea de comandos (`find_gaps.py --note`).
- Los comentarios, las docstrings y todo mensaje para el usuario (salidas, ayudas, errores) van en español.

## Verdad y creencia
- Las notas de lore cuentan lo que se sabe o se cree. La verdad oculta va en `80_Secretos`.
- Las notas de lore nunca enlazan a secretos; los secretos enlazan a lo que afectan.

## Reglas de contenido
Derivadas de la entrevista inicial. Si cambia un pilar en la Ficha, actualiza también esta lista.

{{REGLAS}}{{POR_DEFINIR}}
