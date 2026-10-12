# Guía de Nombres — {{MUNDO}}

## Archivos
- Nombre del archivo = título de la nota, con `_` en lugar de espacios: `Torre_del_Alba.md`.
- **Solo caracteres ASCII:** sin tildes ni diéresis (`á`→`a`, `ü`→`u`), `ñ`→`n`, sin apóstrofes, comillas ni signos (`¿ ? ¡ ! : ; / \ # ^ [ ] | * < >`). Ejemplo: `D'rakar` → `Drakar.md`.
- La ortografía real va en el `H1` y en `aliases` del frontmatter.
- **Únicos en toda la bóveda:** si dos entidades comparten nombre, añade un calificador (`Aria_Ciudad`, `Aria_Hechicera`).
- Sin prefijos numéricos ni fechas, salvo que formen parte del nombre.
- Prefijos reservados: `Plantilla_` (plantillas) y `MOC_` (índices).

## Carpetas
- Prefijo numérico de decena solo en las de primer nivel (`10_`, `20_`…).
- `Mayusculas_Iniciales_Con_Guion_Bajo`, sin tildes.

## Nombres dentro del mundo
- Idioma de la bóveda: {{idioma}}
- Sonoridad: {{nombres}}
- Un nombre = una entidad. Antes de crear uno, búscalo en la bóveda y en el [[Glosario]].
- Variantes, apodos y traducciones van en `aliases`.
- Mantén la coherencia fonética dentro de cada cultura o pueblo.
- Registra cada término inventado en el [[Glosario]].

## Enlaces
- Usa wikilinks: `[[Nombre_de_Archivo|texto visible]]` cuando el texto difiera del archivo.
- Enlaza cada mención de una entidad, no solo la primera, también con su nombre corto; no se enlazan los términos ni los secretos.
- Un enlace a una nota que aún no existe es válido: es un enlace pendiente (ver `00_Sistema/Enlaces_Pendientes.md`).

## Scripts
- Nombres de archivo e identificadores en inglés (`find_gaps.py`, `load_relations()`); comentarios y mensajes en español.
