# Tipo: criatura

Los seres vivos (o no tan vivos) que no forman pueblos: la fauna corriente, las bestias peligrosas, los monstruos, las aberraciones que deforma un fenómeno, los no muertos, los espíritus menores y los constructos. La ficha dice cómo es, dónde vive, cómo caza o se alimenta, qué puede hacer y qué la frena, cómo se reconoce su presencia, cómo se caza o se evita, qué se obtiene de ella y qué cree la gente.

**No es una criatura:**
- un pueblo con lengua y cultura (`especie`): una criatura puede ser astuta, pero no habla ni tiene costumbres que se transmitan;
- un dios o un espíritu mayor con culto (`deidad`);
- la fuerza que la crea o la transforma (`fenomeno`);
- un ejemplar famoso, con nombre propio e historia, de una criatura conocida (la loba que asoló un valle durante tres inviernos): es un `personaje`, que nombra su criatura en la ficha. Si es la única de su clase, sí es una criatura (`rara` o `legendaria`, y el texto dice que es única).

## Identidad del tipo
- **Emoji del tipo:** 🐺, al inicio del H1: `# 🐺 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según lo que es (🦌 presa, 🐍 reptil, 🦅 ave, 🕷️ alimaña, 🐟 acuática, 🦇 nocturna, 🐉 monstruo, 💀 no muerto, 👻 espíritu, 🗿 constructo…).
- **Carpeta:** según la `categoria`: `fauna` (animales corrientes, cazados o domesticados) va en `50_Naturaleza/Fauna`; `bestia`, `monstruo`, `aberracion`, `no_muerto`, `espiritu`, `constructo` y `otro` van en `50_Naturaleza/Criaturas_y_Monstruos`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Criatura.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, escalas, valores permitidos y relaciones). El motor puede crear criaturas desde cero.

**Hechos importantes:** la fauna y las bestias de una comarca son detalles que Claude puede inventar según la autonomía de la Ficha. Un monstruo que amenaza una región entera, o una criatura ligada al conflicto central que cambia lo que se sabe de él, es un hecho importante: va como `Confirmar: …` en Preguntas Abiertas, con la criatura como primer enlace de la línea.

## Cómo funciona (lo más importante)
Una criatura sin reglas es un comodín. Toda ficha deja claro:
- **lo que puede hacer** (sus sentidos, sus armas, sus capacidades extraordinarias) y **lo que la frena o la mata**: al menos una debilidad real y una creencia falsa sobre cómo vencerla;
- **cómo se reconoce su presencia** antes de verla: huellas, restos, sonidos, olores, el silencio de los demás animales;
- **algo que nadie entiende todavía:** un misterio deliberado, no un dato que falta.

Las reglas respetan los pilares de la Ficha:
- **Especies:** si la Ficha pide aprobación para las especies nuevas, una criatura nunca es un pueblo encubierto: si habla, razona y transmite costumbres, es una especie y se pregunta antes.
- **Poderes:** lo extraordinario que haga respeta las reglas y los límites de los poderes de la Ficha.
- **Tecnología:** un constructo solo existe si la Ficha lo permite.

## Fechas y situación
- `aparicion` y `extincion`: años del eje del calendario de referencia. `aparicion` solo si apareció en un momento conocido (con un fenómeno, tras una catástrofe); `extincion`, solo si ya no existe.
- **Si el calendario está por definir,** las fechas quedan vacías y el texto usa fechas relativas. No decidas el calendario: es un pilar (ver `referencias/pilares.md`).
- `situacion`: `comun`, `escasa`, `rara`, `legendaria` (solo se sabe de ella por relatos; quizá no exista) o `extinta`. `check_note.py` comprueba que encaje con sus fechas y el año actual.
- `peligrosidad`: del 1 al 5 (1, inofensiva; 3, mata a quien se descuida; 5, una amenaza para un pueblo entero).
- `naturaleza`, `tamano`, `dieta`, `sociabilidad` y `actividad`: ver el `modulo.json`.

## Nombre
- Muchas criaturas tienen un nombre descriptivo en la lengua común («el lobo de ceniza», «la garza ciega»); cada pueblo puede llamarla a su manera. Los otros nombres van en `aliases`.
- Para un nombre propio, genera candidatos con `generate_names.py`.
- Archivo en ASCII (`Lobo_de_Ceniza.md`). H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **completa**. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, dónde vive y por qué se teme o se busca.
- **Datos clave:** la tabla completa; "Lo que vale", lo que se obtiene de ella y lo que se paga.
- **Anatomía y aspecto:** el cuerpo, lo que la delata a simple vista, cómo se mueve y cómo suena y huele.
- **Comportamiento:** cómo vive (sola, en manada, en enjambre), cómo caza o se alimenta, qué hace ante las personas (huye, acecha, se acerca) y su ciclo de vida.
- **Capacidades y debilidades:** ver arriba.
- **Señales de su presencia:** de 2 a 4 señales concretas.
- **Cómo se trata con ella:** cómo se caza (y quién lo hace), cómo se evita y si se puede domesticar.
- **Lo que se obtiene de ella:** sus materiales y para qué sirven, y lo que se paga por ellos.
- **Lo que se sabe y lo que se cree:** lo comprobado frente a las supersticiones de cada pueblo.
- **Origen e historia:** su origen (natural, nacida de un fenómeno, creada por alguien), de 2 a 5 avistamientos o momentos decisivos y el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para un plano de cuerpo entero en su hábitat: su pose característica (acechando, posada, en marcha), su anatomía, lo que la delata, una referencia de tamaño, el hábitat y la luz. **Nada gráfico:** sin presas destrozadas ni sangre; su peligro se ve en su porte, en sus garras o en la huella que deja.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`: `fauna`, `bestia` (un animal peligroso, aunque natural), `monstruo` (fuera de lo natural, o de lo que se conoce), `aberracion` (deformada por un fenómeno, un poder o una afección), `no_muerto`, `espiritu` (sin culto: un aparecido, un genio de un lugar), `constructo` u `otro`.
- `situacion`, `peligrosidad`, `aparicion` y `extincion`: ver arriba.
- Relaciones, solo con enlaces:
  - `habitat`: las regiones y los lugares donde vive; cada uno la tiene en sus `criaturas`;
  - `fenomenos` que la crearon o la transforman: cada uno la tiene en sus `criaturas`;
  - `afecciones` que transmite o sufre: cada una la tiene en sus `criaturas`;
  - `parientes`: criaturas emparentadas (la variante de otro hábitat, la forma antigua); recíprocas;
  - `deidades` a las que sirve o con las que se la asocia: cada una la tiene en sus `criaturas`;
  - `creencias` que la veneran, la temen o la usan en sus ritos;
  - `materiales` que se obtienen de ella (su piel, su veneno, su hueso);
  - `cazadores`: quienes la cazan o la estudian, personas o facciones; su tipo va en el registro de enlaces pendientes;
  - `eventos`: ataques o avistamientos con nota propia;
  - `era` en que apareció.
- `relevancia`: 5 la criatura del conflicto central o una que amenaza al mundo; 4 una regional; 3 una que pesa en su comarca; 2 una menor; 1 la fauna corriente.
- `ultima_revision` sin comillas.

## Coherencia
- **La Ficha:** sus capacidades, su origen y su papel ante el conflicto central encajan con la Ficha (ver los pilares arriba). Si el conflicto central cambia a los seres vivos, sus criaturas lo muestran de forma concreta.
- **Lo que ya existe:** su hábitat, los fenómenos que la crearon, las afecciones que transmite y las notas que ya la nombran (como enlace pendiente) deben encajar con lo que dicen. Léelas (`build_context.py`).
- **Reciprocidad:** su hábitat, sus fenómenos, sus afecciones, sus deidades y sus parientes que ya existen la listan en su propiedad inversa.
- **Glosario:** registra su nombre (como criatura), sus otros nombres y los términos que nacen de ella (el nombre de sus cazadores, un material, una expresión).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 2 y 8 nuevos** (los que solo nombra esta nota), de al menos dos tipos. Buenos candidatos:
- el lugar donde más abunda o su guarida conocida (`habitat`);
- el fenómeno que la creó o la transforma (`fenomenos`);
- quien la caza o la estudia (`cazadores`);
- un material que se obtiene de ella (`materiales`);
- un ataque o un avistamiento recordado (`eventos`);
- una criatura emparentada (`parientes`).

## Secretos
Tirada real con `roll_dice.py 1d4`: con 4, la criatura guarda un secreto (no nace: alguien la hace; la manada obedece a algo que nadie ha visto; lo que se vende como su veneno es otra cosa; antes fue otra cosa, o alguien). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] La categoría la lleva a su carpeta.
- [ ] No es un pueblo encubierto: si la Ficha pide aprobación para las especies, no habla ni tiene cultura.
- [ ] Un monstruo que amenaza una región, o una criatura que cambia lo que se sabe del conflicto central, quedó como `Confirmar: …`.
- [ ] Tiene capacidades, una debilidad real, una creencia falsa sobre cómo vencerla, señales de su presencia y un misterio.
- [ ] La situación cuadra con sus fechas y con el año actual.
- [ ] Nada gráfico ni gratuito en la ficha ni en la imagen.
- [ ] Su hábitat, sus fenómenos, sus afecciones, sus deidades y sus parientes que ya existen la listan.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y hay entre 2 y 8 enlaces pendientes nuevos, todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
