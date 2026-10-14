# Enlaces pendientes (huecos)

Un **enlace pendiente** (o **hueco**) es un enlace a una entidad que todavía no tiene nota. Así crece el mundo: cada nota nombra con su enlace a la gente, los lugares y los hechos que la rodean; los que aún no existen quedan pendientes, y el usuario o el motor (`expandir-mundo`) los va creando. Obsidian los muestra atenuados.

## Qué se enlaza
**Toda entidad que la nota nombra va enlazada cada vez que la nombra,** no solo la primera: a su nota, si existe, o como enlace pendiente, si no. También con su nombre corto: «Aldric» por Aldric Voss, `[[Aldric_Voss|Aldric]]`; «los Varenne» por su casa. Solo quedan sin enlace las menciones de la propia entidad, los títulos de sección y la sección Imagen.

Una referencia con un nombre común («la ciudad», «el viejo», «la tormenta» por la Tormenta Eterna) no es una mención por su nombre y no se enlaza. Un apodo con nombre propio («la Tuerta», «el Barquero») sí.

Una entidad es lo que tiene o podría tener nota propia:
- personas y seres, también en grupo («los nueve jueces», un consejo de ancianos) o conocidos por un apodo («el Barquero», «la Tuerta»): el apodo de una persona concreta es esa persona;
- lugares, también los que están dentro de otro (un cabo, un barrio con nombre, una cueva de una sierra) o se llaman con una palabra común («el Paso», «la Cantera»: el sitio que nombran);
- pueblos, facciones, linajes, fes, dioses, lenguas, eras y hechos;
- objetos únicos, obras, mitos y profecías, costumbres y fiestas, criaturas, afecciones y materiales;
- sistemas: una magia, un don, una técnica, una ley del universo o un concepto con nombre propio («el Arte del Hilo»), no la palabra común («la magia», «la muerte»).

Da igual que esté dentro de otra entidad o que vaya en minúscula: si es una entidad, se enlaza. Un colectivo que actúa como uno («los nueve jueces») puede ser una sola entidad, con el tipo que mejor encaje (una facción, si obraban juntos).

No se enlazan:
- **Los términos:** rangos, títulos, cargos, oficios, expresiones y apodos de grupos, gentilicios, monedas, medidas, meses y días, y las palabras de una lengua. Van al Glosario.
- **Los secretos:** la nota de lore nunca enlaza a uno (ver `secretos.md`).

Lo que se crea a la vez que la nota (las demás entidades de un paquete) no queda pendiente: se enlaza a su nota.

**Una entidad menor no lleva nombre propio:** «un herrero del puerto», «su madre, tejedora de redes». Si no merece nota, no la nombres y no hará falta enlazarla. Ponles nombre y enlace solo a las que importan.

**Lo que sostiene el conflicto o un gancho importa:** si una persona, un lugar o un objeto mueve la historia de la nota (aparece en su conflicto, en su sucesión, en sus ganchos), merece nota. Enlázalo con su nombre o, si aún no lo tiene, con un nombre de rol (`[[Socio_de_Aldric_Voss|su socio]]`).

**En el Glosario, el Tipo dice qué es:** el tipo de entidad (lugar, costumbre, personaje…) si es una entidad, o la clase de término (rango, título, oficio, expresión…) si es un término. Registrar una entidad en el Glosario no la libra de llevar enlace.

Los scripts lo comprueban:
- `check_note.py` avisa de las menciones sin enlace: los nombres propios desconocidos, las entidades del Glosario (aunque vayan en minúscula) y las entidades que la nota ya enlaza en otra parte (también con el nombre corto). Enlázalas o, si en realidad son términos, regístralas (o corrige su Tipo) en el Glosario.
- `audit_world.py` avisa de las entidades del Glosario que ninguna nota enlaza.

## Cómo se escribe
- **Nombre del enlace:** el nombre real de la entidad, en ASCII según la Guía de Nombres y con su texto legible: `[[Aldric_Voss|Aldric Voss]]`. Quien la cree usará ese nombre.
  - Los nombres nuevos se generan como los demás (`generate_names.py`, con el perfil de su cultura).
  - Si la entidad merece nota pero el texto no la nombra, porque aún no tiene nombre o no se sabe (su madre, el señor de un castillo), usa un **nombre de rol** `<Rol>_de_<Entidad>`: `[[Madre_de_Aldric_Voss|su madre]]`. Quien la cree le pondrá nombre y reemplazará el enlace.
- **Tipo:** todo enlace pendiente necesita el tipo de entidad que será, para saber con qué módulo crearlo.
  - Si va en una **propiedad de relación** (`padres`, `facciones`, `lugares_notables`…), la propiedad le da el tipo (ver el `modulo.json`). Es la forma preferida: pon cada entidad en su propiedad cuando la hay y, en el cuerpo, en la sección que da el contexto. Si la propiedad da una familia con varios módulos posibles (`lugar`: un asentamiento, un lugar o una región), concreta cuál con `--set` (`--set Puerto_Viejo=asentamiento`).
  - Si solo aparece en el cuerpo, o en una propiedad que admite cualquier entidad, asígnale el tipo en el registro: `pending_links.py --set <Enlace>=<tipo>`. Usa el tipo del módulo que la creará (`asentamiento`, `lugar` o `region`, no solo «lugar») o un tipo previsto que aún no tiene módulo (`obra`, `costumbre`, `material`…).
- **Pista:** en el cuerpo, una línea de contexto para quien la cree: `[[Madre_de_Aldric_Voss|su madre]] — tejedora de redes; murió cuando él tenía doce años`.
- **Texto legible:** en el cuerpo, todo enlace a un archivo con guiones bajos lleva su texto (`[[Aldric_Voss|Aldric Voss]]`); en las tablas, `[[Nota\|texto]]`. En las propiedades va sin texto.

## Cuántos
- **El rango del módulo** (`huecos_propios` en `modulo.json`) dice cuántos enlaces pendientes **nuevos** puede abrir cada nota: los que solo nombra ella. Es el rango de una nota de relevancia 4 o 5; con relevancia 3 se queda en tres cuartos, con 2 en la mitad y con 1 en un cuarto (`check_note.py --depth <tipo>:<relevancia>` da la cuenta). Los que ya nombraban otras notas no cuentan, porque reutilizarlos es lo mejor que puede pasar.
- **Por encima del máximo,** `check_note.py` da un error: deja sin nombre propio las entidades menos importantes. Por debajo del mínimo, un aviso.
- **El presupuesto:** en `expandir-mundo`, el selector da un rango más estrecho para cada tipo (`enlaces_nuevos`), según cuántos enlaces pendientes hay por entidad. Con muchos, cada nota abre pocos nuevos; con pocos, más.
  - Al crear a mano vale cualquier número dentro del rango.
  - Si el registro muestra más de 1,5 por entidad, quédate cerca del mínimo.
- **Variedad:** de al menos dos tipos distintos, si el rango lo permite.
- **Coherencia:** solo entidades plausibles y coherentes con la Ficha. Nunca una especie nueva si no está permitida, ni un hecho que contradiga el canon. Los hechos importantes nuevos van además como `Confirmar: …` (ver `SKILL.md`).

## Reutilizar antes de crear
Antes de nombrar una entidad nueva, comprueba dos cosas:
1. **Si ya existe:** búscala con `search_vault.py "<nombre>"`, que mira las entidades y el Glosario, también por nombres parecidos. Si existe, enlaza su nota.
2. **Si ya está pendiente:** la misma búsqueda muestra los enlaces pendientes que coinciden (`--in pendientes`, para ver solo esos). Si otra nota ya nombra lo mismo (la capital de la región, el gremio del puerto), usa ese enlace con el mismo nombre. Dos enlaces para la misma cosa acabarían siendo dos entidades duplicadas. Además, cuantas más notas nombran un enlace pendiente, antes lo crea el motor.

## El registro
`00_Sistema/Enlaces_Pendientes.md` lista todos los enlaces pendientes, agrupados por tipo. Es para el usuario: Claude no lo lee entero, sino que busca en él con `search_vault.py`.
- con las notas que los nombran y su primera mención;
- con un resumen de cuántos hay por entidad.

Lo genera `pending_links.py`:
```bash
python <skill>/scripts/pending_links.py                           # regenera el registro
python <skill>/scripts/pending_links.py --set Puerto_Viejo=lugar   # asigna un tipo (repetible)
python <skill>/scripts/pending_links.py --list                    # solo el resumen
```
- Se regenera al terminar cada creación, y los tipos asignados se conservan.
- La primera vez, el registro se enlaza desde `MOC_Inicio`.
- En Obsidian, un clic en un enlace pendiente crea una nota vacía con su nombre y lo anula. `audit_world.py` avisa de las notas vacías.

## Lo de fuera del mundo
Si la Escala de la Ficha es `ciudad` o `region`, el mundo es su foco y todo se crea dentro de él. Lo que una nota nombra fuera (la ciudad vecina, el reino al que pertenece, el continente) se enlaza igual, porque es una entidad, pero con el tipo `fuera`: `pending_links.py --set <Enlace>=fuera`. Ese tipo manda sobre el que le dé una propiedad. Así se ve en el grafo y en el registro, en su propio grupo, y nadie lo crea: el motor lo descarta. Si un día el usuario lo quiere dentro del mundo, se le cambia el tipo.

## Completar un enlace pendiente
1. Lee lo que dicen de él todas las notas que lo nombran (`find_gaps.py --link <Enlace>` o `build_context.py --target <Enlace>`). La entidad debe encajar con todo.
2. Créala con `crear-entidad` en modo `hueco=<Enlace>`:
   - **Con nombre real:** el archivo nuevo se llama **exactamente como el enlace**, así todos los enlaces existentes la encuentran sin tocar nada. El H1 y `aliases` llevan la ortografía real (la del texto del enlace).
   - **Con nombre de rol** (`<Rol>_de_<Entidad>`): ponle nombre y reemplaza el enlace en todas las notas que lo usan con `rename_link.py <Rol_de_Entidad> <Nombre_Real>`, que cambia el frontmatter y el cuerpo y conserva el texto visible (`[[Nombre_Real|su madre]]`).
3. Añade en la nueva entidad el vínculo inverso con las notas que la nombran, en su propiedad si la hay.
4. Regenera el registro con `pending_links.py`.

Un **secreto** también puede nombrar entidades por crear. Al crearlas, lo que diga el secreto es verdad oculta: la nota de lore cuenta solo lo que se sabe o se cree. `build_context.py` y `find_gaps.py` lo marcan con 🔒 y lo ponen aparte: úsalo para no contradecirlo, y como mucho deja en la nota alguna señal o rumor que no lo delate.

## Huecos de dato
Un campo que no se puede rellenar porque depende de un pilar por definir (por ejemplo, el año de nacimiento sin calendario) se escribe "Por definir". Si es importante, se anota en `Preguntas_Abiertas`.

## Detección
`scripts/find_gaps.py` lista los enlaces pendientes:
- primero los que no tienen tipo y después los demás, por tipo;
- en cada uno, la nota y la propiedad o la sección donde aparece.

```bash
python <skill>/scripts/find_gaps.py                             # todos
python <skill>/scripts/find_gaps.py --note Aldric_Voss          # los de una nota
python <skill>/scripts/find_gaps.py --link Madre_de_Aldric_Voss # el contexto de uno
python <skill>/scripts/find_gaps.py --json                      # salida para otros scripts
```
