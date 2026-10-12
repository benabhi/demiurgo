# Tipo: mito

Los relatos que el mundo cuenta y cree, sean ciertos o no: mitos de origen (cómo empezó el mundo, un pueblo, la muerte o una costumbre), leyendas de héroes, monstruos y lugares, profecías, cuentos populares y rumores que ya se cuentan como historia. La ficha cuenta el relato con la voz de quien lo cuenta, sus versiones, qué enseña o justifica, cómo se cuenta, qué huella deja en el mundo y qué se sabe y qué se cree de él. Lo que pasó de verdad, si se decide, va en un secreto.

**No es un mito:**
- un hecho con fecha y testigos (`evento`): el evento ocurrió y el mito se cuenta. Un mito puede nacer de un evento, y entonces se enlazan (`eventos`);
- la fe que lo cuenta (`creencia`): la fe es lo que sus fieles creen y practican; el mito, uno de sus relatos;
- un texto, un poema o un cantar concretos (`obra`): la obra es una versión fijada del relato, y el mito vive en todas sus versiones;
- la fiesta o el rito que lo recuerda (`costumbre`);
- un dios (`deidad`), un héroe (`personaje`) o un monstruo (`criatura`), aunque lo protagonicen: el mito los enlaza;
- la verdad que esconde (`secreto`).

## Identidad del tipo
- **Emoji del tipo:** 📖, al inicio del H1: `# 📖 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según lo que cuenta (🌅 un origen, ⚔️ una hazaña, 🐉 un monstruo, 🔮 una profecía, 🕯️ un cuento de miedo, 🗣️ un rumor, ⛓️ un castigo…).
- **Carpeta:** fija, `40_Historia/Mitos_y_Leyendas`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Mito.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, valores permitidos, `solo_si` y relaciones). El motor puede crear mitos desde cero.

**Hechos importantes:** un mito cuenta lo que se cree, no lo que pasó, así que casi nunca establece hechos.
- Una leyenda local, un cuento o un rumor son detalles que Claude puede inventar según la autonomía de la Ficha.
- Son importantes, y van como `Confirmar: …` en Preguntas Abiertas con el mito como primer enlace de la línea:
  - el mito de origen del mundo o de un pueblo entero;
  - el que explica el conflicto central;
  - una profecía que mueve a una región;
  - un mito que nombra un hecho, un ser o un lugar nuevo de gran peso (una guerra de dioses, una ciudad hundida).
- Si el usuario pide el mito, el pedido es la aprobación.

## Lo que se cuenta, no lo que pasó (lo más importante)
- **La voz del mundo:** «El relato» lo cuenta un narrador del mundo, con su voz, sus certezas, sus exageraciones y sus olvidos: como lo contaría una abuela junto al fuego, un sacerdote en el templo o un cantor en la plaza. Las demás secciones son neutras: dicen quién lo cuenta y qué se sabe, nunca si es cierto.
- **La verdad, aparte:** la nota nunca afirma qué pasó de verdad. Si se decide, va en un secreto (ver «Secretos»). Lo que cualquiera puede comprobar (que el lugar existe, que hubo una guerra) va en «Lo comprobado».
- **El canon manda sobre la nota, no sobre el relato:** un mito puede deformar lo que pasó (exagerar, confundir nombres, invertir culpas, mezclar dos historias). Si contradice un hecho del canon, la nota lo dice en «Lo que se sabe y lo que se cree». El relato puede mentir; la nota, no.
- **Los pilares:** en el relato, los poderes y los dioses pueden hacer más de lo que permiten las reglas del mundo, porque es lo que se cuenta. La nota no lo da por bueno: si choca con un sistema o con el pilar de las entidades superiores, lo señala. Si la Ficha pide un mundo inventado, ningún mito calca uno real (un diluvio universal, el robo del fuego, la caja de los males): puede compartir un motivo universal, no su forma reconocible.
- **Versiones:** un mito que cuentan varios pueblos o grupos tiene al menos dos versiones, y cada una cambia algo por un motivo (quién queda bien, quién tiene la culpa, qué derecho justifica).

## Categoría y situación
- `categoria`:
  - `origen`: cómo empezó algo (el mundo, un pueblo, la muerte, una costumbre, un nombre);
  - `leyenda`: hazañas, caídas, castigos, monstruos y lugares de un pasado incierto;
  - `profecia`: lo que vendrá, anunciado por alguien;
  - `cuento`: un relato popular, una fábula o un cuento para asustar o enseñar a los niños;
  - `rumor`: algo reciente que se repite como cierto hasta volverse relato;
  - `otro`.
- `alcance`: `local`, `regional`, `continental` o `mundial`: dónde se cuenta.
- `situacion`: `vivo` (se cuenta y se cree), `en_declive` (se cuenta, pero ya pocos lo creen), `olvidado` (lo recuerdan unos pocos o un texto viejo) o `prohibido` (contarlo se castiga en alguna parte).
- **Profecías:** dos propiedades solo para `categoria: profecia`. En los demás mitos quedan vacías, y `check_note.py` lo comprueba (regla `solo_si` del módulo):
  - `cumplimiento`, obligatorio en una profecía: `pendiente`, `cumplida` (se da por cumplida; el evento que la cumplió va en `eventos`), `incumplida` o `discutida` (unos dicen que se cumplió y otros no);
  - `plazo`: el año del eje que anuncia, si lo anuncia. Si es vaga («cuando el río corra hacia atrás»), queda vacío. `audit_world.py` avisa de una profecía pendiente cuyo plazo ya pasó.
- `aparicion`: el año del eje en que empezó a contarse, si se sabe (en una profecía, cuando se pronunció). Casi siempre queda vacía: la antigüedad va en el texto («desde antes de los primeros reyes»).
- **Si el calendario está por definir,** las fechas quedan vacías y el texto usa fechas relativas. No decidas el calendario: es un pilar (ver `referencias/pilares.md`).

## Nombre
- El nombre con que se lo conoce en la lengua común: «el Gigante que Bebió el Mar», «la Doncella de las Siete Puertas», «la Profecía de las Tres Lunas». Cada pueblo puede llamarlo a su manera: los otros nombres van en `aliases`.
- Se enlaza cada vez que una nota lo nombra por su nombre. El motivo suelto (un gigante, una inundación) no se enlaza.
- Archivo en ASCII (`Gigante_que_Bebio_el_Mar.md`). H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** de qué trata, quién lo cuenta y por qué importa.
- **Datos clave:** la tabla completa. «Antigüedad», casi siempre relativa. «Cuándo ocurre lo que cuenta», en el tiempo del relato («al principio de todo», «en tiempos de la primera reina») o, en una profecía, cuándo dice que pasará.
- **El relato:** el relato entero, de 3 a 6 párrafos, contado como lo cuenta su pueblo; en una profecía, sus palabras y cómo se pronunció.
  - Toda entidad que nombra va enlazada, también aquí.
  - Las figuras que solo existen en el relato y no merecen nota no llevan nombre propio («el primer pastor», «la madre de todos»).
- **Versiones:** de 1 a 4 filas: quién la cuenta, qué cambia y por qué. Si solo hay una, la fila lo dice.
- **Qué enseña o justifica:** la lección; lo que justifica (un poder, un derecho, un odio, una costumbre, un tabú); y a quién le conviene que se crea.
- **Cómo se cuenta:**
  - quién lo cuenta (narradores, sacerdotes, madres, soldados);
  - cuándo y dónde (junto al fuego, en un rito, en una fiesta);
  - sus imágenes y fórmulas (la frase con que empieza, el estribillo, el gesto con que se acompaña).
- **Su huella en el mundo:** las costumbres y los ritos que lo recuerdan, los lugares ligados a él, los dichos y los nombres que salen de él, y cómo pesa hoy en lo que la gente hace o teme.
- **Lo que se sabe y lo que se cree:** lo comprobado (lo que cualquiera puede ver o probar); quién lo cree y quién no; y lo que se discute (en una profecía, si ya se cumplió).
- **Origen e historia:**
  - cómo nació, según lo que se sabe (de un hecho real, de una fe, de un miedo);
  - cómo ha cambiado: de 2 a 4 momentos, con quién lo cambió y por qué;
  - el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas, de quien lo cuenta, de quien lo cree o de quien se burla de él.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para la escena clave del relato **tal como la imaginan quienes lo cuentan**: el momento, las figuras (sin nombres), el escenario, los símbolos y la luz.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `alcance`, `situacion`, `cumplimiento`, `aparicion` y `plazo`: ver arriba.
- Relaciones, solo con enlaces:
  - `culturas` que lo cuentan (la de origen, primero): cada una lo tiene en sus `mitos`;
  - `creencias` que lo cuentan como sagrado o lo condenan: cada una lo tiene en sus `mitos`;
  - `deidades` que aparecen en él: cada una lo tiene en sus `mitos`;
  - `figuras`: personas que aparecen en él, reales o legendarias;
  - `criaturas`, `lugares` y `objetos` que aparecen en él (el monstruo, la cueva, la espada);
  - `eventos`: los hechos reales que lo inspiraron o, en una profecía, el que la cumplió;
  - `fenomenos` y `sistemas` cuyo origen o funcionamiento explica a su manera;
  - `costumbres` que lo recuerdan y `obras` que lo cuentan;
  - `relacionados`: otros mitos con los que se cruza (el principio y el final de una misma historia, dos versiones enemigas); recíproca;
  - `epoca`: la era en que ocurre lo que cuenta (a menudo, una era legendaria o profetizada);
  - `era`: la era en que empezó a contarse.
- `relevancia`: 5 el mito de origen del mundo o el que explica el conflicto central; 4 un mito de un pueblo entero o de una región; 3 una leyenda de una comarca; 2 un cuento local; 1 un rumor de unos pocos.
- `ultima_revision` sin comillas.

## Coherencia
- **Lo que ya existe:** las notas que ya lo nombran (como enlace pendiente) y las entidades que aparecen en él (sus dioses, sus héroes, sus lugares) cuentan cosas de él. Léelas (`build_context.py`): el relato puede deformar lo que dicen, pero la nota lo señala.
- **Reciprocidad:** sus culturas, sus creencias y sus deidades que ya existen lo listan en sus `mitos`; sus mitos relacionados, en sus `relacionados`.
- **Glosario:** registra su nombre (como mito), sus otros nombres y las palabras o fórmulas que nacen de él (un dicho, un nombre que nadie pone a sus hijos).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 2 y 7 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- el héroe, el villano o el profeta (`figuras`);
- el lugar donde ocurrió, o donde dicen que ocurrió (`lugares`);
- el monstruo o el objeto del relato (`criaturas`, `objetos`);
- el hecho real que lo inspiró, o el que cumplió la profecía (`eventos`);
- la fiesta o el rito que lo recuerda (`costumbres`);
- el cantar o el libro que lo fijó (`obras`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 3 o 4, el mito guarda un secreto: lo que pasó de verdad, quién lo inventó y para qué, qué parte se borró o, en una profecía, quién la amañó o qué dice de verdad. El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza. Un secreto que cambia lo que se sabe del conflicto central es un hecho enorme: además, va como `Confirmar: …` en Preguntas Abiertas, enlazando al mito y no al secreto.

## Comprobaciones antes de escribir
- [ ] «El relato» suena a quien lo cuenta, y las demás secciones son neutras: la nota nunca dice si es cierto.
- [ ] Tiene sus versiones (o dice que solo hay una), lo que enseña o justifica y a quién le conviene.
- [ ] Lo que choca con el canon o con los pilares está señalado en «Lo que se sabe y lo que se cree».
- [ ] Si es una profecía, tiene `cumplimiento`; si no lo es, `cumplimiento` y `plazo` quedan vacíos.
- [ ] No calca un mito del mundo real.
- [ ] Si no es un detalle y no lo pidió el usuario, quedó como `Confirmar: …`.
- [ ] Sus culturas, sus creencias, sus deidades y sus mitos relacionados que ya existen lo listan.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace (también en el relato) y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
