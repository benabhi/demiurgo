# Tipo: material

Las materias del mundo en su estado natural y los recursos de los que vive: metales, piedras, gemas, cristales, maderas, materias de origen animal o vegetal (hueso, marfil, pieles, resinas, fibras), sustancias (sal, azufre, aceites, venenos), compuestos exóticos y los recursos que se reparten por la tierra (el agua, el suelo fértil, las fuentes de energía, los bancos de pesca). La ficha dice cómo es y cómo se reconoce, dónde se encuentra, cómo se saca y se trabaja, para qué sirve, qué riesgos tiene, cuánto vale y quién lo controla, qué se cree de él y su historia.

**No es un material:**
- lo que se fabrica con él (`objeto`): el mineral es un material; el lingote, la tela o el cuero curtido son objetos (`material_procesado`), y lo que se forja con ellos, también. El objeto lo enlaza en sus `materiales`;
- el ser vivo del que sale (`criatura` o `flora`): la criatura o la planta son seres; el material es lo que se saca de ellos (su piel, su resina);
- el sitio donde se encuentra (`lugar`, `asentamiento`, `region`): la mina, la cantera o la región son lugares, y el material los enlaza en `yacimientos`;
- un poder (`sistema`): el material puede alimentarlo, guardarlo o frenarlo, según sus reglas, pero las reglas son del sistema;
- el daño que causa (`afeccion`): el polvo que pudre los pulmones de los mineros es una afección, y el material la enlaza.

## Identidad del tipo
- **Emoji del tipo:** 💎, al inicio del H1: `# 💎 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según lo que es (⛓️ metal, 🪨 piedra, 💎 gema, 🔮 cristal, 🪵 madera, 🦴 materia animal, 🧂 sustancia, ☄️ compuesto exótico, 💧 agua, 🌾 suelo, ⚡ energía, 🐟 alimento…).
- **Carpeta:** según la `categoria`:
  - las materias (`metal`, `piedra`, `gema`, `cristal`, `madera`, `organico`, `sustancia`, `exotico`) van en `50_Naturaleza/Minerales_y_Materiales_Naturales`;
  - los recursos que se reparten por la tierra (`agua`, `suelo`, `energia`, `alimento`) van en `50_Naturaleza/Recursos_Naturales`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Material.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, escalas, valores permitidos, `solo_si`, recíprocas y relaciones). El motor puede crear materiales desde cero.

**Hechos importantes:** una piedra de cantera, una madera de la comarca o una sal de la costa son detalles que Claude puede inventar según la autonomía de la Ficha. Son importantes, y van como `Confirmar: …` en Preguntas Abiertas con el material como primer enlace de la línea:
- un material con propiedades extraordinarias (`naturaleza: sobrenatural`), o legendario;
- el que mueve la economía de una región o del mundo, o por el que se hacen guerras;
- el que responde al conflicto central (lo que lo frena, lo que nace de él).

Si el usuario pide el material, el pedido es la aprobación.

## Lo que vale un material (lo más importante)
Un material importa por lo que hace con el mundo: dónde está, quién lo saca, quién lo controla, qué permite hacer y qué cuesta.
- **Es concreto:** su aspecto, su tacto, su olor, su peso, cómo responde al fuego, al agua o al tiempo, y cómo se reconoce y se falsifica. Nada de generalidades («un metal muy resistente»): el gesto del herrero que lo prueba, el color de la llama, el sonido al golpearlo.
- **Está en algún sitio:** sus `yacimientos` (las regiones, las minas, los ríos o los lugares donde se encuentra) son entidades. Lo escaso está lejos, es peligroso o tiene dueño, y eso mueve gente, rutas y conflictos.
- **Tiene un precio y un dueño:** cuánto vale en la moneda o el trueque del mundo, quién lo compra y quién lo vende, por qué rutas viaja y quién controla su comercio.
- **Sus propiedades extraordinarias tienen reglas:** si hace algo fuera de lo natural, lo hace por un `sistema` del mundo, con sus límites y su precio, y no rompe sus reglas. Los pilares de la Ficha mandan: en un mundo sin poderes, un material no los tiene.
- **Responde al mundo:** la tecnología decide qué se puede sacar y trabajar (sin máquinas, una veta profunda es inalcanzable), y el conflicto central se nota en él (lo que lo envenena, lo que lo vuelve valioso).

## Categoría, naturaleza, rareza, situación y peligro
- `categoria`:
  - `metal`: metales y sus menas, en bruto;
  - `piedra`: piedras de construcción, de talla o de molino;
  - `gema`: piedras preciosas o de adorno;
  - `cristal`: cristales y vidrios naturales;
  - `madera`: maderas, cortezas y lo que da un árbol al cortarlo;
  - `organico`: lo que sale de un ser vivo (hueso, marfil, pieles en bruto, resinas, fibras, venenos animales);
  - `sustancia`: sal, azufre, aceites, breas, tierras de color y otras sustancias naturales;
  - `exotico`: compuestos que no encajan en lo conocido;
  - `agua`, `suelo`, `energia` y `alimento`: los recursos que se reparten por la tierra (las fuentes y los pozos, la tierra fértil y los pastos, lo que da fuerza o calor, la pesca, la caza o la cosecha silvestre).
- `naturaleza`: `natural`, `sobrenatural` (tiene propiedades extraordinarias, según un sistema del mundo), `artificial` (lo hizo alguien, aunque hoy se encuentre como se encuentra un mineral: los restos de una técnica perdida) o `desconocida`.
- `rareza`: `comun`, `escaso`, `raro`, `unico` (un solo yacimiento o un solo hallazgo) o `legendario` (solo lo cuentan los relatos: puede que no exista). La ficha de uno legendario cuenta lo que dicen sus fuentes (en `fuentes` y en el texto), nunca si es verdad; la verdad, si se decide, va en un secreto.
- `situacion`:
  - `en_explotacion`: se saca y se trabaja hoy;
  - `sin_explotar`: se conoce, pero nadie lo saca (no se puede, no se sabe, no se atreven);
  - `agotandose`: queda poco, y se nota;
  - `agotado`: ya no queda (con `agotamiento`, si se sabe);
  - `perdido`: se sabe que existió, pero no dónde está;
  - `prohibido`: alguien prohíbe sacarlo, venderlo o usarlo.

  `check_note.py` comprueba que cuadre con sus fechas y con el año actual.
- `peligrosidad`, del 1 al 5: 1, se toca sin miedo; 3, hace falta saber cómo; 5, mata a quien lo trabaja sin cuidado (o con él).
- `valor`: texto breve, en la moneda o el trueque del mundo («una onza vale lo que una cabra», «se paga a peso de plata»).
- `descubrimiento` y `agotamiento`: el año del eje en que se descubrió o empezó a usarse y en que se agotó, si se saben. Casi siempre quedan vacíos y la antigüedad va en el texto. Si el calendario está por definir, quedan vacíos.

## Nombre
- Como lo llaman quienes lo trabajan, en la lengua común: «hierro de pantano», «sal negra», «piedra de humo». Con `generate_names.py` si el nombre lleva una palabra inventada.
- Los nombres que le dan otros pueblos, los sabios o los mercaderes van en `aliases`.
- Se enlaza cada vez que una nota lo nombra. Archivo en ASCII (`Sal_Negra.md`); H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, dónde se encuentra y por qué importa.
- **Datos clave:** la tabla completa. «Aspecto», en una línea; «Dónde se encuentra», sus yacimientos enlazados; «Valor», como en `valor`.
- **Cómo es:** su aspecto; lo que se siente al tocarlo, al olerlo o al golpearlo; cómo se comporta (dureza, peso, el fuego, el agua, el tiempo); cómo se reconoce (y cómo se distingue de lo que se le parece).
- **Dónde se encuentra:** sus yacimientos, enlazados (y en `yacimientos`); cómo se presenta (en vetas, en nódulos, en la arena de un río, en la piel de una bestia, en un pozo); las señales que lo delatan.
- **Cómo se obtiene y se trabaja:** cómo se saca (con qué, con qué riesgo, cuánto se tarda), cómo se trabaja (fundir, tallar, curtir, destilar, secar) y quién sabe hacerlo (un oficio, un gremio, un pueblo).
- **Usos:** para qué sirve; lo que se hace con él (los objetos que tienen nota, enlazados y en `objetos`); lo que no se puede hacer con él (sus límites naturales).
- **Propiedades extraordinarias** (solo si las tiene): qué hace, sus límites y su precio, según su `sistema`.
- **Riesgos:** lo que cuesta sacarlo y trabajarlo (el polvo, el fuego, los derrumbes, las afecciones, enlazadas) y usarlo. Si no tiene, en pocas palabras.
- **Comercio:** cuánto vale y por qué; quién lo compra y quién lo vende; por dónde viaja (sus rutas, enlazadas y en `rutas`); las falsificaciones y cómo se descubren.
- **Lo que se cree:** de 1 a 3 creencias, supersticiones o usos rituales (lo que espanta, lo que trae suerte, lo que no se toca con la mano izquierda), contadas como lo que creen quienes las siguen.
- **Historia:** cómo se descubrió o se empezó a usar; de 2 a 4 momentos decisivos (la fiebre de su hallazgo, la guerra por un yacimiento, su prohibición); y el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas, de quien lo saca, de quien lo vende o de quien lo teme.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para una lámina de espécimen: el material en bruto y, al lado, cómo queda trabajado; su color, su brillo y su textura; y lo que lo acompaña (la roca donde aparece, la herramienta que lo saca, una muestra cortada). Un recurso (el agua, el suelo), por su muestra o su fuente.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `naturaleza`, `rareza`, `situacion`, `peligrosidad`, `valor`, `descubrimiento` y `agotamiento`: ver arriba.
- Relaciones, solo con enlaces:
  - `yacimientos`: donde se encuentra o se saca (regiones, asentamientos, lugares como una mina o una cantera, ecosistemas); cada uno lo tiene en sus `recursos`;
  - `criaturas` de las que se obtiene: cada una lo tiene en sus `materiales`;
  - `plantas` de las que se obtiene: cada una lo tiene en sus `materiales`;
  - `objetos` que se hacen con él: cada uno lo tiene en sus `materiales`;
  - `sistemas` que alimenta, guarda o frena: cada uno lo tiene en sus `materiales`;
  - `facciones` que lo sacan, lo controlan o lo comercian;
  - `pueblos` que lo trabajan, lo veneran o dependen de él;
  - `rutas` por las que viaja: cada una lo tiene en sus `mercancias`;
  - `afecciones` que causa (o que cura);
  - `fenomenos` que lo crean, lo cambian o lo envenenan;
  - `relacionados`: otros materiales con los que va de la mano (el mineral y su ganga, los dos metales de una aleación); recíproca;
  - `eventos` en torno a él (su hallazgo, la guerra por su yacimiento);
  - `era` en que se descubrió o empezó a usarse.
- `fuentes`: los textos, mapas o relatos de donde se sabe (imprescindible en uno legendario).
- `relevancia`: 5 el material del que depende el mundo o su conflicto central; 4 el que mueve la economía de una región; 3 el conocido en su comarca; 2 uno local; 1 uno que conocen pocos.
- `ultima_revision` sin comillas.

## Coherencia
- **La tierra y la vida del mundo:** sus yacimientos encajan con la geografía y el clima de donde están (lo que sale del fondo de un pantano no aparece en un desierto); lo que sale de un ser vivo, con lo que dicen de él su criatura o su planta.
- **La Ficha:** la tecnología decide qué se puede sacar y trabajar; los poderes, si puede tener propiedades extraordinarias; el conflicto central, qué le hace o qué hace él.
- **Lo que ya existe:** las notas que ya lo nombran (como enlace pendiente: una región en sus `recursos`, una criatura en sus `materiales`, un sistema que lo necesita) cuentan cosas de él. Léelas (`build_context.py`) y no las contradigas.
- **Reciprocidad:** sus yacimientos lo listan en `recursos`; sus criaturas, sus objetos y sus sistemas, en `materiales`; sus rutas, en `mercancias`; sus materiales relacionados, en `relacionados`.
- **Glosario:** registra su nombre (como material), sus otros nombres y los términos que nacen de él (el oficio de quien lo saca, una medida, una expresión).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 1 y 6 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- un yacimiento (`yacimientos`): una mina, una cantera, una salina (un `lugar` de categoría `explotacion`) o una región;
- quien lo saca o lo controla (`facciones`);
- lo que se hace con él (`objetos`);
- la criatura o la planta de la que sale (`criaturas`, `plantas`);
- la ruta por la que viaja (`rutas`);
- la afección que causa (`afecciones`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, el material guarda un secreto (el yacimiento se agota y nadie lo dice, no es lo que se cree, su poder tiene un precio escondido, sale de algo que no debería desenterrarse, lo que se vende como él es falso). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] Su aspecto, su tacto y su comportamiento son concretos, y se dice cómo se reconoce.
- [ ] Sus yacimientos son entidades y encajan con la geografía; los que ya existen lo listan en `recursos`.
- [ ] Sus propiedades extraordinarias, si las tiene, siguen las reglas de su sistema y los pilares de la Ficha.
- [ ] Uno legendario cuenta lo que dicen sus fuentes, sin afirmar que exista.
- [ ] Si no es un detalle y no lo pidió el usuario, quedó como `Confirmar: …`.
- [ ] Sus criaturas, sus objetos, sus sistemas, sus rutas y sus materiales relacionados que ya existen lo listan.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
