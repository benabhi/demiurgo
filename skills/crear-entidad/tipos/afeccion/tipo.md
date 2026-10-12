# Tipo: afeccion

Lo que enferma, cambia o somete a los seres vivos: enfermedades y fiebres, plagas que arrasan pueblos, cosechas o ganados, mutaciones que provoca un fenómeno o una sustancia, corrupciones del cuerpo o del espíritu, maldiciones, adicciones y locuras. La ficha dice cómo se reconoce, cómo se transmite, cómo avanza, qué la frena, qué remedios se creen y cuáles funcionan, y qué hace la gente con los enfermos.

**No es una afección:**
- la fuerza que la provoca (`fenomeno`): una tormenta que enloquece es un fenómeno; la locura que deja en quien la sufre, una afección;
- un ser que la transmite (`criatura`) o una sustancia que la cura (`material`);
- una herida o una cicatriz de alguien: eso va en la ficha de su personaje.

## Identidad del tipo
- **Emoji del tipo:** 🦠, al inicio del H1: `# 🦠 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según cómo se manifiesta (🤒 fiebre, 🫁 tos, 🧬 mutación, 🕷️ corrupción, ☠️ mortal, 🌾 plaga de cosechas, 🩸 maldición, 🍷 adicción, 🌀 locura…).
- **Carpeta:** `50_Naturaleza/Enfermedades_y_Afecciones`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Afeccion.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, escalas, valores permitidos y relaciones). El motor puede crear afecciones desde cero.

**Hechos importantes:** un mal local (una fiebre de una aldea, una adicción de un puerto) es un detalle que Claude puede inventar según la autonomía de la Ficha. Una plaga regional o mundial que no está en el canon, o una afección ligada al conflicto central que cambia lo que se sabe de él, es un hecho importante: va como `Confirmar: …` en Preguntas Abiertas, enlazando su nota.

## Cómo funciona (lo más importante)
Una afección sin reglas es un comodín. Toda ficha deja claro:
- **cómo se reconoce:** la primera señal y cómo avanza, por fases (de 2 a 5), con lo que dura cada una;
- **cómo se transmite** (`contagio`) y quién corre más riesgo;
- **lo que la frena:** al menos un remedio que funciona a medias y a un precio, y uno que es falso aunque se crea;
- **algo que nadie entiende todavía:** un misterio deliberado, no un dato que falta.

Las reglas respetan los pilares de la Ficha. Con tecnología antigua, nadie conoce lo que la provoca como lo conoceríamos hoy: se habla de humores, de aires, de castigos o de la sangre, y los remedios son los de su época. Una corrupción o una maldición sobrenatural es un poder extraordinario: respeta sus reglas y sus límites.

## Fechas y prevalencia
- `aparicion` y `erradicacion`: años del eje del calendario de referencia; `erradicacion` solo si ya no existe.
- **Si el calendario está por definir,** las fechas quedan vacías y el texto usa fechas relativas («desde la última gran sequía»). No decidas el calendario: es un pilar (ver `referencias/pilares.md`).
- `prevalencia`: `esporadica` (casos sueltos), `endemica` (siempre presente en una zona), `epidemica` (se extiende ahora), `latente` (sin casos, pero no ha desaparecido) o `erradicada` (ya no existe). `check_note.py` comprueba que encaje con sus fechas y el año actual.
- `gravedad`: del 1 al 5 (1, una molestia; 3, deja secuelas o mata a algunos; 5, casi siempre mortal o lo cambia todo en quien la sufre).
- `naturaleza`: `natural`, `sobrenatural`, `artificial` (provocada a propósito) o `desconocida`. `contagio`: cómo pasa de un ser a otro.

## Nombre
- Muchas afecciones tienen un nombre descriptivo en la lengua común («la fiebre del pantano», «la tos negra», «la piel de ceniza»); cada pueblo puede llamarla a su manera. Los otros nombres van en `aliases`.
- Para un nombre propio, genera candidatos con `generate_names.py`.
- Archivo en ASCII (`Tos_Negra.md`). H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **completa**. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, cómo se reconoce y por qué se teme.
- **Datos clave:** la tabla completa.
- **Síntomas y fases:** de 2 a 5 filas, de la primera señal al final (la cura, las secuelas o la muerte). Concreto, pero sin recrearse: la crudeza adulta sirve al mundo, nunca es gratuita.
- **Cómo se transmite:** el contagio, quién corre más riesgo y cómo se evita.
- **Efectos a largo plazo:** en quien sobrevive (secuelas, marcas, cambios) y en las familias y los pueblos (huérfanos, aldeas vacías, oficios que desaparecen).
- **Remedios:** lo que funciona, lo que no aunque se crea, y lo que cuesta curarse.
- **Lo que se sabe y lo que se cree:** lo comprobado frente a las teorías, las supersticiones y las explicaciones de cada fe.
- **Estigma y sociedad:** cómo se trata a los enfermos (se los aparta, se los cuida, se los teme), las costumbres y leyes que nacieron por ella y quién gana con ella (quien vende el remedio, quien se queda las tierras de los muertos).
- **Historia:** su origen según lo que se sabe, de 2 a 5 brotes o momentos decisivos (con fechas o relativos) y el presente.
- **Casos notables:** de 1 a 3 personas que la sufren o la sufrieron, con su enlace (en `afectados`).
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para una lámina de estudio, como la de un tratado de su época: el sujeto de la lámina (una mano, un rostro de perfil, una hoja de trigo, un animal), las señales visibles, las fases en pequeño, los remedios o los útiles de quien la trata alrededor, sus colores y el tono. **Nada gráfico:** ni heridas abiertas ni sufrimiento explícito; la afección se ve por sus señales.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`: `enfermedad`, `plaga` (lo que arrasa pueblos, cosechas o ganados a la vez), `mutacion`, `corrupcion` (del cuerpo, de la mente o del espíritu, de origen sobrenatural), `maldicion` (la echó alguien, con sus reglas), `adiccion`, `locura` u `otro`.
- `naturaleza`, `contagio`, `prevalencia`, `gravedad`, `aparicion` y `erradicacion`: ver arriba.
- Relaciones, solo con enlaces:
  - `fenomenos` que la provocan: cada fenómeno la tiene en sus `afecciones`;
  - `especies` que la sufren (las que solo la sufre una, o a las que afecta de otro modo): cada especie la tiene en sus `afecciones`;
  - `criaturas` que la transmiten o la sufren: cada una la tiene en sus `afecciones`;
  - `afectados`, los casos notables: cada uno la tiene en sus `afecciones` (no hace falta que la nota liste a todos los que la tienen);
  - `zonas` donde se da (regiones o asentamientos);
  - `sanadores`: quienes la tratan o la estudian, personas o facciones (una orden de hospitaleros, un curandero); su tipo va en su propiedad o en el registro de enlaces pendientes;
  - `creencias` que la explican, la curan o la castigan;
  - `eventos`: sus brotes con nota propia (una gran plaga es un evento);
  - `era` en que apareció.
- `relevancia`: 5 la afección del conflicto central o una plaga mundial; 4 una regional; 3 una que pesa en su comarca; 2 una menor; 1 una anécdota.
- `ultima_revision` sin comillas.

## Coherencia
- **La Ficha:** su causa, sus remedios y su papel ante el conflicto central encajan con la Ficha y con su tecnología. Si el conflicto central daña a los seres vivos, sus afecciones lo dicen de forma concreta.
- **Lo que ya existe:** los fenómenos que la provocan, las especies y las personas que la sufren, y las notas que ya la nombran (como enlace pendiente) deben encajar con lo que dicen. Léelas (`build_context.py`).
- **Reciprocidad:** sus fenómenos, especies y afectados que ya existen la listan en sus `afecciones`.
- **Glosario:** registra su nombre (como afección), sus otros nombres y los términos que nacen de ella (el nombre de los enfermos, un remedio, un oficio).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 2 y 8 nuevos** (los que solo nombra esta nota), de al menos dos tipos. Buenos candidatos:
- el fenómeno o la criatura que la provoca o la transmite (`fenomenos`, `criaturas`);
- un caso notable (`afectados`);
- quien la trata (`sanadores`) y la fe que la explica o la castiga (`creencias`);
- la zona donde más golpea (`zonas`);
- un brote recordado (`eventos`).

## Secretos
Tirada real con `roll_dice.py 1d4`: con 4, la afección guarda un secreto (alguien la provocó a propósito, el remedio que se vende la empeora, no es una enfermedad sino otra cosa, los que la sufren cambian hacia algo). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] Una plaga regional o mundial que no estaba en el canon, o una afección que cambia lo que se sabe del conflicto central, quedó como `Confirmar: …`.
- [ ] Tiene fases, una forma de contagio, un remedio a medias, uno falso y un misterio.
- [ ] La prevalencia cuadra con sus fechas y con el año actual.
- [ ] Nada gráfico ni gratuito en la ficha ni en la imagen.
- [ ] Sus fenómenos, especies y afectados que ya existen la listan en sus `afecciones`.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y hay entre 2 y 8 enlaces pendientes nuevos, todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
