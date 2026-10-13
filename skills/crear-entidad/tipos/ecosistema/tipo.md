# Tipo: ecosistema

Los biomas y ecosistemas del mundo: bosques, selvas, praderas, desiertos, tundras, montañas, humedales, ríos y lagos, mares, costas, mundos subterráneos y ecosistemas artificiales (los campos de cultivo, las ciudades, los jardines de una nave), corrientes o extraordinarios. La ficha dice cómo es, qué vive en él y quién come a quién, qué lo sostiene, cómo se vive en él, qué peligros tiene, qué lo amenaza y cómo cambia, y su historia.

**No es un ecosistema:**
- un sitio concreto (`lugar`) ni un territorio (`region`): el Bosque Negro es un lugar; el bosque de niebla, el ecosistema que se da en él y en otros sitios. El ecosistema los enlaza en `zonas`, y ellos lo tienen en sus `ecosistemas`;
- una planta (`flora`) o un animal (`criatura`): son sus habitantes, que lo tienen en su `habitat`;
- una fuerza extraordinaria (`fenomeno`): la niebla que muta lo que toca es un fenómeno; el ecosistema que nace de ella, un ecosistema que lo enlaza en `fenomenos`;
- un clima: el clima es uno de sus datos.

## Identidad del tipo
- **Emoji del tipo:** 🌲, al inicio del H1: `# 🌲 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según lo que es (🌳 bosque, 🌴 selva, 🌾 pradera, 🏜️ desierto, ❄️ tundra, ⛰️ montaña, 🪷 humedal, 🏞️ río o lago, 🌊 mar, 🏖️ costa, 🕳️ subterráneo, 🏙️ artificial…).
- **Carpeta:** fija, `50_Naturaleza/Ecosistemas`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Ecosistema.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, escalas, valores permitidos, recíprocas y relaciones). Es de la familia `lugar`, pero no contiene a otros lugares (`contenedor: false`): no es el foco del mundo ni la región de nadie, y no lleva mapa. Su `completa` dice qué enlaces pendientes de otras fichas puede crear: el hábitat de una criatura o de una planta, la zona que afecta un fenómeno o donde se da una afección, y el yacimiento de un material, cuando las notas que lo nombran describen un tipo de tierra que se repite («las turberas», «el bosque de niebla») y no un sitio concreto.

**Hechos importantes:** el prado de una comarca o el humedal de un río son detalles que Claude puede inventar según la autonomía de la Ficha. Son importantes, y van como `Confirmar: …` en Preguntas Abiertas con el ecosistema como primer enlace de la línea:
- un ecosistema extraordinario (`naturaleza: sobrenatural`) o nacido del conflicto central;
- el que cubre una región entera o el mundo (`alcance` continental o mundial);
- el que se muere, o se extiende, y con él cambia la vida de un pueblo.

Si el usuario pide el ecosistema, el pedido es la aprobación.

## Un sistema vivo (lo más importante)
- **Está vivo y conectado:** sus plantas (`flora`) y sus criaturas (`criaturas`) se comen, se esconden, se necesitan. La ficha cuenta **quién come a quién** y **qué lo sostiene** (el agua, una planta, una criatura, el fenómeno que lo mantiene): su pieza clave, la que si cae, cae todo.
- **Se da en algún sitio:** sus `zonas` (las regiones y los lugares donde aparece) son entidades, y su clima y su terreno encajan con ellos.
- **Se vive en él, o no:** quién lo habita (pueblos, asentamientos), qué da (sus `recursos`: madera, caza, agua, turba) y qué cuesta vivir allí.
- **Cambia:** nada está quieto. Lo que lo amenaza (la tala, la sequía, el conflicto central), cómo está cambiando y hacia dónde.
- **Lo extraordinario tiene reglas:** si se da por un poder o un fenómeno (un bosque que respira, una tierra que muta), lo dicen sus `fenomenos` y sus sistemas, con sus límites. En un mundo sin poderes, no los tiene.

## Categoría, naturaleza, alcance, situación y peligro
- `categoria`: `bosque`, `selva`, `pradera`, `desierto`, `tundra`, `montana`, `humedal`, `agua_dulce` (ríos y lagos), `marino`, `costero`, `subterraneo`, `artificial` (lo hizo la gente: campos, ciudades, jardines, el interior de una nave) u `otro`.
- `naturaleza`: `natural`, `sobrenatural` (existe por un poder o un fenómeno extraordinario), `artificial` o `desconocida`.
- `alcance`: `local`, `regional`, `continental` o `mundial`: cuánto se extiende.
- `situacion`:
  - `estable`: sigue como siempre;
  - `en_expansion`: gana terreno;
  - `en_retroceso`: pierde terreno;
  - `amenazado`: algo concreto lo pone en peligro;
  - `devastado`: queda lo que queda;
  - `desaparecido`: ya no existe; se sabe de él por relatos, restos o textos (en `fuentes`).
- `peligrosidad`, del 1 al 5: cuánto le cuesta a la gente vivir o cruzar por él. 1, se vive sin miedo; 3, nadie entra sin saber; 5, no se sale.
- `clima`: texto breve («frío y húmedo, nieblas casi a diario»).

## Nombre
- Como lo llaman quienes lo conocen, en la lengua común: «el bosque de niebla», «las turberas rojas», «el mar de hierba». Con `generate_names.py` si el nombre lleva una palabra inventada.
- Los nombres de otros pueblos o de los sabios van en `aliases`.
- Se enlaza cada vez que una nota lo nombra. Archivo en ASCII (`Turberas_Rojas.md`); H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, dónde se da y por qué importa.
- **Datos clave:** la tabla completa. «Dónde se da», sus zonas enlazadas; «Extensión», con su alcance y una medida del mundo; «Peligro», con su número y lo que significa aquí.
- **Cómo es:** lo que se ve, se oye y se huele al llegar; el terreno y el agua; las estaciones; el día y la noche.
- **La vida:** sus plantas y sus criaturas (las que tienen nota, enlazadas y en `flora` y `criaturas`); quién come a quién, en pocas líneas; lo que lo sostiene, su pieza clave.
- **Cómo se vive en él:** quién lo habita (pueblos y asentamientos, enlazados), lo que da (sus recursos, enlazados y en `recursos`) y lo que cuesta vivir allí.
- **Peligros:** los del terreno y el clima, y los de lo que vive en él (las criaturas, las plantas, las afecciones que da, enlazadas y en `afecciones`).
- **Equilibrio y cambios:** lo que lo amenaza, cómo está cambiando y qué pasaría si cae su pieza clave.
- **Historia:** cómo nació (siempre estuvo, lo trajo un cambio del clima, lo hizo alguien, lo creó el conflicto); de 2 a 4 momentos decisivos; y el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas, de quien vive en él, de quien lo cruza o de quien lo estudia.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para un paisaje del bioma: su terreno, su vegetación, su agua, la luz y el tiempo que hace, y una o dos de sus criaturas, pequeñas.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `naturaleza`, `alcance`, `situacion`, `peligrosidad` y `clima`: ver arriba.
- Relaciones, solo con enlaces:
  - `zonas`: las regiones y los lugares donde se da: cada uno lo tiene en sus `ecosistemas`;
  - `flora` y `criaturas` que viven en él: cada una lo tiene en su `habitat`;
  - `recursos`: los materiales que da (la madera, la turba, la caza, el agua): cada uno lo tiene en sus `yacimientos`;
  - `pueblos` que viven en él o de él;
  - `fenomenos` que lo crean, lo sostienen o lo amenazan: cada uno lo tiene en sus `zonas_afectadas`;
  - `afecciones` que se dan en él;
  - `relacionados`: otros ecosistemas con los que linda o de los que depende (el humedal que alimenta el delta); recíproca;
  - `era` en que nació o cambió.
- `fuentes`: los textos o relatos de donde se sabe (imprescindible en uno desaparecido).
- `relevancia`: 5 el ecosistema del que depende el mundo o que nace de su conflicto central; 4 el que cubre una región o la define; 3 el conocido en su comarca; 2 uno local; 1 uno pequeño.
- `ultima_revision` sin comillas.

## Coherencia
- **La geografía:** su clima y su terreno encajan con los de sus zonas, y con sus vecinos (`relacionados`): un desierto no linda con una selva sin una razón.
- **La vida:** sus plantas y sus criaturas que ya existen cuentan dónde viven y qué comen; no lo contradigas. Lo que come cada uno tiene que estar ahí.
- **La Ficha:** el conflicto central se nota en él (lo que lo cambia, lo que nace de él); los poderes, si puede ser extraordinario.
- **Lo que ya existe:** las notas que ya lo nombran (como enlace pendiente: el hábitat de una criatura, la zona de un fenómeno) cuentan cosas de él. Léelas (`build_context.py`) y no las contradigas.
- **Reciprocidad:** sus zonas lo listan en `ecosistemas`; su flora y sus criaturas, en `habitat`; sus recursos, en `yacimientos`; sus fenómenos, en `zonas_afectadas`; sus ecosistemas relacionados, en `relacionados`.
- **Glosario:** registra su nombre (como ecosistema), sus otros nombres y los términos que nacen de él.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 2 y 7 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- una planta o una criatura propias (`flora`, `criaturas`), sobre todo su pieza clave;
- un recurso que da (`recursos`);
- un lugar donde se da (`zonas`);
- el fenómeno que lo crea o lo amenaza (`fenomenos`);
- el pueblo que vive de él (`pueblos`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, el ecosistema guarda un secreto (su pieza clave no es la que todos creen, se está muriendo por dentro, alguien lo cuida a propósito, crece sobre algo enterrado, se comunica). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] Se dice quién come a quién y qué lo sostiene (su pieza clave).
- [ ] Su clima y su terreno encajan con sus zonas, que lo listan en `ecosistemas`.
- [ ] Sus plantas y sus criaturas que ya existen lo tienen en su `habitat`, y lo que cuenta de ellas no las contradice.
- [ ] Lo extraordinario, si lo tiene, sigue las reglas de sus fenómenos y sistemas y los pilares de la Ficha.
- [ ] Si no es un detalle y no lo pidió el usuario, quedó como `Confirmar: …`.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
