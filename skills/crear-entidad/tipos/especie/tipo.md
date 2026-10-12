# Tipo: especie

Las especies inteligentes del mundo: seres con conciencia y capacidad de formar culturas, sean biológicos, sobrenaturales o artificiales (una especie de constructos conscientes, por ejemplo). Es la ficha **biológica**: cómo es el cuerpo, cuánto vive, qué percibe, cómo nace y muere. Lo cultural (costumbres, gobierno, arte) va en sus culturas, que se enlazan.

**No es una especie:**
- un animal o un monstruo sin cultura propia (`criatura`);
- un pueblo o una etnia de una especie (`cultura`): los humanos son una especie; los pueblos de las montañas, una cultura;
- un individuo extraordinario (`personaje`) ni un dios (`deidad`).

## Identidad del tipo
- **Emoji del tipo:** 🧬, al inicio del H1: `# 🧬 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (🧑 humanos, 🌿 un pueblo del bosque, 🪨 seres de piedra, ⚙️ constructos…).
- **Carpeta:** fija, `50_Naturaleza/Especies_Inteligentes`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Especie.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, escalas, valores permitidos y relaciones). Lleva `crear_desde_cero: false`: el motor de generación nunca inventa una especie por su cuenta; solo crea las que ya nombra el canon.

## Especies y la Ficha (lo más importante)
Las especies son pilares del mundo. Antes de crear una, lee la regla de especies de la Ficha y de `CLAUDE.md`:
- **Una sola especie inteligente:** no se crea ninguna otra, nunca; la diversidad es cultural. Este módulo solo describe la que existe. Si el usuario pide otra, avísale de que contradice la Ficha y no la crees: cambiar ese pilar es una decisión suya, en la Ficha.
- **Otras especies, con aprobación:** se crea sin preguntar solo si la nombra la Ficha o una nota `canon`. Si no:
  - **Si la pide el usuario** (invocando `crear-entidad`): antes de escribir nada, pregúntale con AskUserQuestion si la aprueba, por ejemplo «La Ficha pide aprobación para especies nuevas: ¿existen los <Nombre> en <Mundo>?». Es una decisión real del mundo, de las pocas que se preguntan. Las opciones:
    - **«Sí, apruébala»:** créala y añade una línea al Registro de Canon (`| <fecha> | [[<Nombre>]] | Nueva especie aprobada | Pedido del usuario |`);
    - **«No, déjala como propuesta»:** no la crees; anótala como `Confirmar` (abajo).
  - **Sin nadie a quien preguntar** (el motor, el modo semilla, un enlace en un borrador): no la crees. Anota en Preguntas Abiertas `- [ ] Confirmar: existe la especie [[Nombre]] (<qué se sabe de ella y dónde aparece>)`, detente y dilo en el informe. La línea `Confirmar` bloquea esa referencia en el motor hasta que el usuario decida.
- **Sin humanos:** ninguna biología, costumbre ni expresión humana por defecto.

## Longevidad y madurez (números)
- `longevidad`: años que vive un miembro típico (`80`). `madurez`: edad a la que es adulto (`16`). Números del calendario de años, no texto.
- El auditor las usa para revisar a los personajes: avisa si uno tiene una edad imposible para su especie o si fue padre antes de la madurez.
- Si la especie no envejece, deja `longevidad` vacía y explícalo en el cuerpo.
- Si el mundo tiene otras especies con fichas, compáralas: las cifras deben tener sentido entre sí.

## Nombre
- El nombre común de la especie en la lengua de la bóveda ("humanos") y, en `aliases`, cómo se llaman a sí mismos y cómo las llaman otros pueblos.
- Para un nombre inventado, genera candidatos con `generate_names.py`.
- Archivo en ASCII (`Humanos.md`). H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es y qué la distingue. No una lista de datos.
- **Datos clave:** la tabla completa; longevidad y madurez, con las mismas cifras que el frontmatter.
- **Anatomía:** concreta y visual: cuerpo, rostro, cobertura (piel, pelo, escamas…), variaciones dentro de la especie y lo que la delata a simple vista. Las variaciones (tallas, colores, subgrupos) van aquí; no son especies nuevas salvo que la Ficha lo diga.
- **Sentidos y capacidades:** lo que percibe y puede hacer mejor o peor que otras especies, con sus límites y debilidades, y lo que necesita (alimento, descanso, entorno). Las capacidades extraordinarias respetan las reglas de poderes de la Ficha.
- **Ciclo vital:** nacimiento y crianza, madurez, vejez, la muerte y qué se hace con sus muertos.
- **Psicología y rasgos comunes:** tendencias, no un molde. Cada miembro es un individuo, y la sección "Variación individual" lo deja claro; las diferencias de costumbres van en sus culturas.
- **Culturas y pueblos:** de 1 a 4 entradas con su enlace y una línea que las defina.
- **Relación con otras especies:** con quién convive, con quién choca y si hay mestizaje (y cómo se ve).
- **Origen:** lo que cuentan sus mitos frente a lo que se sabe. La verdad oculta, si la hay, va a un secreto.
- **Distribución y situación:** dónde vive (con enlaces a regiones), cuántos son y cómo le va.
- **Prejuicios y estereotipos:** lo que dicen de ella, lo que ella dice de los demás y lo que hay de cierto. Es una fuente de conflictos y ganchos.
- **Relación con el mundo, secretos y rumores, ganchos y citas:** como en todo tipo.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para una figura de cuerpo entero de un miembro **típico**, no de un individuo concreto: la silueta y la talla, la cobertura y el color, los rasgos que la delatan, el atuendo habitual de sus culturas (si lo hay) y su hábitat de fondo.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `naturaleza`: `natural`, `sobrenatural`, `artificial` o `desconocida`.
- `situacion`: `prospera`, `estable`, `en_declive`, `amenazada`, `extinta` o `desconocida`.
- `longevidad` y `madurez`: números (ver arriba).
- `tamano` y `poblacion`: texto breve (`algo más bajos que un humano`, `unos pocos miles`).
- Relaciones, solo con enlaces:
  - `regiones`: donde vive; recíproca con `especies` de la región;
  - `culturas`: los pueblos que forma; recíproca con `especie` de la cultura;
  - `idiomas` (recíproca con `especies` del idioma) y `creencias` propios de la especie, si los hay;
  - `relacionadas`: especies emparentadas; recíproca;
  - `afecciones` propias de la especie: cada una la tiene en sus `especies`.
- `relevancia`: 5 la especie dominante o central del mundo; 3 o 4 las demás; 2 una especie rara o marginal.
- `ultima_revision` sin comillas.

## Coherencia
- **Pilares:** la regla de especies (arriba), la tecnología y los poderes de la Ficha.
- **Personajes existentes:** si ya hay personajes de esta especie, su edad, su aspecto y su historia deben encajar con lo que dice la ficha. Léelos antes de escribir (`build_context.py`).
- **Regiones:** cada región donde vive que ya exista la lista en `especies` (reciprocidad).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 3 y 8 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- un pueblo o una cultura de la especie (`culturas`);
- su tierra de origen o donde más abunda (`regiones`);
- su lengua propia (`idiomas`), si la tiene;
- una fe propia (`creencias`);
- una afección que solo la sufre ella (`afecciones`).

No nombres especies nuevas en `relacionadas` si la Ficha pide aprobación para ellas: serían especies inventadas.

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, la especie guarda un secreto (su verdadero origen, una capacidad que oculta, lo que le pasó a una rama perdida). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza. Si el secreto cambia un pilar del mundo, además va como `Confirmar: …`.

## Comprobaciones antes de escribir
- [ ] La especie está permitida: la nombra la Ficha o una nota `canon`, o el usuario la aprobó al preguntarle (y quedó en el Registro de Canon).
- [ ] El nombre es único en la bóveda y en el Glosario.
- [ ] `longevidad` y `madurez` son números coherentes con los personajes que ya existen.
- [ ] Las regiones donde vive que ya existen la listan en `especies`.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
