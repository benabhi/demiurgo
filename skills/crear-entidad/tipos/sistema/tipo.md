# Tipo: sistema

Las reglas profundas del mundo: los sistemas de poder (la magia que se aprende, los dones con que se nace, los pactos que conceden poder a cambio de algo), las tecnologías y los saberes técnicos, las leyes del universo (la muerte, el alma, el destino, una física propia) y los conceptos con que el mundo se explica a sí mismo. La ficha dice qué es, qué permite y qué no puede hacer nunca, qué cuesta, cómo se aprende y se usa, cómo se manifiesta, quién lo controla, qué cambia en la sociedad y qué se sabe y qué se cree de él.

Es la regla general, y cada ejemplo concreto va en su carpeta natural y enlaza su sistema: un hechicero es un `personaje`; una espada encantada, un `objeto`; una orden que enseña el arte, una `faccion`. Lo dice la Guía de Organización: la regla general va en `70_Sistemas_y_Cosmologia`.

**No es un sistema:**
- una fuerza o una anomalía que actúa sola, sin que nadie la use (`fenomeno`): una tormenta perpetua es un fenómeno; el arte de protegerse de ella o de aprovecharla, un sistema;
- un objeto con poder o una máquina concreta (`objeto`): el objeto enlaza el sistema con el que funciona;
- una fe o una filosofía con fieles (`creencia`): lo que se cree y se practica. Si sus milagros funcionan de verdad, ese poder es un sistema (`pacto`);
- un dios o una entidad (`deidad`), aunque conceda el poder;
- una enfermedad o una mutación (`afeccion`), aunque dé poderes: el mal es la afección; el poder que concede, un sistema (`don`);
- una ley o una costumbre de un pueblo (`costumbre`): las leyes del universo no las dicta nadie;
- un plano o el más allá como lugar (`region`, categoría `plano`), o un cuerpo celeste (`astro`).

## Identidad del tipo
- **Emoji del tipo:** ⚙️, al inicio del H1: `# ⚙️ Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según lo que es (🔮 una magia, 🩸 un don de la sangre, 🤝 un pacto, ⚒️ una técnica, ⚗️ una alquimia, 🧭 una navegación, ⚖️ una ley, 💀 la muerte, 🌀 un concepto…).
- **Carpeta:** según la `categoria`: `magia`, `don` y `pacto` van en `70_Sistemas_y_Cosmologia/Sistemas_de_Poder`; `tecnologia`, en `70_Sistemas_y_Cosmologia/Tecnologia`; `ley`, en `70_Sistemas_y_Cosmologia/Leyes_del_Universo`; `concepto` y `otro`, en `70_Sistemas_y_Cosmologia/Conceptos_Fundamentales`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Sistema.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, valores permitidos y relaciones). El motor puede crear sistemas desde cero; los que no son detalles quedan como `Confirmar`.

**Hechos importantes:** si el usuario pide el sistema, el pedido es la aprobación. Si no (lo crea el motor, o aparece al crear otra entidad), depende de su peso:
- una técnica local, el secreto de un gremio o los ensalmos de una aldea son detalles que Claude puede inventar según la autonomía de la Ficha;
- un sistema de poder, una tecnología que cambia lo que es posible en una región, una ley del universo o un concepto que define el mundo son hechos importantes: van como `Confirmar: …` en Preguntas Abiertas, con el sistema como primer enlace de la línea.

## Los pilares de la Ficha (lo más importante)
La Ficha dice si existen los poderes extraordinarios y hasta dónde llega la técnica. El sistema encaja siempre con eso; si el pedido choca con un pilar, avisa antes de escribir.
- **Poderes extraordinarios** (`magia`, `don`, `pacto`):
  - **No existen:** no hay sistemas de poder. Lo que la gente cree que funciona es una `creencia` o una superstición, y lo que funciona por medios naturales, una `tecnologia`.
  - **Raros y peligrosos:** pocos lo tienen (`difusion: raro` o `escaso`), siempre cobra un precio alto y la gente común lo teme o desconfía de él.
  - **Presentes con reglas:** reglas claras, límites duros y costes concretos. Puede ser escaso o cotidiano, y la ficha dice cuánto.
  - **Por definir:** no lo decidas tú (ver `referencias/pilares.md`). Con el usuario, pregúntale antes de crear un sistema de poder. En el motor no se crea: si es un enlace pendiente, vuelve a ejecutar el selector con `--skip <enlace>`; si es una entidad nueva, elige una categoría que no dependa del pilar.
- **Tecnología** (`tecnologia`): no supera el nivel de la Ficha.
  - En un mundo antiguo o medieval es un saber de su tiempo (una forja, una navegación, una medicina, una arquitectura), sin lo que la Ficha veta (la pólvora, la imprenta, los relojes mecánicos, los conceptos científicos modernos).
  - En uno moderno o futurista, la ficha dice el nivel exacto o los límites de cada avance (el viaje, la energía, la inteligencia artificial).
  - Si el pilar está por definir, se hace lo mismo que con los poderes.
- **Dioses y entidades superiores:** un `pacto` con una entidad respeta su pilar. Si las entidades rara vez intervienen, el poder que conceden es raro, discutido o tiene otra explicación posible.
- **Leyes del universo y conceptos** (`ley`, `concepto`): lo que la Ficha y las notas `canon` dicen del mundo (la muerte, el alma, los dioses, el conflicto central) manda. Lo que dejan abierto queda abierto, como creencias enfrentadas en «Lo que se sabe y lo que se cree». Una ley del universo es casi siempre un hecho importante.

## Cómo funciona (reglas, costes y límites)
Un sistema sin reglas es un comodín que rompe la coherencia del mundo. Toda ficha deja claro:
- **lo que permite**, con su escala (hasta dónde llega el más hábil), y **lo que nunca puede hacer**: al menos dos límites duros;
- **lo que necesita** para funcionar (materiales, palabras, gestos, tiempo, un lugar, un momento) y **lo que lo frena o lo anula**;
- **un coste real** para quien lo usa (el cuerpo, la mente, el tiempo, los materiales, el dinero, los vínculos…), proporcional a lo que da: cuanto más permite, más cuesta;
- **qué pasa cuando falla** y qué deja **el abuso** (sus secuelas; si son una afección con nota, en `afecciones`);
- al menos un **error común** (algo que la gente cree de él y es falso) y algo que **nadie entiende** todavía: un misterio deliberado, no un dato que falta.

Las reglas son concretas y comprobables: «no puede devolver la vida a un muerto» mejor que «tiene límites»; «cada llama que enciende cuesta una noche de fiebre» mejor que «agota». Las manifestaciones y las notas que lo usan las cumplen.

En una ley o un concepto, las mismas secciones se leen así:
- «Reglas y límites»: lo que se cumple siempre, lo que no ocurre nunca y sus excepciones conocidas;
- «Costes y riesgos»: lo que cuesta desafiarla, lo que les pasa a quienes lo intentan y quién lo ha pagado;
- «Uso y aprendizaje»: cómo se conoce, quién la estudia y quién la aprovecha; si nadie la usa, dilo y explica quién la sufre;
- «Manifestaciones»: los casos en que se ve cumplirse, o en que el concepto toma forma (un rito, una ley de los hombres, un refrán).

### La raíz y las ramas
Un mundo con poderes suele tener un **sistema raíz**: las reglas comunes de todo lo extraordinario (de dónde sale el poder, qué no puede hacer nada, qué cuesta siempre). Cada tradición concreta (una escuela, el don de una sangre, los milagros de una fe) es una **rama** (`sistema_padre` y `ramas`), con reglas propias que nunca rompen las de su raíz. Con la técnica pasa lo mismo: la raíz dice lo que es posible en el mundo, y cada saber concreto es una rama.
- Antes de crear un sistema, busca si ya hay raíz (`search_vault.py --type sistema`). Si la hay, el nuevo es una rama o respeta sus reglas.
- Si no la hay: lo que habla del poder (o de la técnica) del mundo en general es la raíz; una tradición concreta enlaza su raíz en `sistema_padre` como enlace pendiente, con nombre propio, para que se cree después.

## Nombre
- Un nombre propio del mundo, no la palabra genérica: «el Arte del Hilo», «el Canto Hondo», «la Ley del Retorno», no «la magia» ni «la muerte». Así se distingue cuándo una nota lo nombra.
- Se enlaza cada vez que una nota lo nombra por su nombre. Las palabras genéricas (magia, hechizo, ingenio, la muerte de alguien) no se enlazan.
- **La fuerza y el arte no se llaman igual:** si el mundo tiene una palabra propia para la fuerza o la materia que se mueve (un aliento, una savia, un éter), esa palabra es un término del Glosario, y el sistema lleva el nombre del arte, el don o el oficio que la mueve («el Arte del Aliento», «la Vía de la Savia»). Si se llamaran igual, cada nota que hablara de la fuerza tendría que enlazar el sistema. `audit_world.py` avisa de un nombre que el Glosario registra como entidad y como término.
- Cada pueblo puede llamarlo a su manera: los otros nombres van en `aliases`. Para un nombre propio, genera candidatos con `generate_names.py` y el perfil de su cultura de origen.
- Archivo en ASCII (`Arte_del_Hilo.md`). H1 con la ortografía real.

## Categoría, alcance y situación
- `categoria`:
  - `magia`: un arte que se aprende y se practica (conjuros, rituales, runas, cantos, una alquimia que obra prodigios);
  - `don`: un poder que no se aprende: se nace con él o aparece en el cuerpo (la sangre, una mutación, una marca, una exposición). Se entrena, pero no se adquiere estudiando;
  - `pacto`: un poder que se recibe de otro a cambio de algo (los milagros de una fe, el trato con una entidad, una bendición o una maldición que da poder);
  - `tecnologia`: un saber técnico de su época (un oficio avanzado, una ingeniería, una medicina, una navegación, una alquimia que obra por medios naturales) o, en un mundo futurista, un avance con sus límites;
  - `ley`: una regla física o metafísica que rige a todos (la muerte y lo que viene después, el alma, el destino, la causalidad, una física propia del mundo);
  - `concepto`: una idea clave con que el mundo se entiende a sí mismo (el honor, la pureza, el equilibrio, la memoria), compartida por varios pueblos y sin fieles ni doctrina propia (eso sería una `creencia`);
  - `otro`.
- `alcance`: `local`, `regional`, `continental`, `mundial` o `cosmico`: dónde funciona o dónde se conoce.
- `difusion`: `raro` (un puñado en todo su alcance), `escaso` (unos pocos en cada comarca), `comun` (muchos lo usan o lo conocen) o `universal` (todos, o todo lo que existe, como una ley del universo).
- `situacion`: `en_auge` (crece: más practicantes, saberes nuevos), `vigente`, `en_declive` (se pierde: menos maestros, saberes olvidados), `legendario` (solo se sabe de él por relatos; quizá nunca existió) o `perdido` (ya nadie sabe usarlo). `check_note.py` comprueba que encaje con sus fechas y el año actual.
- `aparicion` y `desaparicion`: años del eje del calendario de referencia. `aparicion`, si se sabe cuándo apareció o se descubrió; `desaparicion`, solo si se perdió. Una ley del universo o un concepto no suelen tenerlas.
- **Si el calendario está por definir,** las fechas quedan vacías y el texto usa fechas relativas. No decidas el calendario: es un pilar (ver `referencias/pilares.md`).

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, qué permite (o qué rige) y qué cuesta.
- **Datos clave:** la tabla completa. «Coste» y «Límite», los principales, en pocas palabras; «Desde cuándo», con el año del calendario o de forma relativa.
- **Qué es:** su naturaleza (qué es en el fondo, según lo que se sabe), de dónde sale su poder o su saber, y cómo se percibe cuando actúa: lo que se ve, se oye, se huele o se siente.
- **Reglas y límites, costes y riesgos:** ver «Cómo funciona».
- **Uso y aprendizaje:**
  - quién puede (todos, los que nacen con él, los elegidos, los que pagan);
  - cómo se aprende (años de aprendizaje, una iniciación, un trato);
  - cómo se usa (gestos, palabras, herramientas, rituales, procedimientos);
  - los grados de dominio: qué puede hacer un aprendiz y qué un maestro.
- **Manifestaciones:** de 3 a 6 filas con las formas concretas en que se usa (técnicas, conjuros, ingenios, remedios), lo que hace cada una y su coste o su límite.
  - Son partes del sistema: van al Glosario como términos (Tipo «técnica»), sin enlace.
  - Un objeto concreto que lo usa es un `objeto` y sí se enlaza.
- **Quién lo controla:** quién lo enseña o lo guarda (con enlace a sus facciones o sus lugares), quién lo regula o lo persigue y quién gana con él.
- **Impacto en la sociedad:**
  - qué cambia en la vida diaria, en el poder y en la economía;
  - cómo se mira a quien lo usa (miedo, respeto, desprecio);
  - qué leyes lo permiten, lo limitan o lo prohíben, y dónde.
- **Lo que se sabe y lo que se cree:** lo comprobado frente a las creencias y teorías de cada pueblo o grupo, y los errores comunes.
- **Origen e historia:**
  - su origen, según lo que se sabe (descubierto, enseñado por alguien, nacido de un hecho o de un fenómeno);
  - de 2 a 5 momentos decisivos, con fechas o relativos (su descubrimiento, una prohibición, un desastre, una reforma);
  - el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas, de maestros, de aprendices, de quien lo teme o de un texto que lo enseña.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para una escena del sistema en uso: quién lo usa y para qué, el efecto que se ve, sus útiles o sus gestos, su precio a la vista, el lugar y la luz. Una ley se muestra cumpliéndose; un concepto, encarnado en una escena (un trato que se sella, un juicio). **Nada gráfico:** el precio se sugiere.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `alcance`, `difusion`, `situacion`, `aparicion` y `desaparicion`: ver arriba.
- Relaciones, solo con enlaces:
  - `practicantes`: quienes lo usan o lo dominan (los notables), que lo tienen en sus `sistemas`;
  - `figuras`: otras personas clave que no lo practican (quien lo descubrió o lo formuló, quien lo prohibió, quien lo estudia desde fuera);
  - `facciones` que lo enseñan, lo guardan, lo regulan o lo persiguen: cada una lo tiene en sus `sistemas`;
  - `objetos` que funcionan con él o lo canalizan: cada uno lo tiene en sus `sistemas`;
  - `creencias` que lo practican (sus milagros), lo veneran o lo condenan: cada una lo tiene en sus `sistemas`;
  - `sistema_padre` y `ramas`: de qué sistema es una rama y qué ramas tiene; recíprocas;
  - `opuestos`: los sistemas que lo contrarrestan o con los que choca; recíproca;
  - `culturas` y `especies` que lo practican o que pueden usarlo;
  - `deidades` que lo conceden o a las que se asocia;
  - `fenomenos` de los que sale su poder, que lo alteran o contra los que sirve;
  - `afecciones` que deja su uso o que lo provocan;
  - `materiales` que necesita o que lo frenan;
  - `lugares` donde se enseña, donde es más fuerte o donde no funciona;
  - `obras` que lo enseñan o lo cuentan;
  - `eventos` que lo marcaron (su descubrimiento, una prohibición, una catástrofe);
  - `era` en que apareció.
- `relevancia`: 5 la raíz de los poderes o de la técnica del mundo, una ley del universo o un concepto que lo define; 4 un sistema regional o una rama mayor; 3 una tradición o un saber de una comarca; 2 una técnica menor; 1 un truco de unos pocos.
- `ultima_revision` sin comillas.

## Coherencia
- **La Ficha:** ver «Los pilares». Si el conflicto central toca lo extraordinario o la técnica (lo provoca, lo alimenta, lo anula), el sistema lo muestra de forma concreta.
- **Lo que ya existe:** las notas que ya lo nombran (como enlace pendiente) o que muestran poderes, ingenios u objetos de su clase cuentan cosas de él. Léelas (`build_context.py`): sus reglas las explican y no las contradicen. Si una nota existente muestra un efecto que rompería las reglas que propones, ajusta las reglas o anótalo en Preguntas Abiertas.
- **Raíz y ramas:** una rama respeta las reglas de su raíz. Dos ramas pueden contradecirse en lo que creen, no en lo que hacen.
- **Reciprocidad:** sus practicantes, sus facciones, sus objetos y sus creencias que ya existen lo listan en sus `sistemas`; su raíz, en sus `ramas`; sus opuestos, en sus `opuestos`.
- **Glosario:** registra su nombre (como sistema), sus otros nombres, sus manifestaciones (como técnica) y los términos que nacen de él (cómo se llama a quien lo practica, sus grados, sus útiles).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 2 y 7 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- quien lo enseña o lo persigue (`facciones`);
- un practicante notable (`practicantes`);
- donde se enseña o donde es más fuerte (`lugares`);
- un objeto que lo canaliza (`objetos`);
- una rama, una escuela o su raíz (`ramas`, `sistema_padre`);
- la afección que deja su abuso (`afecciones`);
- el hecho que lo marcó (`eventos`) o el texto que lo enseña (`obras`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, el sistema guarda un secreto (su poder sale de otro sitio del que se cree; tiene un coste oculto que nadie ha notado; alguien lo creó o lo enseñó a propósito; su primera regla es falsa; cada uso alimenta otra cosa). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza. Un secreto que cambia lo que se sabe del conflicto central es un hecho enorme: además va como `Confirmar: …` en Preguntas Abiertas, enlazando al sistema y no al secreto.

## Comprobaciones antes de escribir
- [ ] La categoría lo lleva a su carpeta.
- [ ] Tiene nombre propio, distinto de la palabra genérica y del nombre de la fuerza que mueve.
- [ ] Encaja con los pilares de la Ficha (poderes, tecnología, entidades superiores); si uno está por definir, no se decide.
- [ ] Tiene lo que permite, al menos dos límites duros, lo que necesita, lo que lo frena, un coste real, qué pasa cuando falla, un error común y un misterio.
- [ ] Si hay raíz, la respeta y la enlaza en `sistema_padre`.
- [ ] Explica, sin contradecirlas, las notas que ya lo nombran.
- [ ] Si no es un detalle y no lo pidió el usuario, quedó como `Confirmar: …`.
- [ ] La situación cuadra con sus fechas y con el año actual.
- [ ] Sus practicantes, sus facciones, sus objetos, sus creencias, su raíz y sus opuestos que ya existen lo listan.
- [ ] Nada gráfico ni gratuito en la ficha ni en la imagen.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
