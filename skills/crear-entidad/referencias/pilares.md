# Pilares por definir

La Ficha del Mundo puede dejar pilares «Por definir.» (el calendario, las inspiraciones…), que se listan en `CLAUDE.md` y en Preguntas Abiertas. **Un pilar lo decide el usuario, nunca Claude.** Esta referencia dice qué hacer cuando una creación lo necesita; cada módulo dice qué preguntar y qué reglas añade (el calendario, por ejemplo, en su `tipo.md`).

## Cuándo se resuelve
- **Solo con una decisión del usuario:** la que ya trae su pedido, o la que responde a una pregunta (AskUserQuestion, con 2 o 3 opciones concretas sacadas de la Ficha y la recomendada primero).
- **Nunca en el motor** (`expandir-mundo`): allí el pilar sigue por definir, y lo que depende de él espera o se escribe en relativo («hace veinte años»).
- Si el usuario prefiere no decidir todavía, sigue sin el pilar: lo que dependa de él queda vacío o en relativo, y el pilar sigue en Preguntas Abiertas.

## Cómo se resuelve
Con la decisión, actualiza estos cuatro sitios, y nada más de ellos:
1. **La Ficha del Mundo** (`00_Sistema/Ficha_del_Mundo.md`): sustituye «Por definir.» en la línea del pilar por lo decidido, con el mismo estilo que las demás líneas. Si el pilar tiene propiedad en el frontmatter, ponle su valor. Actualiza `ultima_revision`.
2. **`CLAUDE.md`** (en la raíz del proyecto), sección «Reglas de contenido»:
   - añade la regla del pilar, una línea como las demás (el módulo da su texto);
   - quita el pilar de la línea «**Pilares por definir:**»; si no queda ninguno, borra la línea entera.
3. **Preguntas Abiertas:** marca el pilar como resuelto y enlaza dónde se decidió: `- [x] <Pilar> — decidido en [[Nota]]`.
4. **Registro de Canon:** una fila al principio de la tabla: `| <fecha> | [[Ficha_del_Mundo]] | <Pilar>: <lo decidido> | Decisión del usuario al crear [[Nota]] |`.

Valida después la nota creada con `check_note.py` y el mundo con `audit_world.py`: las fechas y edades que ya existían ahora se comparan con el pilar.

## En el informe
Dedica una línea a cada pilar decidido: qué se decidió y los cuatro cambios, con enlaces a la Ficha, a `CLAUDE.md`, a Preguntas Abiertas y al Registro de Canon.
