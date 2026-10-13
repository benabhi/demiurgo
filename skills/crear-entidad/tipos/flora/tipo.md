# Tipo: flora

Las plantas y los hongos del mundo: árboles, arbustos, hierbas, trepadoras, cultivos, hongos y plantas del agua, silvestres o cultivados, corrientes o extraordinarios. La ficha dice cómo es y cómo se reconoce, dónde y cómo crece, para qué sirve y qué se saca de ella, qué peligros tiene y con qué se confunde, quién la cultiva o la recoge, qué se cree de ella y su historia.

**No es flora:**
- lo que se saca de ella y se trabaja (`material`): la madera, la resina o la fibra son materiales, que la enlazan en sus `plantas`; el tinte o la tela ya hechos, objetos;
- el bosque, la selva o el prado donde crece (`lugar`, `region` o, más adelante, `ecosistema`): la planta los enlaza en su `habitat`;
- un ser que se mueve, caza o piensa (`criatura` o `especie`), aunque parezca vegetal: una planta que caza es flora si no se desplaza ni tiene voluntad propia; si la tiene, es una criatura;
- el remedio o el veneno ya preparados (`objeto`): la planta es la materia; el ungüento, un objeto.

## Identidad del tipo
- **Emoji del tipo:** 🌿, al inicio del H1: `# 🌿 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según lo que es (🌳 árbol, 🌲 conífera, 🌱 hierba, 🌾 cultivo, 🍄 hongo, 🌸 flor, 🍇 fruto, 🪷 planta del agua, 🥀 planta venenosa…).
- **Carpeta:** fija, `50_Naturaleza/Flora`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Flora.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, escalas, valores permitidos, recíprocas y relaciones). El motor puede crear flora desde cero.

**Hechos importantes:** una hierba de los caminos, un árbol de la comarca o un hongo de las cuevas son detalles que Claude puede inventar según la autonomía de la Ficha. Son importantes, y van como `Confirmar: …` en Preguntas Abiertas con la planta como primer enlace de la línea:
- una planta con propiedades extraordinarias (`naturaleza: sobrenatural`), o legendaria;
- el cultivo del que come una región entera, o la planta que cura (o causa) una afección de gran peso;
- la que responde al conflicto central (lo que crece donde nada crece, lo que lo frena).

Si el usuario pide la planta, el pedido es la aprobación.

## Una planta viva (lo más importante)
- **Es concreta:** su porte, sus hojas, sus flores o sus esporas, su olor, su sabor y lo que se siente al tocarla. Se reconoce por algo preciso, y se confunde con algo: la planta que cura y su gemela que mata es un clásico, y da historias.
- **Crece en algún sitio:** su `habitat` (las regiones, los bosques, las orillas, las cuevas) son entidades, y su clima y su suelo encajan con ellos. Tiene un ciclo: cuándo brota, florece, da fruto o se seca.
- **Sirve para algo, o no:** lo que se come, lo que cura (y cómo se prepara), lo que mata, lo que se saca de ella (sus `materiales`). Lo que cura funciona como cura en el mundo: a medias, con su precio, según lo que digan sus afecciones; nunca como una medicina moderna si la Ficha no tiene esa técnica.
- **Sus propiedades extraordinarias tienen reglas:** si hace algo fuera de lo natural, lo hace por un `sistema` del mundo, con sus límites y su precio. En un mundo sin poderes, no los tiene.
- **Responde al mundo:** quién la cultiva, quién la recoge y qué se cree de ella, y cómo la toca el conflicto central (lo que la marchita, lo que la cambia).

## Categoría, naturaleza, uso, situación y peligro
- `categoria`: `arbol`, `arbusto`, `hierba`, `trepadora`, `cultivo` (lo que se siembra para comer o para vender), `hongo`, `acuatica` u `otro`.
- `naturaleza`: `natural`, `sobrenatural` (tiene propiedades extraordinarias, según un sistema del mundo), `artificial` (alguien la creó o la cambió de forma que no se da sola) o `desconocida`.
- `uso`: el principal: `alimento`, `medicina`, `veneno`, `material` (madera, fibra, resina, tinte), `ritual`, `ornamental`, `ninguno` u `otro`.
- `situacion`: `comun`, `escasa`, `rara`, `legendaria` (solo la cuentan los relatos: puede que no exista; la ficha cuenta lo que dicen sus fuentes, en `fuentes` y en el texto, y la verdad, si se decide, va en un secreto) o `extinta`.
- `peligrosidad`, del 1 al 5: 1, inofensiva; 3, hay que saber tocarla; 5, mata a quien la toca, la come o la respira.
- `tamano`: texto breve («a la rodilla», «un árbol de cuarenta varas»).

## Nombre
- Como la llaman quienes la usan, en la lengua común: «hierba de los ahogados», «roble ceniciento», «seta de la sal». Con `generate_names.py` si el nombre lleva una palabra inventada.
- Los nombres que le dan otros pueblos, los sabios o los herbolarios van en `aliases`.
- Se enlaza cada vez que una nota la nombra. Archivo en ASCII (`Hierba_de_los_Ahogados.md`); H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, dónde crece y por qué importa.
- **Datos clave:** la tabla completa. «Dónde crece», su hábitat enlazado; «Peligro», con su número y lo que significa aquí («3: sus espinas dejan fiebre»).
- **Cómo es:** su porte; sus hojas y su tallo; sus flores, sus frutos o sus esporas; su olor y su sabor; cómo se reconoce (y con qué se confunde).
- **Dónde y cómo crece:** su hábitat (enlazado y en `habitat`); el clima y el suelo que necesita; su ciclo (cuándo brota, florece, da fruto, se seca); lo que vive con ella (las criaturas que la comen o la habitan, enlazadas y en `criaturas`).
- **Usos:** para qué sirve; lo que se saca de ella (sus materiales con nota, enlazados y en `materiales`); cómo se prepara (se seca, se hierve, se fermenta, se muele).
- **Peligros:** lo que hace daño (su veneno, sus espinas, sus esporas, las afecciones que causa, enlazadas y en `afecciones`) y con qué se confunde. Si no tiene, en pocas palabras.
- **Cultivo y recolección:** quién la cultiva o la recoge (un oficio, un pueblo, una orden); cómo y cuándo se recoge; cómo se conserva; cuánto vale.
- **Propiedades extraordinarias** (solo si las tiene): qué hace, sus límites y su precio, según su `sistema`.
- **Lo que se cree:** de 1 a 3 creencias, supersticiones o usos rituales (la flor que se deja a los muertos, el árbol que no se tala), contadas como lo que creen quienes las siguen.
- **Historia:** de dónde viene (siempre estuvo, la trajo alguien, nació del conflicto); de 2 a 4 momentos decisivos (la plaga que la arrasó, la cosecha que salvó a un pueblo); y el presente.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas, de quien la cultiva, de quien cura con ella o de quien la teme.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para una lámina botánica: la planta entera, sus detalles (la hoja, la flor, el fruto, la raíz o la semilla), un corte y su color. Un hongo, con su sombrero y su pie, y su lugar.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `naturaleza`, `uso`, `situacion`, `peligrosidad` y `tamano`: ver arriba.
- Relaciones, solo con enlaces:
  - `habitat`: dónde crece (regiones, lugares o ecosistemas); cada uno la tiene en su `flora`;
  - `materiales` que se sacan de ella (su madera, su resina, su fibra): cada uno la tiene en sus `plantas`;
  - `afecciones` que cura o que causa (el texto dice cuál);
  - `criaturas` que la comen, la polinizan o viven en ella;
  - `pueblos` que la cultivan o dependen de ella, y `creencias` que la tienen por sagrada o maldita;
  - `sistemas` que la usan o que explican lo que hace;
  - `fenomenos` que la crean, la cambian o la matan;
  - `parientes`: otras plantas de su familia o con las que se confunde; recíproca;
  - `eventos` en torno a ella (una plaga, una hambruna, un hallazgo);
  - `era` en que apareció o empezó a cultivarse.
- `fuentes`: los textos o relatos de donde se sabe (imprescindible en una legendaria).
- `relevancia`: 5 la planta de la que depende el mundo o su conflicto central; 4 la que alimenta, cura o envenena a una región entera; 3 la conocida en su comarca; 2 una local; 1 una que conocen pocos.
- `ultima_revision` sin comillas.

## Coherencia
- **La tierra del mundo:** su hábitat, su clima y su suelo encajan con los de las regiones y los lugares donde crece. Lo que crece en el desierto no crece en la ciénaga, salvo que eso sea lo extraordinario.
- **La Ficha:** la técnica decide cómo se cultiva y se prepara; los poderes, si puede tener propiedades extraordinarias; el conflicto central, qué le hace.
- **Lo que ya existe:** las notas que ya la nombran (como enlace pendiente: una afección que cura, un material que sale de ella, una costumbre que la usa) cuentan cosas de ella. Léelas (`build_context.py`) y no las contradigas.
- **Reciprocidad:** su hábitat la lista en `flora`; sus materiales, en `plantas`; sus parientes, en `parientes`.
- **Glosario:** registra su nombre (como flora), sus otros nombres y los términos que nacen de ella (el nombre de un preparado, de un oficio, de una fiesta de la cosecha).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 1 y 6 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- el sitio donde crece (`habitat`);
- lo que se saca de ella (`materiales`);
- la afección que cura o causa (`afecciones`);
- la criatura que vive de ella (`criaturas`);
- quien la cultiva o la recoge (un pueblo, una facción);
- la planta con la que se confunde (`parientes`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, la planta guarda un secreto (lo que cura también enferma, crece sobre algo enterrado, la trajo alguien a propósito, lo que se vende como ella es otra, su flor solo abre por una razón que nadie dice). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] Su aspecto es concreto y se dice cómo se reconoce y con qué se confunde.
- [ ] Su hábitat, su clima y su suelo encajan con los lugares donde crece, que la listan en `flora`.
- [ ] Lo que cura o envenena funciona como en el mundo (a medias, con su precio) y cuadra con sus afecciones.
- [ ] Sus propiedades extraordinarias, si las tiene, siguen las reglas de su sistema y los pilares de la Ficha.
- [ ] Si no es un detalle y no la pidió el usuario, quedó como `Confirmar: …`.
- [ ] Sus materiales y sus parientes que ya existen la listan.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
