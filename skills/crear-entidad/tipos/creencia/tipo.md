# Tipo: creencia

Lo que la gente cree y cómo lo vive: religiones, cultos, fes populares y supersticiones, filosofías e ideologías. La ficha dice qué enseña, qué venera, cómo se practica, quién la administra, dónde y cuándo se celebra, qué premia y qué castiga, en qué se ha partido y cómo se lleva con el poder y con las demás fes.

**No es una creencia:**
- la iglesia, la orden o la secta que la administra (`faccion`): la fe es lo que se cree; la organización, quienes la gobiernan;
- un dios o una entidad superior (`deidad`): la creencia es lo que sus fieles dicen de él, no lo que es;
- un mito o una leyenda concretos (`mito`): un relato que la fe cuenta, no la fe;
- una costumbre o una fiesta con su historia propia (`costumbre`, más adelante);
- un pueblo (`cultura`): una cultura tiene creencias, pero no es una.

## Identidad del tipo
- **Emoji del tipo:** 🕯️, al inicio del H1: `# 🕯️ Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (☀️ un culto solar, 🌙 uno nocturno, 💀 uno a los muertos, 🔥 una fe del fuego, 🌿 una fe de la tierra, 🧿 una superstición, 📜 una filosofía, ⚖️ una doctrina moral…).
- **Carpeta:** fija, `30_Sociedad_y_Cultura/Creencias_y_Religiones`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Creencia.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, escalas, valores permitidos y relaciones). El motor puede crear creencias desde cero.

**Hechos importantes:** un culto de aldea, la devoción a un santuario o una superstición de marineros (`alcance: local`) son detalles que Claude puede inventar según la autonomía de la Ficha. Una religión regional o mundial que no está en el canon, o una fe que explica un pilar (el origen del mundo, la naturaleza del conflicto central, la de los dioses), es un hecho importante: va como `Confirmar: …` en Preguntas Abiertas, enlazando su nota.

## Lo que se cree, no lo que es
- **La nota cuenta lo que creen sus fieles,** con su voz y sus certezas. Nunca dice si tienen razón: si sus dioses existen, si sus milagros ocurrieron, qué hay de verdad tras la muerte. Esa verdad, si se decide, va en un secreto (`80_Secretos`) o en la nota de la deidad.
- **Los dioses de la Ficha:** si la Ficha dice cómo son las entidades superiores (reales pero distantes, inexistentes, presentes a diario), la fe encaja con eso. Un prodigio que la fe atribuye a sus dioses es, como manda la Ficha, excepcional y discutido: otros lo explican de otra forma.
- **Los poderes:** si sus sacerdotes hacen algo extraordinario, sigue la regla de poderes de la Ficha, con sus límites y su precio. Ese poder es un sistema (un `pacto`, casi siempre), que se enlaza en `sistemas`. Si no lo hacen, lo que la gente cree que hacen es igual de útil.
- **Sin referencias reales:** ni religiones, ni dioses, ni ritos, ni símbolos, ni nombres de fiestas del mundo real, si la Ficha dice que el mundo es inventado. Que se parezca en algo es inevitable; que se reconozca, no.

## Fechas y situación
- `fundacion` y `extincion`: años del eje del calendario de referencia; `extincion` solo si ya nadie la practica.
- **Si el calendario está por definir,** las fechas quedan vacías y el texto usa fechas relativas. No decidas el calendario: es un pilar (ver `referencias/pilares.md`).
- `situacion`: `en_auge`, `extendida`, `en_declive`, `perseguida` y `oculta` (se practica a escondidas) son fes vivas, sin `extincion`; `extinta`, una que ya nadie practica (sus templos y sus palabras pueden seguir ahí). `check_note.py` comprueba que encaje con el año actual.
- `categoria`: `religion` (una fe organizada, con clero y doctrina), `culto` (la devoción a un ser, un lugar o una fuerza concretos), `fe_popular` (supersticiones y creencias sin clero ni libro), `filosofia` (una doctrina sobre cómo vivir, sin culto), `ideologia` (una creencia sobre cómo debe ser el mundo o quién debe mandar) u `otro`.
- `teologia`: `monoteista`, `politeista`, `dualista` (dos fuerzas enfrentadas), `animista` (espíritus en las cosas y los lugares), `ancestral` (el culto a los muertos) o `no_teista`.
- `alcance`: `mundial`, `regional` o `local`. `fieles`: texto breve («casi toda la costa», «unas pocas familias»). `influencia`: del 1 al 5, el peso de la fe en la vida y en las decisiones de su gente (1, una costumbre que pocos toman en serio; 3, la fe que marca el año y los ritos de una comarca; 5, la que decide quién manda).

## Nombre
- Cómo la conocen sus fieles («la Senda de las Cenizas», «el Culto del Pozo», «los Usos del Faro») y, en `aliases`, cómo la llaman los de fuera y sus enemigos.
- Archivo en ASCII. H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **completa**. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué enseña, quiénes la siguen y por qué importa.
- **Datos clave:** la tabla completa. «Lo venerado», en pocas palabras (un dios, un panteón, los muertos, un principio).
- **Doctrina:** lo que enseña en el centro, y lo que dice del origen del mundo, de la muerte y de por qué existen el mal y la desgracia. Es la respuesta de la fe a lo que más teme su gente. Los relatos que merecen nota propia (cómo empezó el mundo, cómo acabará) van en `mitos`.
- **Lo venerado:** de 1 a 5 líneas, una por dios, espíritu, ancestro o principio, con su dominio y cómo lo imaginan. Un dios con nota propia, con su enlace (en `deidades`).
- **Culto y ritos:** lo que hace un fiel cualquier día, los ritos del nacimiento, el paso a la edad adulta, la unión y la muerte, lo que se ofrece (y si se sacrifica algo) y el rito mayor de la fe.
- **Clero:** de 2 a 5 rangos, del más alto al más bajo, con quién los ocupa y qué hacen; si no tiene clero (una fe popular, una filosofía), una fila que diga quién guarda la tradición.
- **Lugares sagrados:** de 1 a 4, con su enlace y por qué lo son. El principal va en `centro`.
- **Símbolos y textos:** el símbolo (lo que muestra la imagen), los colores, gestos y señales con que se reconoce a los fieles, sus textos sagrados (si los hay y cómo se transmiten, según la técnica de la Ficha: copiados a mano, grabados, recitados de memoria) y su lengua sagrada, si tiene una (en `idiomas`).
- **Festividades:** de 1 a 4 filas. Si existe el calendario de referencia, «Cuándo» usa sus nombres de meses y, si la fiesta ya está entre las suyas, el mismo nombre.
- **Moral:** sus virtudes, sus pecados, sus tabúes y cómo castiga y perdona.
- **Ramas y herejías:** las corrientes que salieron de ella o contra ella, con su enlace (en `ramas`) y en qué se separan. Si no tiene, una línea que diga por qué (es joven, es pequeña, persigue a quien disiente).
- **Relación con el poder:** cómo se lleva con quien gobierna (lo sostiene, lo tolera, lo combate, gobierna ella) y con las demás fes (en `rivales`, las que chocan con ella).
- **Historia:** su fundación (quién, cuándo, por qué), de 2 a 5 momentos decisivos y el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas son la mejor voz de una fe: un rezo, un precepto, una maldición, la burla de un incrédulo.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para su símbolo sagrado: el soporte (un amuleto, un altar tallado, una pintura en un muro, un estandarte, un sello, un tatuaje), la figura del símbolo, los materiales y colores, los elementos que lo acompañan (ofrendas, velas, cuerdas) y el desgaste de la devoción.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `teologia`, `situacion`, `alcance`, `fieles`, `fundacion`, `extincion` e `influencia`: ver arriba.
- Relaciones, solo con enlaces:
  - `deidades`: los dioses o entidades con nota propia (o su enlace pendiente): cada una la tiene en sus `creencias`;
  - `fundador` y `figuras` (profetas, santos, reformadores, herejes célebres): cada uno la tiene en sus `creencias`;
  - `centro` (su templo mayor, su ciudad santa), `lugares_sagrados` y `zonas` donde se practica (regiones o asentamientos): cada uno la tiene en sus `creencias`;
  - `culturas` que la profesan: cada una la tiene en sus `creencias`;
  - `facciones` que la administran o la defienden (su iglesia, sus órdenes): cada una la tiene en sus `creencias`;
  - `objetos` sagrados (reliquias, insignias): cada uno la tiene en sus `creencias`;
  - `fenomenos` que explica o venera: cada uno la tiene en sus `creencias`;
  - `sistemas` que practica (sus milagros, si funcionan), venera o condena: cada uno la tiene en sus `creencias`;
  - `mitos` que cuenta como sagrados o que condena: cada uno la tiene en sus `creencias`;
  - `idiomas`: su lengua sagrada;
  - `creencia_madre` y `ramas`: de qué fe nació y qué ramas o herejías salieron de ella; recíprocas;
  - `rivales`: las fes con que choca; recíproca;
  - `eventos` que la marcaron (su fundación, un cisma, una persecución);
  - `era` en que nació.
- `relevancia`: 5 la fe que define el foco o el mundo; 4 una fe regional; 3 la fe de una comarca o un culto conocido; 2 un culto menor; 1 una superstición de unos pocos.
- `ultima_revision` sin comillas.

## Coherencia
- **La Ficha:** sus dioses, sus prodigios, su técnica y su tono encajan con la Ficha. El conflicto central casi siempre tiene una explicación en la fe (un castigo, una prueba, un enemigo, una mentira de los poderosos), y esa explicación es lo que más la diferencia de las demás.
- **Lo que ya existe:** sus fieles, sus lugares, su clero y las notas que ya la mencionan (como enlace pendiente) deben encajar con lo que dicen. Léelas (`build_context.py`). Si una cultura ya cuenta en qué cree, la fe no la contradice.
- **Reciprocidad:** su fundador, sus figuras, sus lugares, sus zonas, sus culturas, sus facciones, sus objetos, sus fenómenos, sus ramas y sus rivales que ya existen la listan en su propiedad inversa.
- **Glosario:** registra su nombre, sus otros nombres, sus rangos y sus términos propios; sus dioses y sus festividades, con su tipo de entidad.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 3 y 8 nuevos** (los que solo nombra esta nota), de al menos dos tipos. Buenos candidatos:
- quien la fundó (`fundador`);
- una figura notable (`figuras`);
- su templo mayor (`centro`);
- un lugar sagrado (`lugares_sagrados`);
- quien la administra (`facciones`);
- una reliquia (`objetos`);
- una herejía (`ramas`).

El dios principal, si no tiene nota, queda como enlace pendiente en `deidades`, con su nombre (el de la Ficha, si lo nombra). Los dioses menores con nombre también son entidades: van en `deidades`, como enlaces pendientes. Si son muchos, nombra solo los que importan y describe el resto sin nombre propio («los dioses menores de la cosecha»).

## Secretos
Tirada real con `roll_dice.py 1d4`: con 4, la fe guarda un secreto (su fundador no creía en lo que predicó, su texto sagrado fue cambiado, su clero sabe que el dios calla, su rito mayor sirve a otra cosa). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] Cuenta lo que creen sus fieles, no si tienen razón; la verdad, si se decide, va en un secreto.
- [ ] Sus dioses y sus prodigios encajan con la Ficha; tiene su explicación del conflicto central.
- [ ] Una religión regional o mundial que no estaba en el canon quedó como `Confirmar: …`.
- [ ] La situación cuadra con sus fechas y con el año actual.
- [ ] Sus fieles, lugares, facciones, objetos, ramas y rivales que ya existen la listan.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y hay entre 3 y 8 enlaces pendientes nuevos, todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
