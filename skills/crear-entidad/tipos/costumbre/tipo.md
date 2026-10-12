# Tipo: costumbre

Lo que un pueblo, una fe o un poder hace, manda o prohíbe: leyes, tradiciones, festividades, ritos de paso, tabúes y normas de trato (la cortesía, la hospitalidad, el luto, la comida). La ficha cuenta en qué consiste, cuándo y dónde se cumple, quién participa, qué significa para quien la sigue, qué pasa si se rompe, cómo se vive, sus variantes, quién la defiende y quién la discute, y de dónde viene.

**No es una costumbre:**
- el pueblo que la sigue (`cultura`) ni la fe que la manda (`creencia`): la costumbre es una de sus prácticas, y los enlaza;
- el poder que dicta una ley (`faccion`): la ley es la norma; la facción, quien la dicta y la hace cumplir;
- el relato que la justifica (`mito`): el mito se cuenta, la costumbre se hace;
- el hecho que recuerda (`evento`): el evento ocurrió una vez; la costumbre lo repite;
- una regla del mundo o de un poder extraordinario (`sistema`): un sistema dice lo que es posible; una costumbre, lo que la gente hace o se prohíbe;
- un objeto del rito (`objeto`), aunque sea su centro: la costumbre lo enlaza.

## Identidad del tipo
- **Emoji del tipo:** 🎉, al inicio del H1: `# 🎉 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según lo que es (⚖️ una ley, 🎊 una fiesta, 🕯️ un rito, 🚫 un tabú, 🤝 una norma de trato, 🍞 una costumbre de mesa, ⚱️ un rito funerario…).
- **Carpeta:** fija, `30_Sociedad_y_Cultura/Leyes_y_Costumbres`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Costumbre.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, escalas, valores permitidos, recíprocas y relaciones). El motor puede crear costumbres desde cero.

**Hechos importantes:** una costumbre local o de una familia, una fiesta de aldea o un tabú de un oficio son detalles que Claude puede inventar según la autonomía de la Ficha. Son importantes, y van como `Confirmar: …` en Preguntas Abiertas con la costumbre como primer enlace de la línea:
- la ley que rige a todo un pueblo o a un estado;
- la gran fiesta o el tabú que define a un pueblo entero;
- una costumbre que responde al conflicto central o que fija un hecho de gran peso (un sacrificio, una purga, un exilio obligado).

Si el usuario pide la costumbre, el pedido es la aprobación.

## Lo que se hace, no por qué funcionaría (lo más importante)
- **La costumbre se describe como se practica:** quién hace qué, cuándo y dónde, paso a paso, con lo que se ve y lo que se siente. Nada de generalidades («una fiesta alegre»): el gesto concreto, la comida, la frase, la prenda.
- **Su sentido es el que le dan quienes la siguen:** «Qué significa» cuenta lo que se cree que asegura o evita (la cosecha, el regreso de los muertos, la buena suerte), nunca si de verdad lo logra. Si lo lograra por una fuerza extraordinaria, eso lo dicen las reglas de su `sistema` o, si es oculto, un secreto.
- **Las normas tienen consecuencias:** en una ley o un tabú, «Normas y castigos» dice qué está obligado o prohibido y qué le pasa a quien lo rompe, y `rigor` mide cuánto se cumple. Una costumbre sin consecuencias no es una ley.
- **Responde al mundo:** una costumbre nace de algo (el clima, el miedo, un hecho, una fe, la escasez) y dice cómo vive su gente frente al conflicto central y frente a los temas de la Ficha.
- **Mundo inventado:** si la Ficha lo pide, ninguna costumbre calca una del mundo real (una fiesta reconocible con otro nombre, un rito conocido): puede compartir un motivo universal (el fuego en el invierno, el luto, el pan compartido), no su forma.

## Categoría, alcance, situación y rigor
- `categoria`:
  - `ley`: la norma de un poder (un gobierno, una facción, una fe), con su castigo;
  - `tradicion`: lo que se hace porque siempre se hizo (la mesa, la vestimenta, la hospitalidad, el oficio);
  - `festividad`: una celebración con su fecha;
  - `rito`: el acto que marca un paso (el nacimiento, la edad adulta, la unión, la muerte, la iniciación, el juramento);
  - `tabu`: lo que no se hace, no se dice o no se toca, por miedo o por respeto;
  - `norma`: el trato que se espera sin ley escrita (la cortesía, el saludo, el luto, la deuda);
  - `otro`.
- `alcance`: `local`, `regional`, `continental` o `mundial`: dónde se sigue.
- `situacion`: `vigente`, `en_declive` (se sigue cada vez menos), `prohibida` (alguien la persigue, aunque se siga a escondidas), `olvidada` (la recuerdan unos pocos o un texto viejo) o `recuperada` (vuelve después de perderse).
- `rigor`, del 1 al 5: cuánto se cumple y qué cuesta no hacerlo. 1, casi nadie la cumple ya; 3, se cumple y quien no lo hace queda mal visto; 5, romperla se paga con la vida, el destierro o la ruina.
- `fecha`: solo en las festividades, y solo si existe el calendario (ver abajo).
- `inicio` y `fin`: el año del eje en que empezó y en que se prohibió o se perdió, si se sabe. Casi siempre quedan vacíos y la antigüedad va en el texto («desde la primera cosecha»). Si el calendario está por definir, quedan vacíos.

## Festividades y calendario
- Una festividad se celebra en una fecha del calendario. Si el mundo tiene un calendario (nota de tipo `calendario`), enlázalo en `calendario` y pon su fecha en `fecha` con sus nombres: «15 de <Mes>», o la regla de una fiesta movible («la primera luna llena de <Mes>»). `world_calendar.py` muestra los meses.
- La fiesta va también en la tabla «Festividades» de ese calendario, con la misma fecha, y en su propiedad `festividades`: si no está, añade su fila y su enlace (`add_relation.py <Calendario> festividades <Costumbre>`). `check_note.py` avisa si no coinciden.
- Si el calendario está por definir, `calendario` y `fecha` quedan vacíos y el texto usa fechas relativas («al empezar el deshielo»). No decidas el calendario: es un pilar (ver `referencias/pilares.md`).
- Un rito de paso o una tradición no llevan `fecha`: su «Cuándo» es el momento de la vida o del año en que se hacen.

## Nombre
- El nombre con que la conocen quienes la siguen, en la lengua común: «la Quema de la Paja», «el Silencio de los Siete Días», «la Ley del Pozo Compartido». Si es una norma sin nombre propio («no se pisa el umbral de un difunto»), la ficha le da uno descriptivo y la nota lo explica.
- Cada pueblo puede llamarla a su manera: los otros nombres van en `aliases`.
- Se enlaza cada vez que una nota la nombra. Archivo en ASCII (`Quema_de_la_Paja.md`); H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, quién la sigue y por qué importa.
- **Datos clave:** la tabla completa. «Rigor», con su número y lo que significa aquí («4: quien no ayuna, no come en la mesa común»).
- **En qué consiste:** paso a paso, de 3 a 6 puntos, con los gestos, las palabras, los objetos y las comidas concretos.
- **Cuándo y dónde:** la fecha o el momento (de la vida, del año, del día) y el lugar donde se cumple.
- **Quién participa:** quién la cumple, quién la dirige o la vigila, y quién queda fuera (y por qué).
- **Qué significa:** lo que se cree que asegura o evita, y lo que dice de quien la sigue (su orgullo, su miedo, su deuda).
- **Normas y castigos:** lo obligado y lo prohibido, y qué pasa si se rompe: el castigo de una ley, la vergüenza de una norma, el miedo de un tabú. En una fiesta, lo que no se puede hacer ese día.
- **Cómo se vive:** lo que se ve, se oye y se huele, y lo que se come, se lleva o se canta.
- **Variantes:** de 1 a 3 filas: dónde o quién la cumple distinto, qué cambia y por qué.
- **Quién la defiende y quién la discute:** quién la sostiene (y qué gana con ella) y quién la critica, la evita o la persigue.
- **Origen e historia:** de dónde viene, según lo que se sabe (un hecho, una fe, una escasez, un miedo, un mito); de 1 a 3 momentos decisivos (cuando se impuso, se prohibió o cambió); y el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas, de quien la cumple, de quien la impone o de quien se burla de ella.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para la costumbre en su momento más reconocible: la fiesta en su punto álgido, el rito en su gesto central, la ley al cumplirse o al castigarse, el tabú en la señal que lo recuerda (la puerta que nadie cruza).
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `alcance`, `situacion`, `rigor`, `fecha`, `inicio` y `fin`: ver arriba.
- Relaciones, solo con enlaces:
  - `pueblos` que la siguen (el de origen, primero): cada uno la tiene en sus `costumbres`;
  - `creencias` que la mandan, la bendicen o la condenan: cada una la tiene en sus `costumbres`;
  - `facciones` que la dictan, la vigilan o la persiguen;
  - `figuras`: quien la impuso, quien la guarda o quien la rompió de forma sonada;
  - `lugares` donde se cumple o se celebra;
  - `calendario` por el que se fija su fecha (solo en una festividad): la tiene en sus `festividades`;
  - `mitos` que la justifican o que se cuentan en ella: cada uno la tiene en sus `costumbres`;
  - `eventos` que recuerda, que la impusieron o que la prohibieron;
  - `objetos` del rito o de la fiesta;
  - `relacionadas`: otras costumbres con las que va de la mano (el ayuno y la fiesta que lo rompe, la ley y el tabú que la sostiene); recíproca;
  - `era` en que nació.
- `relevancia`: 5 la costumbre que define al mundo o que responde a su conflicto central; 4 la de un pueblo entero o una región; 3 la de una comarca, una ciudad o una fe; 2 la de un barrio, un oficio o una familia; 1 la manía de unos pocos.
- `ultima_revision` sin comillas.

## Coherencia
- **Lo que ya existe:** las notas que ya la nombran (como enlace pendiente) y las que la rodean (su pueblo, su fe, su calendario, el mito que la justifica) cuentan cosas de ella. Léelas (`build_context.py`) y no las contradigas: si su pueblo dice que la fiesta es en invierno, es en invierno.
- **La tecnología, los poderes y la escasez del mundo:** lo que se come, se quema o se ofrece existe en el mundo y cuesta lo que cuesta allí.
- **Reciprocidad:** sus pueblos, sus creencias y sus mitos que ya existen la listan en sus `costumbres`; su calendario, en sus `festividades`; sus costumbres relacionadas, en sus `relacionadas`.
- **Glosario:** registra su nombre (como costumbre), sus otros nombres y las palabras que nacen de ella (el nombre de un plato, un saludo, una fórmula).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 1 y 6 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- el pueblo o la fe que la sigue (`pueblos`, `creencias`);
- quien la dictó, la vigila o la persigue (`facciones`, `figuras`);
- el lugar donde se cumple o se celebra (`lugares`);
- el mito que la justifica o el hecho que recuerda (`mitos`, `eventos`);
- el objeto del rito (`objetos`);
- la costumbre que va de la mano con ella (`relacionadas`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, la costumbre guarda un secreto (nació para tapar un crimen, lo que se ofrece no va a donde se cree, quien la impuso no creía en ella, su sentido verdadero es otro). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] «En qué consiste» describe gestos, palabras, objetos y comidas concretos, no generalidades.
- [ ] «Qué significa» cuenta lo que creen quienes la siguen, sin afirmar que funcione.
- [ ] Si es una ley o un tabú, tiene sus consecuencias y su `rigor` cuadra con ellas.
- [ ] Si es una festividad y existe el calendario, tiene `calendario` y `fecha`, y está en su tabla de festividades con la misma fecha.
- [ ] No calca una costumbre del mundo real.
- [ ] Si no es un detalle y no la pidió el usuario, quedó como `Confirmar: …`.
- [ ] Sus pueblos, sus creencias, sus mitos, su calendario y sus costumbres relacionadas que ya existen la listan.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
