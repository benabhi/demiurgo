# Tipo: idioma

Las lenguas del mundo y lo que se parece a ellas: idiomas, dialectos, jergas, lenguas francas, sistemas de escritura, lenguajes de señas y códigos. La ficha dice cómo suena, cómo se construye, cómo se escribe y quién la usa, y da un vocabulario y unas frases para que las demás notas hablen con su voz.

**No es un idioma:**
- la cultura que lo habla (`cultura`): el idioma se enlaza desde ella;
- un texto concreto escrito en él (`obra`).

## Identidad del tipo
- **Emoji del tipo:** 🗣️, al inicio del H1: `# 🗣️ Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (📜 lengua escrita y culta, 🤝 lengua de comercio, 🤫 jerga o código, ✋ señas, 🪶 lengua antigua…).
- **Carpeta:** fija, `30_Sociedad_y_Cultura/Idiomas_y_Escrituras`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Idioma.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, valores permitidos y relaciones). Lleva `crear_desde_cero: false`: el motor solo crea las lenguas que otra nota ya nombra como enlace pendiente (la lengua de una cultura, por ejemplo), nunca una de la nada.

## Sonido y nombres (lo más importante)
El idioma es la fuente del sonido de un pueblo: de él salen sus nombres de personas y lugares.
- **Fonética:** de dónde sale su sonido: la sonoridad de los nombres de la Ficha, el carácter de quienes lo hablan y, si existe, su lengua madre. Debe sonar distinto de los demás idiomas del mundo: léelos antes.
- **Patrones de nombres:** la sección lista las sílabas típicas (inicios, medios, finales) en el formato de los perfiles de nombres, para que se puedan copiar a un perfil.
- **Perfiles que alimenta:** las culturas que lo hablan basan su perfil (`Nombres_<Cultura>`) en esta sección.
  - Si una cultura que lo habla ya tiene perfil, **el idioma se adapta a ese perfil**: el perfil es del usuario, y los nombres que ya existen en el mundo salieron de él.
  - Si no lo tiene, el perfil se crea cuando se crea la cultura, a partir de esta sección.
- **Palabras inventadas:** el vocabulario, las frases y las citas usan la misma fonética. Para inventar palabras con su sonido, genera candidatos con `generate_names.py --profile <Cultura>` (el perfil de quien lo habla, o `Generico`) y elige o adapta.
- **Mundo inventado:** si la Ficha lo pide, nada de palabras, gramáticas ni alfabetos reales con otro nombre.

## Nombre
- El nombre de la lengua en la lengua de la bóveda ("ribereño", "la lengua del delta") y, en `aliases`, cómo la llaman sus hablantes en su propia lengua y cómo la llaman otros.
- Archivo en ASCII. H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué lengua es, quién la habla y cómo suena. No una lista de datos.
- **Datos clave:** la tabla completa; los hablantes, aproximados.
- **Cómo suena:** los sonidos más frecuentes, los que no tiene, el ritmo y el acento, y cómo la oye un forastero (dura, cantarina, susurrada…).
- **Patrones de nombres:** ver arriba; de 10 a 20 sílabas por línea.
- **Gramática esencial:** sin tratado: el orden de las palabras, cómo marca el número o el género, cómo expresa el respeto, y uno o dos rasgos que la hagan distinta (no tiene futuro, distingue lo visto de lo oído, cuenta en base doce…).
- **Escritura:** el sistema (alfabeto, silabario, glifos, nudos, ninguno), sobre qué se escribe, quién sabe hacerlo y cómo son los signos a la vista. Si no tiene escritura, dilo y explica cómo guardan la memoria.
- **Vocabulario básico:** de 10 a 15 palabras útiles para el resto del mundo (saludo, despedida, familia, agua, fuego, comida, muerte, extranjero, enemigo, hogar, la palabra para su propio pueblo…), con su significado y una nota si la tiene.
- **Frases comunes:** de 3 a 5, con su traducción: un saludo, un dicho, una maldición, una fórmula de respeto.
- **Dialectos y variantes:** de 1 a 3, con dónde se hablan y en qué se notan.
- **Uso social:** quién la habla y cuándo, para qué se usa (comercio, culto, poder, intimidad), su prestigio y qué pasa con quien la habla mal.
- **Historia:** orígenes, de 2 a 5 momentos decisivos (con fechas o relativos) y el presente.
- **Relación con el mundo, secretos y rumores, ganchos:** como en todo tipo.
- **Citas:** en la propia lengua, con su traducción debajo.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para una muestra caligráfica de su escritura: el soporte (pergamino, tablilla, piel, piedra), cómo son los signos, cómo se disponen, la tinta o la herramienta, y algún adorno. Si no tiene escritura, una muestra de cómo guardan la memoria (cordones anudados, marcas talladas).
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `clase`: `lengua`, `dialecto`, `jerga`, `lengua_franca`, `escritura` (un sistema de escritura sin lengua propia), `senas` o `codigo`.
- `situacion`: `viva`, `en_declive`, `amenazada`, `muerta`, `solo_ritual` o `desconocida`.
- `hablantes` y `escritura`: texto breve (`unas treinta mil personas`, `alfabeto de veinte signos`, `sin escritura`).
- `inicio` y `fin`: años del calendario, o vacíos si está por definir.
- Relaciones, solo con enlaces:
  - `culturas` y `especies` que la hablan; recíprocas con sus `idiomas`;
  - `regiones` donde se habla;
  - `lengua_madre` y `derivadas` (lenguas y dialectos que nacieron de ella); recíprocas;
  - `obras` escritas en ella.
- `relevancia`: 4 o 5 la lengua común o franca del foco; 3 la lengua de un pueblo; 2 un dialecto o una jerga.
- `ultima_revision` sin comillas.

## Coherencia
- **Perfiles de nombres:** encaja con los de las culturas que la hablan (ver arriba).
- **Nombres existentes:** los personajes, lugares y términos del Glosario de sus hablantes deben sonar a esta lengua. Si alguno desentona mucho, menciónalo en el informe; no lo cambies.
- **Reciprocidad:** cada cultura y especie que ya existe y la habla la lista en `idiomas`.
- **Glosario:** registra el nombre de la lengua, su nombre propio y las palabras que otras notas vayan a usar; no hace falta registrar todo el vocabulario.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 2 y 6 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota); con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- un dialecto o una lengua derivada (`derivadas`);
- su lengua madre, si no existe (`lengua_madre`);
- una obra escrita en ella (`obras`);
- la región donde más se habla (`regiones`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, la lengua guarda un secreto (una palabra que no debe pronunciarse, una escritura que oculta otra, un origen que sus hablantes niegan). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] El nombre es único en la bóveda y en el Glosario.
- [ ] Su fonética encaja con los perfiles de nombres de las culturas que la hablan.
- [ ] Vocabulario, frases y citas usan esa fonética, sin palabras reales disfrazadas.
- [ ] Las culturas y especies que la hablan y ya existen la listan en `idiomas`.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
