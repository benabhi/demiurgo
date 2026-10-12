# Tipo: faccion

Los grupos organizados que quieren algo: gobiernos y consejos, gremios, órdenes, sectas, compañías, ejércitos y huestes, bandas, sociedades secretas, movimientos, alianzas e instituciones (academias, archivos, tribunales). La ficha dice quiénes son, qué quieren de verdad, cómo se organizan, cómo se entra, quién manda, con qué cuentan, cómo actúan, qué símbolos usan y con quién se llevan bien o mal.

**No es una facción:**
- un pueblo o una cultura (`cultura`): un pueblo no es una organización, aunque tenga las suyas;
- una fe (`creencia`): la fe es lo que se cree; la iglesia, la orden o la secta que la administra, una facción;
- una casa noble, una dinastía o un clan (`linaje`);
- el territorio que gobierna (`region`): el reino como tierra es una región; su gobierno, una facción.

## Identidad del tipo
- **Emoji del tipo:** 🛡️, al inicio del H1: `# 🛡️ Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (👑 gobierno, ⚖️ consejo o tribunal, ⚒️ gremio, ⚔️ orden o ejército, 🗝️ sociedad secreta, 🗡️ banda, 💰 compañía, 🔥 movimiento, 📚 academia, 🤝 alianza…).
- **Carpeta:** según la `categoria`:
  - `gobierno` (monarquías, repúblicas, imperios, teocracias, federaciones) y `consejo` van en `30_Sociedad_y_Cultura/Gobiernos_y_Estados`;
  - `gremio`, `orden`, `secta`, `compania`, `ejercito` (también huestes y milicias), `banda`, `sociedad_secreta`, `movimiento` (rebeldes, sindicatos, causas), `alianza` y `otro` van en `30_Sociedad_y_Cultura/Facciones_y_Organizaciones`;
  - `institucion` (academias, universidades, archivos, tribunales) va en `30_Sociedad_y_Cultura/Instituciones_y_Linajes`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Faccion.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, escalas, valores permitidos y relaciones). El motor puede crear facciones desde cero.

**Hechos importantes:** una banda, un gremio, una cofradía o un consejo de aldea (`alcance: local`) son detalles que Claude puede inventar según la autonomía de la Ficha. Una facción regional o mundial que no está en el canon (un gobierno, una orden que se extiende por todo el foco, una alianza de pueblos) es un hecho importante: va como `Confirmar: …` en Preguntas Abiertas, enlazando su nota.

## Lo que quiere (lo más importante)
Una facción es lo que quiere y lo que está dispuesta a hacer para conseguirlo.
- **Propósito:** lo que dice buscar y lo que busca de verdad (pueden coincidir o no), su objetivo de ahora y lo que no haría nunca.
- **Campos para el motor:** `objetivo` (una frase: lo que intenta conseguir ahora, concreto y con alguien que se oponga), `recursos` (del 1 al 5: 1, casi nada; 3, lo de un gremio próspero o una orden local; 5, los de un gobierno o una potencia) y `rivales` (quien se le opone). Con ellos, más adelante, el motor podrá hacer que las facciones actúen y choquen.
- **Una grieta:** toda facción tiene una tensión interna (dos líderes, una facción dentro de la facción, un dogma que ya no se cumple). Va en "Estructura", "Métodos" o "Secretos y rumores".

## Fechas y situación
- `fundacion` y `disolucion`: años del eje del calendario de referencia; `disolucion` solo si dejó de existir.
- **Si el calendario está por definir,** las fechas quedan vacías y el texto usa fechas relativas. No decidas el calendario: es un pilar (ver `referencias/pilares.md`).
- `situacion`: `en_auge`, `activa`, `en_declive` y `perseguida` son facciones vivas, sin `disolucion`; `disuelta`, una que ya no existe (puede que alguien siga creyendo que sí). `check_note.py` comprueba que encaje con el año actual.
- `alcance`: `mundial`, `regional` o `local`. `visibilidad`: `publica`, `discreta` (se sabe que existe, no lo que hace) o `secreta`.

## Nombre
- Cómo se la conoce («el Consejo de Barqueros», «la Orden del Umbral», «los Cuervos del Puerto») y, en `aliases`, cómo se llama a sí misma y cómo la llaman sus enemigos.
- Archivo en ASCII. H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** quiénes son, qué quieren y por qué importan.
- **Datos clave:** la tabla completa; los miembros, aproximados («unos trescientos», «tres familias y sus criados»).
- **Propósito:** ver arriba.
- **Doctrina y costumbres:** en qué creen, sus ritos y costumbres, y cómo hablan y visten (por qué se los reconoce).
- **Estructura:** de 2 a 5 rangos, del más alto al más bajo, con quién ocupa los altos y qué hace cada uno.
- **Cómo se entra:** quién puede entrar, la prueba o el rito, y cómo se sale (si se puede).
- **Miembros notables:** de 2 a 4, con su enlace y su papel. Nombres nuevos, con `generate_names.py`.
- **Recursos e influencia:** riqueza y medios, a quién pueden mover y dónde operan. Coherente con `recursos`.
- **Métodos:** cómo actúan a la vista y lo que no se cuenta.
- **Símbolos:** el emblema (lo que muestra la imagen), los colores y señales, y el lema.
- **Aliados y enemigos:** de 2 a 4 filas, con la relación (alianza, rivalidad, vasallaje, deuda, guerra abierta), por qué existe y qué cambia para la facción, vistos desde ella.
- **Historia:** su fundación, de 2 a 5 momentos decisivos y el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para su emblema o su estandarte: el soporte (un escudo pintado, un estandarte de tela, un sello de cera, una insignia, un tatuaje), la figura principal, los colores y materiales, los elementos secundarios y el carácter del diseño (austero, recargado, tosco).
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `situacion`, `alcance`, `visibilidad`, `fundacion`, `disolucion`, `objetivo` y `recursos`: ver arriba. `lema` y `miembros`: texto breve.
- Relaciones, solo con enlaces:
  - `sede` (un lugar o un asentamiento) y `zonas` donde operan (regiones o asentamientos);
  - `lider` y `figuras` (miembros notables): cada uno la tiene en sus `facciones`;
  - `faccion_madre` y `ramas`: de qué organización depende y qué capítulos o brazos tiene; recíprocas;
  - `aliados`: otras facciones; recíproca, porque una alianza es de las dos;
  - `rivales`: las que esta tiene por rivales; no se espeja sola: si la rivalidad es mutua, va también en la otra, y si es de un solo lado, solo en esta (ver «Relaciones» en `SKILL.md`);
  - `creencias` que siguen o administran;
  - `culturas` a las que pertenecen: cada cultura la tiene en sus `instituciones`;
  - `objetos` que guardan (reliquias, insignias, tesoros);
  - `sistemas` que enseñan, guardan, regulan o persiguen (un arte, un don, una técnica): cada uno la tiene en sus `facciones`;
  - `eventos` en que tomaron parte: cada evento la tiene en sus `bandos`;
  - `era` en que se fundó.
- `relevancia`: 5 el gobierno del foco o una potencia mundial; 4 una facción regional; 3 una facción local importante; 2 una menor; 1 un grupo de unos pocos.
- `ultima_revision` sin comillas.

## Coherencia
- **La Ficha:** su tecnología, sus poderes (según los sistemas de poder) y su papel ante el conflicto central encajan con la Ficha. Si la Ficha prohíbe algo, la facción no lo tiene.
- **Lo que ya existe:** su sede, sus miembros, los pueblos a los que pertenece, los eventos en que participó y las notas que ya la mencionan (como enlace pendiente) deben encajar con lo que dicen. Léelas (`build_context.py`).
- **Su sede y su territorio:** la sede la lista en sus `facciones` (un lugar o un asentamiento) o en su `control` (una región que gobierna).
- **Reciprocidad:** sus aliados, ramas, miembros, culturas y eventos que ya existen la listan en su propiedad inversa. Sus rivales, no.
- **Glosario:** registra su nombre, sus otros nombres, sus rangos y sus términos propios.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 3 y 8 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- quien la dirige (`lider`);
- un miembro notable (`figuras`);
- su sede (`sede`);
- un rival (`rivales`);
- una rama o un capítulo (`ramas`);
- lo que guardan (`objetos`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, la facción guarda un secreto (su fundador no es quien dicen, sirve a otro amo, su objetivo verdadero es otro, uno de sus rangos no existe en ningún papel). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] La categoría la lleva a su carpeta.
- [ ] Tiene un objetivo concreto, recursos coherentes con su alcance y una grieta interna.
- [ ] Una facción regional o mundial que no estaba en el canon quedó como `Confirmar: …`.
- [ ] La situación cuadra con sus fechas y con el año actual.
- [ ] Sus miembros, aliados, ramas, culturas y eventos que ya existen la listan.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
