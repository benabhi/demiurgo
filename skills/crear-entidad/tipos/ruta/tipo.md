# Tipo: ruta

Lo que une lugares, o lo que sale de uno y no lleva a ninguno: caminos, calzadas y senderos; pasos de montaña, desfiladeros y vados; rutas por río, por mar, por el aire o bajo tierra; rutas entre astros, si el mundo las tiene; y portales que unen dos sitios sin cruzar lo que hay en medio. La ficha dice qué une (o adónde no lleva), por dónde va y cuánto se tarda, cómo se recorre, quién la recorre y qué lleva, qué peligros y controles tiene, sus atajos y desvíos, y su historia.

**No es una ruta:**
- el sitio donde empieza, para o acaba (`asentamiento`, `lugar`): la ruta los enlaza;
- un puente, un vado con nombre, un faro o una posada del camino: son `lugar` si merecen nota, y la ruta los lista en `paradas`;
- la región o el accidente que cruza (`region`, o un `lugar` natural como una montaña): la ruta los atraviesa;
- el comercio, la peregrinación o la guerra que circulan por ella: la ruta cuenta quién la recorre y qué lleva. El gremio que comercia es una `faccion`, y la fe que peregrina, una `creencia`;
- las reglas del poder que abre un portal (`sistema`): el portal las enlaza en `sistemas` y no las rompe.

## Identidad del tipo
- **Emoji del tipo:** 🧭, al inicio del H1: `# 🧭 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según lo que es (🛤️ camino, 🥾 sendero, ⛰️ paso, 🛶 ruta fluvial, ⛵ ruta marítima, 🕳️ ruta subterránea, 🦅 ruta aérea, 🌌 ruta espacial, 🌀 portal, 🐪 ruta de caravanas…).
- **Carpeta:** fija, `10_Mundo/Rutas_y_Conexiones`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Ruta.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, escalas, valores permitidos, `solo_si`, mapa, recíprocas y relaciones). Es de la familia `lugar`, y su `completa` dice qué enlaces pendientes de otras fichas puede crear: el escenario de un evento, de un mito o de una costumbre (`lugares`), el lugar sagrado de una fe, la zona que afecta un fenómeno o donde actúa una facción o una afección, el hábitat de una criatura y el dominio de un linaje, cuando las notas que lo nombran describen un camino, un paso o un portal. Los enlaces pendientes de `rutas` y `conexiones` los completa siempre una ruta.

**Hechos importantes:** una senda, un camino entre dos aldeas o un paso de pastores son detalles que Claude puede inventar según la autonomía de la Ficha. Son importantes, y van como `Confirmar: …` en Preguntas Abiertas con la ruta como primer enlace de la línea:
- la gran ruta que vertebra una región o une reinos;
- un portal, o una ruta que cambia lo que se puede hacer en el mundo (une lugares muy lejanos, cruza el conflicto central, abre una salida que no había);
- una ruta perdida que llevaría a algo de gran peso.

Si el usuario pide la ruta, el pedido es la aprobación.

## Lo que une (lo más importante)
Una ruta es una pieza del mapa del mundo: une lugares que existen y tarda lo que tarda.
- **Sus extremos y sus paradas son entidades:** `partida`, `destino` y `paradas` son asentamientos o lugares, enlazados a su nota o como enlaces pendientes. Reutiliza los que ya existen: una ruta que inventa su propio destino cuando ya hay una ciudad al otro lado de la sierra rompe el mapa.
- **Encaja con la geografía:** cruza lo que hay entre sus extremos (las regiones que lista en `regiones`, los ríos, las sierras, el conflicto central) y su categoría sale de ahí: entre dos puertos, una ruta marítima; a través de una cordillera, un paso; bajo una ciudad, túneles.
- **Respeta las distancias que ya se saben:** antes de fijar los días, `python <directorio de esta skill>/scripts/routes.py <Partida> <Destino>` dice si ya hay un camino conocido entre ellos y cuánto se tarda. Una ruta directa tarda menos que el rodeo, o la nota explica por qué no (el atajo de la montaña es más corto en leguas, pero más lento). Lo que cuentan sus regiones y sus extremos («a tres jornadas de la costa») también manda.
- **Trazado:**
  - `lineal`: une su `partida` y su `destino`, con sus paradas en orden;
  - `sin_salida`: sale de su `partida` y no lleva a ningún sitio con nombre: se pierde en un bosque, se corta en un barranco, se borra en la arena. Son los senderos que no llevan a ningún lado, y su misterio es parte de la nota: dónde se pierde y qué se cuenta de lo que habría más allá. Si al final hay una entidad (una ruina, una torre), la ruta sí lleva a algún sitio: es `lineal` y esa entidad es su destino;
  - `circular`: vuelve a su `partida` (una ronda de vigilancia, un circuito de peregrinación, la vuelta del buhonero, la trashumancia);
  - `red`: varias vías con un nombre común (las calzadas de un reino, los túneles de una ciudad, una red de portales). No tiene partida ni destino; sus rutas la tienen en `red` y ella las lista en `ramales`.
- **Conexiones:** las rutas que se cruzan con ella, nacen de ella o la continúan van en `conexiones` (recíproca). Un ramal es una ruta `lineal` que parte de una parada de otra.

## Categoría
- `camino`: por tierra y con obra: calzadas, carreteras, caminos de carros;
- `sendero`: sendas, veredas y trochas sin obra, a pie o a lomo;
- `paso`: el cruce de un obstáculo: un puerto de montaña, un desfiladero, una ciénaga, un estrecho, un vado largo;
- `fluvial`: por río o por canal;
- `maritima`: por mar o por un gran lago;
- `subterranea`: túneles, galerías, cuevas o minas que llevan de un sitio a otro;
- `aerea`: por el aire (monturas, naves, lo que el mundo tenga);
- `espacial`: entre astros, estaciones o mundos, si el mundo los tiene;
- `portal`: une dos sitios sin cruzar lo que hay en medio (una puerta, un círculo de piedras, un espejo, un salto). Sigue las reglas de su `sistema`: qué lo abre, qué cuesta, quién puede usarlo y qué no puede hacer;
- `otro`.

Los pilares mandan: una ruta aérea o espacial, o un portal, solo si la tecnología y los poderes de la Ficha lo permiten.

## Situación, certeza, uso y peligro
- `situacion`:
  - `en_uso`: se recorre con normalidad;
  - `en_declive`: cada vez menos gente la usa;
  - `cortada`: hoy no se puede pasar (un derrumbe, una guerra, un sello, el conflicto central), aunque podría reabrirse;
  - `abandonada`: se sabe por dónde va, pero ya nadie la usa (con `cierre`, si se sabe);
  - `perdida`: nadie sabe ya por dónde iba ni cómo se abre; queda en textos, mapas viejos o relatos;
  - `en_construccion`: se está abriendo y aún no llega a su destino.

  `check_note.py` comprueba que cuadre con sus fechas y con el año actual.
- `certeza`: `cierta` (se recorre, o hay quien sabe por dónde iba) o `dudosa` (solo la cuentan un texto antiguo, un mapa viejo, una canción o un rumor: puede que nunca existiera, o que no lleve adonde dicen). La ficha de una ruta dudosa cuenta lo que dicen sus fuentes, nunca si es verdad: las enlaza en `fuentes` y en el texto («según el [[Itinerario_de_Ejemplo|Itinerario de Ejemplo]]»). La verdad, si se decide, va en un secreto.
- Solo las rutas ciertas que se pueden recorrer hoy (`en_uso` o `en_declive`) cuentan para las distancias del mundo.
- `uso`: para qué se usa sobre todo: `comercio`, `peregrinacion`, `militar`, `correo`, `migracion`, `trashumancia`, `contrabando`, `exploracion`, `local` (la gente de la zona, para ir y venir) u `otro`.
- `transito`: `nulo`, `escaso`, `moderado` o `intenso`: cuánta gente la recorre hoy.
- `peligrosidad`, del 1 al 5: 1, se recorre sin miedo; 3, nadie la recorre solo; 5, pocos vuelven.
- `apertura` y `cierre`: el año del eje en que se abrió y en que se abandonó o se perdió, si se saben. Si el calendario está por definir, quedan vacías y el texto usa fechas relativas.

## Tiempos de viaje (datos)
Las rutas guardan sus tiempos como datos, y con ellos `routes.py` arma el grafo de distancias del mundo.
- `medio`: cómo se recorre de ordinario («a pie», «a caballo», «en carreta», «en barcaza», «en nave»…), y `dias`: cuánto se tarda de punta a punta por ese medio. Con decimales, si hace falta (`0.5`, medio día). En un portal, lo que dura cruzarlo, a menudo `0`.
- La tabla **Recorrido** da cada tramo en orden, con sus días por ese medio:
  - cada tramo empieza donde acabó el anterior; el primero, en la partida; el último, en el destino. En una circular, el último vuelve a la partida; en una sin salida, acaba donde se pierde. En una red, cada fila es un tramo entre dos de sus nudos;
  - los días de los tramos suman `dias`. Un tramo que nadie sabe cuánto dura (en una ruta perdida o dudosa) lleva «?», y entonces `dias` puede quedar vacía;
  - los puntos que son entidades van enlazados (`[[Nota\|texto]]`, por estar en una tabla), y los asentamientos y lugares, también en `paradas`, en el mismo orden; los demás, como texto («el vado de las tres piedras»).
- Los otros medios van en «Cómo se recorre» («a pie, el doble»).
- `check_note.py` comprueba el recorrido: que los tramos encadenen, que sus días sean números y sumen los de `dias`, y que las paradas estén en él.

## Nombre
- Como la llaman quienes la recorren: «el Camino de la Sal», «la Senda de los Ahorcados», «el Paso del Lobo», «la Puerta de Ceniza». Con `generate_names.py` si el nombre lleva una palabra inventada.
- Cada lado puede llamarla a su manera, y una ruta perdida puede tener el nombre de su fuente: los otros nombres van en `aliases`.
- Se enlaza cada vez que una nota la nombra. Archivo en ASCII (`Camino_de_la_Sal.md`); H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué une (o adónde no lleva), por dónde va y por qué importa.
- **Datos clave:** la tabla completa. «De dónde a dónde»: sus extremos («de X a Y por Z»; «de X a ninguna parte»; «de X a X, por las aldeas del valle»; «red de cuatro rutas entre…»). «Longitud», en la medida del mundo («unas cuarenta leguas»). «Tiempo de viaje», con los días y el medio. «Situación», con su certeza si es dudosa y de dónde se sabe.
- **Recorrido:** la tabla de tramos (ver «Tiempos de viaje»): de 2 a 6 con relevancia 3 o más; con menos, 1 o 2. «Cómo es» dice el terreno, la obra (empedrado, tablones sobre el barro, escalones en la roca, boyas), lo que se ve y lo que hay al llegar.
- **Mapa** (solo si le toca: desde relevancia 3, salvo los portales; `check_note.py --depth ruta:<relevancia>:<categoría>`): el itinerario, la leyenda de sus puntos en orden (la partida es la 1), hasta 12, con su orientación, lo que se ve y sus conexiones (cada punto con el siguiente; en una circular, el último con la 1). Los atajos y desvíos conocidos van como conexiones o como pasos ocultos (la senda de los contrabandistas), y las emboscadas conocidas, como trampas. Con más de 12 puntos, la leyenda lleva los principales y el Recorrido, todos. Ver `referencias/mapas.md`.
- **Cómo se recorre:** el medio y el ritmo (y los otros medios); cuándo se puede (las estaciones, las mareas, las horas, la noche en que se abre el portal); lo que hace falta (un guía, un salvoconducto, un peaje, una llave, un rito); lo que cuesta (dinero, tiempo, el precio que pide el poder del portal).
- **Quién la recorre:** los viajeros (quiénes y cuántos); lo que lleva (sus mercancías, en `mercancias` las que son entidades); las costumbres del camino (dejar una piedra en el mojón, no silbar en el desfiladero), enlazadas si son entidades.
- **Peligros y controles:** los peligros (el terreno, el clima, las criaturas, los bandidos, el conflicto central, perderse); los controles y peajes (quién cobra, quién vigila y qué pide); quién la mantiene, y cómo está (cuidada, comida por la maleza, a medio hundir).
- **Atajos y desvíos:** de 1 a 3, cada uno con lo que gana y lo que cuesta: el atajo que ahorra dos días a cambio de un peligro, el desvío que evita un control, el ramal que lleva a otro sitio (enlazado y en `conexiones`, si es una ruta con nombre).
- **Historia:** su origen (quién la abrió y por qué, o cómo se abrió sola: el paso de los rebaños, la grieta de un terremoto); de 2 a 4 momentos decisivos; y el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas, de viajeros, de quien la cobra o de quien se perdió en ella.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para la vista a lo largo de la ruta en su tramo más reconocible, con sus viajeros (o sin nadie, si está abandonada): el camino que se aleja, su obra, el paisaje, el tiempo que hace. En un portal, el portal y quien está a punto de cruzarlo; en una ruta perdida, lo que queda de ella o el tramo tal como lo describe su fuente.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `trazado`, `situacion`, `certeza`, `uso`, `transito`, `peligrosidad`, `medio`, `dias`, `apertura` y `cierre`: ver arriba.
- Relaciones, solo con enlaces:
  - `partida` (en las lineales, las sin salida y las circulares) y `destino` (solo en las lineales): un asentamiento o un lugar; cada uno la tiene en sus `rutas`;
  - `paradas`: los asentamientos y lugares por los que pasa, en orden; cada uno la tiene en sus `rutas`;
  - `regiones` que cruza, en orden: cada una la tiene en sus `rutas`;
  - `conexiones`: las rutas que se cruzan con ella o nacen de ella; recíproca;
  - `red`: la red a la que pertenece, que la tiene en sus `ramales`; y `ramales`, solo en una red: sus rutas;
  - `control`: las facciones que la gobiernan, la mantienen o cobran su peaje; `facciones`: las que la recorren o la acechan (un gremio de caravaneros, una banda);
  - `pueblos` que la abrieron o la recorren, y `creencias` que peregrinan por ella o la tienen por sagrada;
  - `criaturas` que la acechan (cada una la tiene en su `habitat`), `fenomenos` que la afectan (la tienen en sus `zonas_afectadas`) y `eventos` que ocurrieron en ella (la tienen en sus `lugares`);
  - `sistemas`: el poder o la técnica que la hace posible (el de un portal, el de una ruta aérea);
  - `mercancias`: lo que lleva, de cualquier tipo (sin propiedad que les dé tipo, cada enlace pendiente lo recibe con `pending_links.py --set`); un material la tiene en sus `rutas`;
  - `era` en que se abrió.
- `fuentes`: los textos, mapas o relatos de donde se sabe (imprescindible en una ruta dudosa).
- `relevancia`: 5 la ruta que vertebra el mundo o su foco (la única salida, la gran ruta de la que todo depende); 4 la que une regiones o grandes ciudades; 3 la conocida en su comarca; 2 un camino local; 1 un sendero que pocos conocen.
- `ultima_revision` sin comillas.

## Coherencia
- **La geografía:** sus extremos, sus paradas y sus regiones existen y encajan con lo que cruza; sus días, con la escala de la Ficha, con las distancias que ya se saben (`routes.py`) y con lo que cuentan las notas de sus regiones y sus extremos.
- **La Ficha:** la tecnología y los poderes deciden cómo se viaja; el conflicto central se nota en el camino (qué lo amenaza, qué ya no se puede cruzar).
- **Lo que ya existe:** las notas que ya la nombran (como enlace pendiente) y las de sus extremos cuentan cosas de ella. Léelas (`build_context.py`) y no las contradigas: si su ciudad dice que la caravana sale en primavera, sale en primavera.
- **Reciprocidad:** su partida, su destino y sus paradas la listan en `rutas`; sus regiones, también; las rutas que conecta, en `conexiones`; su red, en `ramales`; sus criaturas, fenómenos y eventos, en su propiedad inversa.
- **Los mapas de lo que une:** la ruta aparece en los mapas de las regiones, los parajes y las ciudades que cruza, si tienen leyenda: al crearla, `map_key.py --sync-routes` la pone en su bloque «Rutas» y conecta las zonas que une (ver «Las rutas en los mapas» en `referencias/mapas.md`). Los portales y las rutas por el aire o el espacio no se dibujan en ellos, ni las perdidas o dudosas.
- **Glosario:** registra su nombre (como ruta), sus otros nombres y los términos que nacen de ella (el nombre de un peaje, de un oficio del camino).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 2 y 8 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- su partida o su destino, si aún no existen, y una parada con nombre (una posada, un fuerte, un vado);
- quien la controla, la cobra o la acecha (`control`, `facciones`);
- una criatura del camino (`criaturas`);
- lo que lleva (`mercancias`);
- la ruta que se cruza con ella (`conexiones`);
- en una ruta dudosa, la fuente que la cuenta (una obra).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, la ruta guarda un secreto (un tramo que nadie usa porque oculta algo, el peaje que financia otra cosa, la ruta perdida que alguien sigue usando, el portal que no siempre lleva al mismo sitio, lo que de verdad le pasó a la caravana que desapareció). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] Sus extremos y sus paradas son entidades (las que existen, enlazadas a su nota) y encajan con la geografía y con sus regiones.
- [ ] Sus días cuadran con las distancias que ya se saben (`routes.py`) y con la escala de la Ficha.
- [ ] El Recorrido encadena sus tramos de la partida al destino (o hasta donde se pierde) y sus días suman `dias`.
- [ ] Un portal o una ruta aérea o espacial respetan los pilares y las reglas de su sistema.
- [ ] Una ruta dudosa cuenta lo que dicen sus fuentes, sin afirmar que exista.
- [ ] Si no es un detalle y no la pidió el usuario, quedó como `Confirmar: …`.
- [ ] Su partida, su destino, sus paradas, sus regiones y sus conexiones que ya existen la listan; los mapas que cruza la muestran (`--sync-routes`).
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
