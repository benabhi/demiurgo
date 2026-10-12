# Tipo: deidad

Los dioses y las entidades superiores: dioses, semidioses, espíritus mayores, demonios, ancestros divinizados y entidades cósmicas o primordiales. La ficha dice qué gobierna, cómo se la imagina, qué se sabe y qué se cree de ella, qué poderes se le atribuyen, qué quiere, cómo se la venera, cuándo se ha manifestado (si lo ha hecho) y con quién se relaciona.

**No es una deidad:**
- la fe que la venera (`creencia`): la creencia es lo que sus fieles hacen y dicen; la deidad, el ser al que se dirigen;
- una fuerza sin voluntad (`fenomeno`): una tormenta perpetua o un mar que hierve son fenómenos, aunque haya quien los adore;
- un mortal muy poderoso (`personaje`): un hechicero, un rey o un monstruo que casi alcanzó la divinidad sigue siendo un personaje, salvo que el canon diga que la alcanzó.

## Identidad del tipo
- **Emoji del tipo:** ✨, al inicio del H1: `# ✨ Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (☀️ un dios del sol, 🌑 uno de la noche, 💀 uno de la muerte, ⚖️ uno de la justicia, 🌊 uno de las aguas, 🔥 uno del fuego, 👁️ una entidad que observa…).
- **Carpeta:** fija, `20_Personajes/Deidades_y_Entidades`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Deidad.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, valores permitidos y relaciones). Lleva `crear_desde_cero: false`: una deidad nueva es un hecho de canon de primer orden, así que el motor solo crea las que otra nota ya nombra como enlace pendiente (el dios de una fe, el que se manifestó en un evento), nunca una de la nada.

**Hechos importantes:** si el usuario pide la deidad, el pedido es la aprobación. Si no (la crea el motor desde un enlace pendiente, o aparece al crear otra entidad), su existencia y lo que se diga de su naturaleza van como `Confirmar: …` en Preguntas Abiertas, enlazando su nota.

## El pilar de las entidades superiores (lo más importante)
La Ficha dice si existen y cuánto intervienen. La deidad encaja siempre con eso:
- **Existen e intervienen:** sus manifestaciones son visibles y tienen consecuencias concretas; "Lo que se sabe" puede ser mucho.
- **Existen pero distantes:** rara vez actúan; cada manifestación es excepcional y discutida (hay quien la explica de otro modo). "Lo que se sabe" es poco, y casi todo es "Lo que se cree" y "Lo que se discute".
- **Inciertas o inexistentes:** ninguna nota de lore confirma que existan. La ficha describe a la deidad tal como la creen sus fieles; sus "manifestaciones" son lo que la gente interpreta como tales, y siempre hay otra explicación. La verdad, si se decide, va en un secreto.
- **Por definir:** no lo decidas tú (ver `referencias/pilares.md`). La ficha cuenta lo que se cree, sin afirmar ni negar que exista, y la pregunta queda en Preguntas Abiertas.

**Verdad y creencia:** la nota de lore nunca afirma lo que la deidad *es* más allá de lo que se sabe en el mundo. Lo que es de verdad (si existe, si es quien dicen, qué quiere en realidad), si se decide, va en un secreto de `80_Secretos` que la enlaza; la ficha no enlaza al secreto.

## Naturaleza y situación
- `naturaleza`: `dios`, `semidios`, `espiritu` (un espíritu mayor de un lugar, un elemento o una especie), `demonio`, `ancestro` (un antepasado divinizado), `entidad` (cósmica, primordial, ajena a lo humano) u `otro`.
- `situacion`, tal como se la conoce o se la cree: `activa` (se manifiesta), `distante` (no responde), `dormida`, `muerta` (se cree que murió, y su culto puede seguir), `olvidada` (nadie la venera ya) o `desconocida`.
- `dominios`, `titulos` y `simbolo`: texto (`dominios` y `titulos` son listas: «la muerte», «los caminos»; «el Que Espera en el Cruce»).

## Nombre
- Su nombre propio en la lengua de sus fieles más antiguos (con `generate_names.py` y su perfil de nombres, o un nombre que suene a su lengua sagrada) y, en `aliases`, los nombres que le dan otros pueblos. Sus títulos van en `titulos`.
- Archivo en ASCII. H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, qué gobierna y quiénes la veneran o la temen.
- **Datos clave:** la tabla completa. «Fieles»: las fes y los pueblos que la veneran.
- **Cómo se la representa:** su figura tal como la imaginan sus fieles (lo que muestra la imagen), sus atributos (lo que lleva, lo que la acompaña) y cómo la ven otros pueblos, que pueden temerla o despreciarla.
- **Naturaleza:** ver "El pilar". Tres líneas honestas: lo que se sabe, lo que se cree y lo que se discute.
- **Poderes:** lo que se le atribuye, sus límites (también los dioses los tienen, si la Ficha pide reglas claras para los poderes) y lo que pide a cambio a quien la invoca.
- **Voluntad y carácter:** lo que quiere (o lo que sus fieles dicen que quiere), su temperamento y lo que la ofende.
- **Culto:** quiénes la veneran (con enlace a sus fes, en `creencias`), cómo se la invoca y qué se le ofrece.
- **Manifestaciones:** de 1 a 4 filas: cuándo, dónde, qué ocurrió y cómo se interpreta. Con el pilar de "distantes", pocas, antiguas y discutidas; con "inciertas", lo que la gente vio y otra explicación posible. Las que merezcan nota propia, en `manifestaciones` (eventos).
- **Relaciones:** con otras deidades (parientes, aliados, rivales), según quién lo cuente: dos fes pueden contar familias distintas.
- **Mitos:** de 2 a 4 relatos breves en que aparece, en la voz de sus fieles. Los que merezcan nota propia, en `mitos`.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas, de rezos, de sacerdotes o de quien la maldice.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para una figura de cuerpo entero **tal como la imaginan sus fieles**: su forma, sus atributos, sus símbolos, el entorno en que se la pinta y la luz. Es una imagen devota, no un retrato de lo que es.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `naturaleza`, `situacion`, `dominios`, `titulos` y `simbolo`: ver arriba.
- Relaciones, solo con enlaces:
  - `creencias` que la veneran: cada una la tiene en sus `deidades`;
  - `parientes` y `aliados`: otras deidades; recíprocas;
  - `rivales`: las deidades a las que esta se opone, según sus fieles; no se espeja sola: si la rivalidad es mutua, va también en la otra, y si es de un solo lado, solo en esta (ver «Relaciones» en `SKILL.md`);
  - `elegidos`: profetas, santos o avatares que hablan en su nombre;
  - `lugares_sagrados` donde se la venera o donde se manifestó;
  - `manifestaciones`: eventos en que se dice que intervino;
  - `fenomenos` que se le atribuyen, `objetos` sagrados y `criaturas` que la sirven (cada una la tiene en sus `deidades`);
  - `mitos` en que aparece: cada uno la tiene en sus `deidades`.
- `relevancia`: 5 una deidad que explica el mundo o el conflicto central; 4 la deidad principal de una fe importante; 3 una deidad de una fe local; 2 un espíritu menor; 1 una figura casi olvidada.
- `ultima_revision` sin comillas.

## Coherencia
- **La Ficha:** el pilar de las entidades superiores (ver arriba), el de los poderes y el tono. Si la deidad tiene que ver con el conflicto central, lo que la Ficha dice de él manda y lo que deja abierto queda abierto.
- **Sus fes:** lo que dicen de ella las creencias que la veneran es su versión; la ficha la recoge y no la contradice. Si dos fes la cuentan distinto, la ficha cuenta las dos.
- **Mundo inventado:** si la Ficha lo pide, nada de dioses, símbolos, iconografía ni nombres del mundo real con otro nombre.
- **Reciprocidad:** las fes, los parientes y los aliados que ya existen la listan en su propiedad inversa. Los rivales, no. Si una fe ya la nombra en su «Lo venerado» sin enlace, añade el enlace y el vínculo inverso.
- **Glosario:** registra su nombre, sus otros nombres, sus títulos y los términos nuevos.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 2 y 6 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- quien habla en su nombre (`elegidos`);
- su santuario (`lugares_sagrados`);
- su manifestación más famosa (`manifestaciones`);
- un objeto sagrado (`objetos`);
- una deidad rival o pariente (`rivales`, `parientes`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, la deidad guarda un secreto (no es quien dicen sus fieles, murió hace siglos y otro responde en su nombre, nunca existió y alguien lo sabe, quiere lo contrario de lo que se predica). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] Encaja con el pilar de las entidades superiores de la Ficha; si está por definir, no se afirma ni se niega que exista.
- [ ] "Naturaleza" separa lo que se sabe, lo que se cree y lo que se discute; la verdad, si se decide, va en un secreto.
- [ ] Si no la pidió el usuario, quedó como `Confirmar: …`.
- [ ] Las fes, parientes y aliados que ya existen la listan.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
