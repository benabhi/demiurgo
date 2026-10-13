# Tipo: obra

Lo que la gente del mundo escribe, canta, representa, pinta, talla o dibuja: crónicas, tratados, cartas, diarios y libros sagrados; documentos (leyes escritas, tratados de paz, contratos, actas); poemas y cantares; canciones e himnos; obras de teatro, danzas y ritos representados; pinturas, murales y tapices; estatuas y relieves; y mapas antiguos. La ficha dice qué es y cómo se ve o se oye, lo que dice (con un fragmento), quién la hizo y por qué, cómo se recibe, sus ejemplares y versiones, y su historia.

**No es una obra:**
- el ejemplar físico como cosa (`objeto`): la obra es lo que dice o lo que muestra; un ejemplar concreto (el único códice que queda, la tablilla que alguien lleva encima) es un objeto, sobre todo si importa como cosa (quién lo tiene, qué poder guarda). La obra enlaza sus ejemplares en «Ejemplares y versiones»;
- el relato que la gente cuenta de boca en boca (`mito`): el mito es lo que se cree; la obra, una forma fijada de contarlo (el cantar que fijó la leyenda). El mito la enlaza en sus `obras`;
- la costumbre en la que se canta o se representa (`costumbre`): la canción es una obra; la fiesta donde se canta, una costumbre;
- el hecho que cuenta (`evento`) o la persona que retrata (`personaje`): la obra los enlaza en `trata_de`, con su versión de los hechos.

## Identidad del tipo
- **Emoji del tipo:** 🎨, al inicio del H1: `# 🎨 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según lo que es (📜 crónica o documento, 📖 libro, ✒️ poema, 🎵 canción, 🎭 representación, 🖼️ pintura, 🗿 escultura, 🗺️ mapa, ⚖️ ley escrita…).
- **Carpeta:** fija, `30_Sociedad_y_Cultura/Arte_y_Expresion`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Obra.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, valores permitidos, `solo_si`, recíprocas y relaciones). El motor puede crear obras desde cero.

**Hechos importantes:** una canción de taberna, una carta, un cuadro de una casa o un mapa de un mercader son detalles que Claude puede inventar según la autonomía de la Ficha. Son importantes, y van como `Confirmar: …` en Preguntas Abiertas con la obra como primer enlace de la línea:
- el texto sagrado de una fe, la ley escrita que rige a un pueblo o el tratado que cerró una guerra;
- la obra que cuenta una verdad que cambia lo que se sabe del mundo (sobre el conflicto central, sobre un hecho de la historia);
- la obra perdida que lleva a algo de gran peso (una ruta, un lugar, un poder).

Si el usuario pide la obra, el pedido es la aprobación.

## Una obra del mundo (lo más importante)
- **Tiene voz:** la ficha cita un **fragmento** inventado (unos versos, una línea de la crónica, una cláusula del tratado, la descripción de lo que muestra el mural), con la voz de quien la hizo y de su época. Es lo que hace que una obra exista: no la resumas sin dejarla hablar.
- **Cuenta su versión:** una crónica no es la historia, sino lo que alguien quiso contar. Lo que dice puede ser falso, exagerado o interesado, y la ficha lo trata así: lo que dice la obra, lo que se discute de ella y quién gana con ella. Si se decide la verdad, va en un secreto.
- **Alguien la hizo por algo:** por encargo, por fe, por memoria, por venganza, por dinero, por amor. Y alguien la lee, la canta, la mira, la guarda, la copia, la censura o la quema.
- **Es de su mundo:** la técnica de la Ficha decide cómo se hace y se conserva (sin imprenta, cada libro es una copia a mano, y cada copia cambia algo); su lengua es la de quien la hizo (`idiomas`); y el conflicto central se nota en lo que cuenta o en lo que le pasó.
- **Mundo inventado:** si la Ficha lo pide, ninguna obra calca una del mundo real (un poema reconocible, un libro sagrado conocido): puede compartir una forma universal (el cantar de gesta, la crónica, el himno), no su contenido.

## Categoría, autoría, difusión y situación
- `categoria`:
  - `texto`: crónicas, tratados, cartas, diarios, libros de saber o de fe;
  - `documento`: leyes escritas, tratados de paz, contratos, actas, títulos;
  - `poema`: poemas, cantares, epopeyas;
  - `cancion`: canciones, himnos, música;
  - `representacion`: obras de teatro, danzas, ritos que se representan;
  - `pintura`: pinturas, murales, tapices, mosaicos;
  - `escultura`: estatuas, relieves, tallas;
  - `mapa`: mapas, cartas de navegar, itinerarios dibujados;
  - `otro`.
- `autoria`: `conocida`, `atribuida` (se dice que es de alguien, y se discute), `anonima` o `colectiva` (la hizo un pueblo, una orden, generaciones).
- `difusion`: `unica` (un solo ejemplar, o una sola pieza), `rara` (pocas copias, pocos que la conocen), `conocida` o `universal` (la sabe todo el mundo).
- `situacion`:
  - `viva`: se lee, se canta, se representa o se mira hoy;
  - `conservada`: existe, pero casi nadie la conoce (en un archivo, en una cripta);
  - `fragmentaria`: quedan trozos;
  - `perdida`: solo se sabe de ella por otras obras o por relatos (puede que nunca existiera);
  - `prohibida`: alguien la persigue, aunque circule a escondidas;
  - `destruida`: se sabe que la destruyeron (con `destruccion`, si se sabe).

  `check_note.py` comprueba que cuadre con sus fechas y con el año actual.
- `creacion` y `destruccion`: el año del eje en que se hizo y en que se perdió o se destruyó, si se saben. Si el calendario está por definir, quedan vacías y el texto usa fechas relativas.

## Nombre
- El título con que se conoce («El Cantar de las Tres Torres», «la Carta de Sal», «el Mural de los Ahogados»), en la lengua común. Si no tiene título, el que le da la gente por lo que es («la crónica del monje ciego»).
- Los títulos en su lengua original, los de otros pueblos y los apodos van en `aliases`.
- Se enlaza cada vez que una nota la nombra. Archivo en ASCII (`Cantar_de_las_Tres_Torres.md`); H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, de qué trata y por qué importa.
- **Datos clave:** la tabla completa. «Autoría», con su duda si es atribuida; «Dónde está», el lugar o quien la guarda (y en `ubicacion`, si es un sitio).
- **Qué es:** su forma (un libro de cuarenta hojas, un cantar de trescientos versos, un mural de veinte pasos); cómo se ve o cómo suena; cómo se conserva o se transmite (copiada a mano, aprendida de memoria, guardada bajo llave).
- **Lo que dice:** de qué trata (lo que cuenta, enseña o muestra, con sus enlaces y en `trata_de`); **un fragmento** citado (de una a cuatro líneas, con su voz); lo que enseña o defiende.
- **Quién la hizo y por qué:** su autoría (y su disputa); por qué se hizo; para quién.
- **Cómo se recibe:** quién la lee, la canta o la mira hoy; cómo se interpreta (las lecturas enfrentadas); quién la discute, la censura o la persigue.
- **Ejemplares y versiones:** de 1 a 3 entradas: los ejemplares que quedan (si alguno es un objeto con nota, enlazado), sus copias con cambios, sus traducciones o las versiones que se cantan distinto.
- **Historia:** cómo se hizo; de 2 a 4 momentos decisivos (cuando se prohibió, se perdió, se encontró, se copió mal); y el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas son lo que dicen **de** la obra (quien la venera, quien la desprecia), no la obra misma, que va en su fragmento.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para la obra misma (una pintura, un mural, una estatua, un mapa: lo que muestra, su estado y su lugar) o su interpretación (una canción o una obra de teatro: la escena en que se canta o se representa; un texto: el libro abierto con sus ilustraciones, en su sitio). Sin letras ni palabras legibles.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `autoria`, `difusion`, `situacion`, `creacion` y `destruccion`: ver arriba.
- Relaciones, solo con enlaces:
  - `autores`: quien la hizo, si se sabe (o a quien se atribuye, y el texto lo dice): cada uno la tiene en sus `obras`;
  - `pueblos` que la hicieron o la guardan como suya, y `facciones` que la encargaron, la guardan o la persiguen;
  - `creencias` para las que es un texto sagrado o maldito: cada una la tiene en sus `textos`;
  - `idiomas` en que está escrita o se canta: cada uno la tiene en sus `obras`;
  - `mitos` que cuenta o fija: cada uno la tiene en sus `obras`;
  - `sistemas` que enseña o cuenta (un tratado de un poder, un libro de una técnica): cada uno la tiene en sus `obras`;
  - `eventos` que narra o en los que nació, y `costumbres` en las que se canta, se lee o se representa;
  - `trata_de`: de quién o de qué trata (personas, lugares, hechos, criaturas…), de cualquier tipo (sin propiedad que les dé tipo, cada enlace pendiente lo recibe con `pending_links.py --set`);
  - `ubicacion`: dónde está, si está en un sitio (la biblioteca, el templo, la cripta);
  - `relacionadas`: otras obras con las que va de la mano (la respuesta, la continuación, la parodia, la copia enemiga); recíproca;
  - `era` en que se hizo.
- `fuentes`: las otras obras o relatos de donde se sabe de ella (imprescindible en una perdida).
- `relevancia`: 5 la obra que define al mundo o a su conflicto central (el texto sagrado de la fe mayor, el tratado que lo cambió todo); 4 la de un pueblo o una fe entera; 3 la conocida en su comarca o su oficio; 2 una local; 1 una que conocen pocos.
- `ultima_revision` sin comillas.

## Coherencia
- **La Ficha:** la técnica decide cómo se hizo y cuántas copias puede haber; los poderes, si la obra puede tener alguno (un texto que hace algo es también un objeto o la regla de un sistema); el conflicto central se nota en lo que cuenta o en lo que le pasó.
- **Lo que ya existe:** las notas que ya la nombran (como enlace pendiente: la fuente de una ruta perdida, el cantar de un mito, el libro de un sistema) cuentan cosas de ella. Léelas (`build_context.py`) y no las contradigas: si un mito dice que su cantar se perdió, se perdió.
- **Su versión de los hechos:** si cuenta un evento que ya existe, su relato puede diferir del de la nota del evento, y la diferencia se dice («la crónica calla la matanza del puerto»).
- **Reciprocidad:** sus autores la listan en `obras`; sus creencias, en `textos`; sus mitos, sus idiomas y sus sistemas, en `obras`; sus obras relacionadas, en `relacionadas`.
- **Glosario:** registra su título (como obra), sus otros títulos y los términos que nacen de ella (un verso que se volvió dicho, un personaje que se volvió insulto).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 1 y 6 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- quien la hizo (`autores`);
- de quién o de qué trata (`trata_de`);
- quien la guarda o la persigue (`facciones`), o el sitio donde está (`ubicacion`);
- el mito que fija o la fe que la venera (`mitos`, `creencias`);
- la obra que le responde (`relacionadas`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, la obra guarda un secreto (no la escribió quien la firma, una página arrancada decía otra cosa, esconde un mensaje para quien sepa leerlo, lo que cuenta es mentira y alguien lo sabe, la copia que todos leen es falsa). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] Tiene su fragmento, con la voz de quien la hizo y de su época.
- [ ] Cuenta su versión de los hechos como versión, no como la verdad.
- [ ] Se dice quién la hizo (o que no se sabe) y por qué, y quién la lee, la guarda o la persigue.
- [ ] La técnica del mundo cuadra con cómo se hizo y se conserva.
- [ ] No calca una obra del mundo real.
- [ ] Si no es un detalle y no la pidió el usuario, quedó como `Confirmar: …`.
- [ ] Sus autores, sus creencias, sus mitos, sus idiomas, sus sistemas y sus obras relacionadas que ya existen la listan.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
