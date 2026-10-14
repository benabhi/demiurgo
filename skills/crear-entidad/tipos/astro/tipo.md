# Tipo: astro

Lo que hay en el cielo del mundo, tal como se ve desde él: soles, lunas, planetas, estrellas y constelaciones, cometas, fenómenos del cielo (eclipses, auroras, lluvias de estrellas, un cielo que cambia de color) y la forma misma del cielo y del mundo según los que lo miran (la bóveda, los cielos superpuestos, el borde). La ficha dice cómo se ve, su ciclo y lo que rige, lo que se sabe de él, lo que se cree, su lugar en la cultura y su historia.

**No es un astro:**
- un mundo que se visita o se habita (`region`): una luna habitada o un planeta al que se viaja es una región (`Grandes_Regiones`). Su nota de astro, si importa también como cuerpo del cielo, cuenta cómo se ve desde el mundo;
- una fuerza extraordinaria que actúa en el mundo (`fenomeno`): la niebla roja que cae del cielo es un fenómeno; el cometa que pasó antes de que cayera, un astro que lo enlaza en `fenomenos`. Si lo que importa es su ciclo en el cielo, es un astro; si es lo que hace en el mundo, un fenómeno;
- el dios que lo encarna (`deidad`): la luna es un astro; la diosa que dicen que es la luna, una deidad. Se enlazan en `deidades` y `astros`;
- el calendario que se cuenta con él (`calendario`): el astro lo marca; el calendario lo enlaza en sus `astros`.

## Identidad del tipo
- **Emoji del tipo:** 🌙, al inicio del H1: `# 🌙 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según lo que es (☀️ sol, 🌕 luna, 🪐 planeta, ⭐ estrella, ✨ constelación, ☄️ cometa, 🌘 eclipse, 🌌 aurora o forma del cielo…).
- **Carpeta:** fija, `70_Sistemas_y_Cosmologia/Cosmos_y_Astros`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Astro.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, valores permitidos, `solo_si`, recíprocas y relaciones). El motor no crea astros desde cero (`crear_desde_cero: false`): el cielo es la base de los calendarios, las fes y los mitos, y cambiarlo cambia el mundo entero. Solo crea los que ya nombran las notas (la luna de un calendario, la constelación de un mito).

**Hechos importantes:** casi todo el cielo lo es, porque lo ve todo el mundo. Una estrella menor o una constelación de un pueblo son detalles que Claude puede inventar según la autonomía de la Ficha. Son importantes, y van como `Confirmar: …` en Preguntas Abiertas con el astro como primer enlace de la línea:
- un sol, una luna o un planeta, y la forma del cielo;
- un astro extraordinario (`naturaleza: sobrenatural`) o ligado al conflicto central;
- un cometa o un fenómeno del cielo que marcó la historia o que se espera.

Si el usuario pide el astro, el pedido es la aprobación. Si la Ficha deja el cielo por definir (los soles y las lunas son parte del pilar del calendario), sigue `referencias/pilares.md` antes de decidirlo.

## El cielo que miran (lo más importante)
- **Se ve desde el mundo:** la ficha cuenta lo que ve alguien que mira hacia arriba: su color, su brillo, su tamaño en el cielo, cómo cambia (sus fases, su camino), cuándo y desde dónde se ve. Nada de datos de astronomía moderna si la Ficha no tiene esa técnica: con tecnología antigua, nadie sabe a cuántas leguas está una estrella.
- **Tiene un ciclo, y el ciclo rige cosas:** cada cuánto vuelve, cuánto dura una fase, y lo que marca (los meses, las mareas, las estaciones, las cosechas, la noche más larga). Si rige el calendario, encaja con sus tablas (`world_calendar.py` las muestra) y el calendario lo lista en sus `astros`.
- **Lo que se sabe y lo que se cree, por separado:** lo que saben quienes lo observan (con sus instrumentos y sus errores) y lo que cree la gente (presagios, dioses, destinos). Lo que de verdad es o hace, si se decide, va en un secreto.
- **Lo extraordinario tiene reglas:** si hace algo fuera de lo natural (un astro que mueve las aguas de los muertos, una luna que da poder), lo hace por un `sistema` o un `fenomeno` del mundo, con sus límites.
- **Mundo inventado:** si la Ficha lo pide, ni su nombre ni sus mitos calcan los del cielo real (los planetas y las constelaciones de la Tierra); puede compartir lo universal (la luna que marca los meses), no su forma.

## Categoría, naturaleza, visibilidad, situación y ciclo
- `categoria`: `sol`, `luna`, `planeta`, `estrella`, `constelacion`, `cometa`, `fenomeno_celeste` (eclipses, auroras, lluvias de estrellas), `cosmos` (la forma del cielo y del mundo según quienes lo miran) u `otro`.
- `naturaleza`: `natural`, `sobrenatural` (es o hace algo extraordinario), `artificial` (lo puso alguien en el cielo) o `desconocida`.
- `visibilidad`: `diaria`, `nocturna`, `estacional` (solo en una época del año), `periodica` (vuelve cada tanto: un cometa, un eclipse), `rara` (se ve una vez en la vida, o menos) u `oculta` (no se ve: se sabe de ella por cálculos, por textos o por fe).
- `situacion`:
  - `estable`: está como siempre;
  - `cambiante`: algo le pasa (se apaga, crece, cambia de color, se desvía);
  - `desaparecido`: ya no está (con `desaparicion`, si se sabe);
  - `por_venir`: se espera (el cometa que vuelve, el astro de una profecía), con `aparicion` en el año en que se espera, si se sabe.

  `check_note.py` comprueba que cuadre con sus fechas y con el año actual.
- `ciclo`: texto breve («veintiocho días», «vuelve cada setenta años», «siempre en el mismo sitio»).
- `aparicion` y `desaparicion`: el año del eje en que apareció o se espera, y en que desapareció, si se saben. Casi siempre quedan vacíos: lo que siempre estuvo no tiene año. Si el calendario está por definir, quedan vacíos.

## Nombre
- Como lo llaman quienes lo miran, en la lengua común: «la Luna Parda», «el Ojo del Pastor», «la Corona de Sal». Con `generate_names.py` si el nombre lleva una palabra inventada.
- Cada pueblo lo llama a su manera, y los sabios a la suya: los otros nombres van en `aliases` y en «En la cultura».
- Se enlaza cada vez que una nota lo nombra. Archivo en ASCII (`Luna_Parda.md`); H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, cómo se ve y por qué importa.
- **Datos clave:** la tabla completa. «Lo que rige»: lo que marca (o «nada», si no marca nada).
- **Cómo se ve:** en el cielo (su color, su brillo, su tamaño, su forma); sus cambios (fases, camino, lo que hace a lo largo del año); dónde y cuándo se ve mejor.
- **Su ciclo y lo que rige:** el ciclo, con sus números si se saben; lo que marca (el calendario, las mareas, las estaciones; los calendarios enlazados y en `calendarios`); lo que se le atribuye (lo que la gente cree que provoca, y lo que provoca de verdad si es un fenómeno del mundo, enlazado en `fenomenos`).
- **Lo que se sabe:** quién lo observa (una orden, unos navegantes, unos pastores; con sus instrumentos); lo que saben; lo que no saben (y lo que creen saber mal).
- **Lo que se cree:** de 1 a 3 creencias: presagios, dioses (`deidades`), destinos, lo que no se hace bajo su luz. Contadas como lo que creen quienes las siguen.
- **En la cultura:** sus nombres en cada pueblo; las fiestas y los ritos que se hacen con él (enlazados y en `costumbres`); para qué se usa (orientarse, sembrar, medir el tiempo, adivinar).
- **Historia:** desde cuándo se conoce o cómo apareció; de 2 a 4 momentos decisivos (un eclipse que paró una batalla, la noche en que se apagó); y el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas, de quien lo observa, de quien lo venera o de quien lo teme.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para el astro sobre un paisaje del mundo: cómo se ve en el cielo, el paisaje de abajo, la luz que da, y quien lo mira (pequeño). Un sol, al alba o al ocaso; un fenómeno del cielo, en su momento; la forma del cielo, como la imaginan quienes lo miran.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `naturaleza`, `visibilidad`, `situacion`, `ciclo`, `aparicion` y `desaparicion`: ver arriba.
- Relaciones, solo con enlaces:
  - `orbita`: el astro alrededor del cual gira (una luna, su planeta), que lo lista en sus `satelites`; y `satelites`: los que giran a su alrededor; recíprocas;
  - `calendarios` que se cuentan con él: cada uno lo tiene en sus `astros`;
  - `deidades` que lo encarnan o que viven en él: cada una lo tiene en sus `astros`;
  - `creencias` que lo veneran o lo temen, `mitos` que lo cuentan y `costumbres` que se hacen con él;
  - `fenomenos` que provoca o que se le atribuyen;
  - `sistemas` que lo usan o que explican lo que hace (una astrología, una navegación, un poder que crece con su luz);
  - `pueblos` que lo miran, lo nombran o lo siguen;
  - `obras` que lo describen (un tratado, un mapa del cielo): cada una lo tiene en su `trata_de`;
  - `relacionados`: otros astros con los que va de la mano (las estrellas de una constelación, el astro que lo eclipsa); recíproca;
  - `era` en que apareció o cambió.
- `fuentes`: los textos o relatos de donde se sabe (imprescindible en uno oculto o desaparecido).
- `relevancia`: 5 el sol o la luna del mundo, o el astro de su conflicto central; 4 el que rige un calendario o una fe; 3 el conocido en su región; 2 una estrella o una constelación de un pueblo; 1 una que conocen pocos.
- `ultima_revision` sin comillas.

## Coherencia
- **La Ficha y el calendario:** el cielo es uno para todo el mundo (aunque cada pueblo lo llame distinto). Lo que rige encaja con el calendario de referencia y sus tablas (meses, estaciones, festividades); lo que se sabe de él, con la técnica del mundo.
- **Lo que ya existe:** las notas que ya lo nombran (como enlace pendiente: la luna de un calendario, el sol de una fe, la constelación de un mito) cuentan cosas de él. Léelas (`build_context.py`) y no las contradigas.
- **Reciprocidad:** su astro central lo lista en `satelites` (y sus satélites, en `orbita`); sus calendarios y sus deidades, en `astros`; sus astros relacionados, en `relacionados`.
- **Glosario:** registra su nombre (como astro), sus otros nombres y los términos que nacen de él (el nombre de una fase, de una noche, de un presagio).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 1 y 5 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- la fe o la deidad que lo venera o lo encarna (`creencias`, `deidades`);
- el mito que lo cuenta (`mitos`);
- la fiesta que se hace con él (`costumbres`);
- quien lo observa (una facción, una orden);
- el astro con el que va (`orbita`, `relacionados`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, el astro guarda un secreto (no es lo que parece, se está acercando, alguien lo puso allí, su ciclo se está rompiendo y quien lo vigila lo calla, lo que provoca de verdad no es lo que se cree). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] Se cuenta como se ve desde el mundo, sin saberes que su técnica no tiene.
- [ ] Su ciclo y lo que rige encajan con el calendario y sus tablas, y el calendario lo lista en sus `astros`.
- [ ] Lo que se sabe y lo que se cree van por separado; la verdad, si se decide, en un secreto.
- [ ] No calca un astro ni un mito del cielo real.
- [ ] Si no es un detalle y no lo pidió el usuario, quedó como `Confirmar: …`.
- [ ] Su astro central, sus satélites, sus calendarios, sus deidades y sus astros relacionados que ya existen lo listan.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
