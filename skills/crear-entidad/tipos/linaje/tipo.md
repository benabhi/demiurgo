# Tipo: linaje

Las familias que duran más que sus miembros: dinastías reinantes, casas nobles, clanes, familias notables (de mercaderes, de artesanos, de sacerdotes, de contrabandistas) y estirpes con una sangre especial. La ficha dice de dónde vienen, qué se hereda con el apellido, quién manda y quién heredará, con qué cuentan, con quién se alían o se odian, y si suben o se hunden.

**No es un linaje:**
- un individuo (`personaje`): cada miembro con nota propia es un personaje, que lleva la casa en su `linaje`;
- una organización (`faccion`): el gobierno que dirige una dinastía, la guardia de una casa o la compañía de una familia de mercaderes son facciones; la familia es el linaje;
- un pueblo (`cultura`): un pueblo no es una familia, aunque se diga descendiente de un antepasado común.

## Identidad del tipo
- **Emoji del tipo:** 🌳, al inicio del H1: `# 🌳 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (👑 dinastía, 🛡️ casa noble, 🪓 clan, 💰 familia de mercaderes, ⚒️ familia de artesanos, 🩸 estirpe, 🥀 casa en ruina…).
- **Carpeta:** `30_Sociedad_y_Cultura/Instituciones_y_Linajes`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Linaje.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, escalas, valores permitidos y relaciones). El motor puede crear linajes desde cero.

**Hechos importantes:** una familia notable de una aldea, de un barrio o de un gremio (`alcance: local`) es un detalle que Claude puede inventar según la autonomía de la Ficha. Una dinastía reinante, o una casa regional o mundial que no está en el canon, es un hecho importante: va como `Confirmar: …` en Preguntas Abiertas, enlazando su nota.

## Lo que se hereda (lo más importante)
Un linaje es lo que pasa de padres a hijos: un nombre, unas tierras, una deuda, un rasgo.
- **La herencia:** qué recibe cada generación (tierras, un título, un oficio, un secreto, una enemistad, un don o una maldición en la sangre).
- **La sucesión:** cómo se hereda (primogenitura, elección dentro de la familia, línea materna, el más capaz, el que sobreviva), quién manda ahora (`cabeza`), quién heredará (`heredero`) y quién más aspira. Casi toda casa tiene una disputa por la herencia, abierta o callada.
- **Campos para el motor:** `poder` (del 1 al 5: 1, un apellido respetado en su barrio; 3, tierras y voz en su comarca; 5, la casa que reina o la que decide quién reina) y `rivales` (otras casas).
- **El rumbo:** toda casa sube o se hunde. "Ascenso o decadencia" dice hacia dónde va y qué podría cambiarlo.

## Fechas y situación
- `fundacion` y `extincion`: años del eje del calendario de referencia; `extincion` solo si el linaje se extinguió.
- **Si el calendario está por definir,** las fechas quedan vacías y el texto usa fechas relativas ("hace siete generaciones"). No decidas el calendario: es un pilar (ver `referencias/pilares.md`).
- `situacion`: `en_auge`, `activa`, `en_declive` y `caida` (perdió su poder, pero sigue viva) son casas con descendientes vivos, sin `extincion`; `extinta`, una que ya no los tiene (puede que alguien se diga su heredero). `check_note.py` comprueba que encaje con el año actual.
- `alcance`: `mundial`, `regional` o `local`.

## Nombre
- Cómo se la conoce («la Casa Varenne», «los Hijos de Oren», «el clan del Lobo Blanco») y, en `aliases`, el apellido solo, cómo la llaman sus enemigos y sus nombres antiguos.
- El apellido suena a su cultura: genéralo con `generate_names.py` y el perfil de su pueblo (`--surnames`).
- Archivo en ASCII. H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **completa**. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** quiénes son, de dónde viene su nombre y qué pesan hoy.
- **Datos clave:** la tabla completa; los miembros vivos, aproximados («una veintena», «tres ramas y sus criados»).
- **Origen:** la fundación (quién, cuándo y cómo), de dónde viene su poder (la tierra, una hazaña, un pacto, un oficio, un crimen) y lo que cuentan de su origen (la versión de la familia, sea verdad o no).
- **Árbol familiar:** de 4 a 8 filas, de la generación más antigua a la más joven: el fundador, los antepasados que importan, la cabeza actual, su familia cercana y el heredero. Ver "Personas".
- **Sucesión:** ver arriba.
- **Rasgos y tradiciones:** lo que se dice que se hereda (un rasgo físico, un carácter, un don, una locura), las costumbres de la casa y lo que la familia no perdona.
- **Posesiones y poder:** tierras y propiedades, riqueza y de dónde sale, las reliquias de la familia y su influencia. Coherente con `poder` y con la tecnología de la Ficha. Cada reliquia con historia («la espada del fundador») es un objeto: va enlazada en `objetos`.
- **Símbolos:** el blasón (lo que muestra la imagen), los colores y el lema. Un clan o una familia sin heráldica también tiene su marca: un tótem, un sello, un tatuaje, un grito de guerra.
- **Alianzas y enemistades:** de 2 a 4 filas, con la relación (matrimonio, vasallaje, deuda, enemistad de sangre, guerra abierta) y el porqué.
- **Historia:** de 2 a 5 momentos decisivos (con fechas o relativas) y el presente.
- **Ascenso o decadencia:** hacia dónde va, lo que la amenaza y lo que podría salvarla o hundirla.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para su blasón: el soporte (un escudo pintado, un estandarte, una piedra tallada sobre una puerta, un sello en un anillo, un tótem), la división y el fondo, la figura principal, los colores, los elementos secundarios (cimera, soportes, bordura) y el carácter del diseño (antiguo y gastado, recargado, tosco).
  - "Prompt": lo completa `generar-imagen`.

## Personas
- **Las que merecen nota** van enlazadas: a su nota, si existe, o como enlaces pendientes (con un nombre de rol si aún no lo tienen). Son el fundador, la cabeza y el heredero, en su propiedad, y en `miembros`, quien está en el centro de su conflicto, dentro de la familia o casado con ella (el rival por la herencia, quien guarda el testamento). Los demás parientes, sin nombre propio («dos hijas casadas fuera», «un primo en la guardia»).
- **Nombres:** con `generate_names.py` y el perfil de su cultura; el apellido es el de la casa.
- **Reciprocidad:** cada miembro enlazado la lleva en su `linaje`. Si la persona ya existe, añádele el linaje.
- **Edades coherentes:** padres mayores que sus hijos, generaciones según la madurez y la longevidad de su especie, y nadie vivo con más edad de la que permite. El auditor lo revisa en los personajes que ya existen.

## Frontmatter
- `categoria`: `dinastia` (casas reinantes), `casa_noble`, `clan` (clanes y tribus que se organizan por parentesco), `familia` (familias notables sin título: mercaderes, artesanos, sacerdotes, contrabandistas), `estirpe` (una sangre con un don, una maldición o un antepasado extraordinario) u `otro`.
- `situacion`, `alcance`, `fundacion`, `extincion` y `poder`: ver arriba. `lema` y `miembros_vivos`: texto breve.
- Relaciones, solo con enlaces:
  - `fundador`, `cabeza`, `heredero` y `miembros` (los que merecen nota): cada uno la tiene en su `linaje`;
  - `sede` (su castillo, su casa solariega, su taller: un lugar o un asentamiento) y `dominios` (las tierras que tiene: regiones o asentamientos);
  - `linaje_madre` y `ramas`: de qué casa se desgajó y qué ramas menores tiene; recíprocas;
  - `aliados` y `rivales`: otras casas; recíprocas. Las facciones aliadas o enemigas van en la tabla y en `facciones`;
  - `facciones` que controla o a las que sirve (el gobierno de una dinastía, la compañía de una familia de mercaderes);
  - `culturas` a las que pertenece, `creencias` que profesa y `objetos` que guarda (reliquias, armas, documentos de la familia);
  - `eventos` en que tomó parte;
  - `era` en que se fundó.
- `relevancia`: 5 la dinastía que reina en el foco o una casa que decide el destino del mundo; 4 una casa regional; 3 una familia que pesa en su ciudad o su comarca; 2 una menor; 1 una familia corriente con algo que contar.
- `ultima_revision` sin comillas.

## Coherencia
- **La Ficha:** su tecnología, sus poderes (según los sistemas de poder) y su papel ante el conflicto central encajan con la Ficha. Un don o una maldición en la sangre es un poder extraordinario: respeta sus reglas.
- **Lo que ya existe:** sus miembros, su sede, sus tierras y las notas que ya la mencionan (como enlace pendiente) deben encajar con lo que dicen. Léelas (`build_context.py`).
- **Sus tierras:** la región o el asentamiento que gobierna no contradice lo que dice su ficha de quién lo controla (`control`, `gobernante`).
- **Reciprocidad:** sus miembros la listan en su `linaje`; sus ramas, aliados y rivales que ya existen, en su propiedad inversa.
- **Glosario:** registra su nombre (como linaje), sus otros nombres, sus títulos y su lema.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 3 y 10 nuevos** (los que solo nombra esta nota), de al menos dos tipos. Buenos candidatos:
- quien la fundó (`fundador`), quien manda (`cabeza`) y quien heredará (`heredero`);
- un miembro que importa (`miembros`): el rival de dentro, la oveja negra, la que se casó fuera;
- su sede (`sede`) o sus tierras (`dominios`);
- una casa aliada o rival (`aliados`, `rivales`), o una rama (`ramas`);
- una reliquia de la familia (`objetos`).

## Secretos
Tirada real con `roll_dice.py 1d4`: con 4, el linaje guarda un secreto (el heredero no es hijo de quien dicen, el fundador no fue quien cuentan, la fortuna salió de un crimen, la sangre lleva algo que no debería). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] Una dinastía, o una casa regional o mundial que no estaba en el canon, quedó como `Confirmar: …`.
- [ ] Tiene una herencia clara, una sucesión (con su disputa) y un rumbo.
- [ ] La situación cuadra con sus fechas y con el año actual; si sigue viva, su cabeza también.
- [ ] Las edades del árbol son coherentes con la especie.
- [ ] Sus miembros enlazados la llevan en su `linaje`; sus ramas, aliados y rivales que ya existen la listan.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y hay entre 3 y 10 enlaces pendientes nuevos, todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
