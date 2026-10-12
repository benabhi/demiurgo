# Tipo: cultura

Los pueblos y las culturas del mundo: grupos que comparten una forma de vivir, una identidad y una memoria. Una etnia, una tribu, un clan, una nación cultural, una diáspora, una subcultura. Es la ficha **cultural**: cómo viven, qué valoran, cómo se organizan y cómo se nombran. La biología va en su especie, que se enlaza.

**No es una cultura:**
- una especie (`especie`): los humanos son una especie; los pastores de las montañas, una cultura;
- un estado o un gobierno (`faccion`, o una `region` política): una cultura puede repartirse entre varios estados, y un estado reunir varias culturas;
- una religión (`creencia`): una cultura tiene creencias, pero no es una.

## Identidad del tipo
- **Emoji del tipo:** 🎭, al inicio del H1: `# 🎭 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (⛰️ pueblo de montaña, ⛵ marinos, 🐎 jinetes, 🔨 artesanos…).
- **Carpeta:** fija, `30_Sociedad_y_Cultura/Pueblos_y_Culturas`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Cultura.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, valores permitidos y relaciones). Lleva `crear_desde_cero: false`: un pueblo nuevo es un hecho importante, así que el motor solo crea las culturas que otra nota ya nombra como enlace pendiente, nunca una de la nada.

## Pueblos nuevos y la Ficha
- Un pueblo que nadie había mencionado es un hecho importante. Se crea si lo pide el usuario (su pedido basta) o para completar un enlace pendiente; en este último caso, si cambia el panorama del mundo (una civilización, un gran pueblo), su existencia va además como `Confirmar: …`.
- Respeta los pilares: la especie (y su regla de especies), la tecnología, los poderes y las reglas sobre referencias al mundo real (nada de culturas reales con otro nombre si la Ficha pide un mundo inventado).

## Perfil de nombres (obligatorio)
Cada cultura crea **su perfil de nombres**, que usarán todos sus personajes:
1. Si no existe la carpeta `00_Sistema/06_Generacion/Nombres`, ejecuta `setup_generation.py` de la skill `expandir-mundo`, que la crea y la registra.
2. Crea `00_Sistema/06_Generacion/Nombres/Nombres_<Cultura>.md` con el formato del perfil Genérico (`assets/nombres/Generico.md`): Inicios, Medios, Finales, Patrones, Patrones de apellido y Prohibido. Si ya existe, úsalo y no lo sobrescribas: es del usuario.
3. La sonoridad sale de la Ficha (sonoridad de los nombres), de su lengua si tiene ficha (copia las sílabas de su sección «Patrones de nombres») y del carácter del pueblo: duros o suaves, cortos o largos, con apóstrofes o sin ellos. Debe sonar distinta de los perfiles de las demás culturas: léelos antes.
4. Pruébalo con `generate_names.py --profile <Cultura> --count 10` (el script encuentra `Nombres_<Cultura>`). Si los nombres no suenan bien, ajusta las sílabas y vuelve a probar.
5. En la ficha: `perfil_nombres: Nombres_<Cultura>`, y la sección "Nombres" explica cómo se forman (nombre, apellido o linaje, apodos, títulos), con 3 o 4 ejemplos generados.

El nombre de la propia cultura puede salir de su perfil (cómo se llaman a sí mismos) y, en `aliases`, cómo los llaman los demás.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** quiénes son y qué los hace reconocibles. No una lista de datos.
- **Datos clave:** la tabla completa; la población, aproximada.
- **Identidad y valores:** cómo se ven, qué valoran, qué desprecian y sus tabúes. Es el corazón de la ficha: todo lo demás se explica desde aquí.
- **Estructura social:** familia y parentesco, quién manda y cómo, el papel de la edad, el género y el oficio, y qué pasa con los de fuera y los marginados.
- **Vida cotidiana:** vivienda, comida, vestimenta y un día corriente, concretos y visuales.
- **Ritos y festividades:** el nacimiento, el paso a la edad adulta, las uniones, la muerte y sus fiestas, con su fecha si existe el calendario de referencia (o el suyo propio).
- **Arte y expresión:** artesanías, música, relatos, símbolos y colores. Sus mitos y leyendas con nota propia, en `mitos`.
- **Creencias:** de 1 a 3 entradas con su enlace, y cuánto pesan en la vida diaria.
- **Oficios y economía:** qué hacen, qué producen, qué intercambian y qué les falta.
- **Guerra y conflicto:** cómo combaten, con qué, y cómo resuelven las disputas internas.
- **Nombres:** ver "Perfil de nombres".
- **Relación con otros pueblos:** aliados, rivales y el trato a los forasteros.
- **Historia:** orígenes, de 3 a 6 migraciones o momentos decisivos (con fechas o relativos) y el presente.
- **Diversidad interna:** de 2 a 4 entradas: ramas, generaciones, disidentes, diferencias entre regiones. Ninguna cultura es un bloque.
- **Estereotipos:** lo que dicen de ellos, lo que ellos dicen de los demás y lo que hay de cierto.
- **Relación con el mundo, secretos y rumores, ganchos y citas:** como en todo tipo. Las citas, con la voz de la cultura (un proverbio, un dicho, una canción).
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para un plano medio de tres miembros con su atuendo tradicional: qué están haciendo (una actividad típica), quiénes son los tres (edades y papeles distintos), el atuendo y los adornos, un objeto o una artesanía de la cultura, y su entorno.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `modo_de_vida`: `sedentario`, `nomada`, `seminomada` o `disperso` (una diáspora repartida entre otros pueblos).
- `situacion`: `prospera`, `estable`, `en_declive`, `amenazada`, `desaparecida` o `desconocida`.
- `poblacion`: texto breve (`unas veinte mil almas`). `inicio` y `fin`: años del calendario, o vacíos si está por definir.
- `perfil_nombres`: el nombre del perfil (`Nombres_<Cultura>`), sin enlace.
- Relaciones, solo con enlaces:
  - `especie`: su especie; recíproca con `culturas` de la especie;
  - `territorios`: regiones y lugares donde vive; recíproca con `pueblos` de la región;
  - `idiomas` (recíproca con `culturas` del idioma) y `creencias`;
  - `calendario`: el suyo, si cuenta el tiempo a su manera (recíproca con `culturas` del calendario); vacío si usa el de referencia;
  - `cultura_madre` y `ramas`: de qué cultura viene y qué culturas nacieron de ella; recíprocas;
  - `aliados`: otras culturas; recíproca, porque una alianza es de las dos;
  - `rivales`: los pueblos que este tiene por rivales; no se espeja sola: si la rivalidad es mutua, va también en la otra, y si es de un solo lado, solo en esta (ver «Relaciones» en `SKILL.md`);
  - `instituciones`: sus gobiernos, órdenes o gremios (facciones, que la tienen en sus `culturas`);
  - `figuras`: sus miembros más notables (no hace falta listar a todos los personajes de la cultura);
  - `mitos` que cuenta: cada uno la tiene en sus `culturas`.
- `relevancia`: 5 si es el pueblo central del foco; 3 o 4 si es importante; 2 si es marginal.
- `ultima_revision` sin comillas.

## Coherencia
- **Especie:** su anatomía, su longevidad y su ciclo vital marcan la cultura (una especie que vive siglos no tiene la prisa de una que vive cuarenta años). Lee la ficha de la especie antes de escribir.
- **Personajes existentes:** si ya hay personajes de esta cultura, sus costumbres, nombres y oficios deben encajar. Léelos (`build_context.py`).
- **Reciprocidad:** la especie la lista en `culturas`, cada territorio que exista la lista en `pueblos` y sus aliados que existan, en `aliados`. Sus rivales, no.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 3 y 10 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- su lengua (`idiomas`);
- su fe (`creencias`);
- su tierra (`territorios`);
- su gobierno o una institución (`instituciones`);
- una figura notable (`figuras`);
- un pueblo rival o una rama (`rivales`, `ramas`);
- su propia cuenta del tiempo (`calendario`), solo si existe el calendario de referencia.

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, la cultura guarda un secreto (un crimen de su historia, un origen distinto del que cuentan, una lealtad oculta). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] El nombre es único en la bóveda y en el Glosario.
- [ ] El perfil `Nombres_<Cultura>` existe, se probó con `generate_names.py` y la sección "Nombres" tiene ejemplos.
- [ ] Encaja con su especie, con los pilares de la Ficha y con los personajes que ya existen.
- [ ] La especie y los territorios que existen la listan en `culturas` y `pueblos`.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
- [ ] Si la creó el motor y es un pueblo nuevo de peso para el canon, su existencia va como `Confirmar: …`.
