# Tipo: calendario

Cómo se cuenta el tiempo en el mundo: desde qué hecho se cuentan los años, cómo se escriben, qué meses, semanas, estaciones y festividades tiene el año, y quién lo usa. Las fechas de todas las demás notas se escriben con sus nombres.

**No es un calendario:**
- un periodo del pasado (`era`): una era se enlaza desde el calendario que la cuenta;
- el hecho que marca el año 0 (`evento`), que el calendario enlaza;
- una festividad con sus ritos y su historia (`costumbre`): el calendario solo dice cuándo cae.

## Identidad del tipo
- **Emoji del tipo:** 📅, al inicio del H1: `# 📅 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (☀️ solar, 🌙 lunar, ⭐ guiado por un astro, 🌾 de las labores del campo, 🕯️ ritual, 📜 erudito…).
- **Carpeta:** fija, `40_Historia/Eras_y_Periodos`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Calendario.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, valores permitidos y relaciones). Lleva `crear_desde_cero: false`: el motor solo crea los calendarios que otra nota ya nombra como enlace pendiente (el de una cultura, por ejemplo), nunca uno de la nada, y nunca el de referencia.

## El calendario de referencia (lo más importante)
Es el **eje de la Ficha**: los años de todas las propiedades de fecha (`nacimiento`, `inicio`…) son años de este calendario. Solo hay uno por mundo: `referencia: true` y `ano_cero: 0`.
- **El año 0 y el año actual son un pilar de la Ficha** (el calendario y el año actual, o «Presente y calendario» en las Fichas antiguas).
  - Si la Ficha ya los define, el calendario los respeta tal cual: su año 0 es el hecho de la Ficha, sus años se escriben como dice la Ficha y su año actual es el de la Ficha.
  - Si están **por definir**, no los decidas: pregúntale al usuario antes de escribir, salvo que su pedido ya lo diga. Una sola llamada a AskUserQuestion con tres preguntas, cada una con 2 o 3 opciones concretas sacadas de la Ficha (la recomendada primero, con «(Recomendado)»):
    1. **El año 0 y cómo se escriben los años:** el hecho que lo marca (el gran desastre, una fundación, la llegada a la tierra del foco…) con su sufijo y su significado: `412 UE (Último Encendido)`.
    2. **El presente:** en qué año está, con números concretos y su sentido: decenas de años (el hecho es memoria viva), cientos (es historia) o miles (es casi leyenda).
    3. **La forma del año:** por ejemplo, una duración parecida a la nuestra con meses y semana propios, un año lunar, o algo singular (días fuera de los meses, un mes que no se nombra). Añade «(Recomendado)» a la que mejor encaje con el mundo.
  - Con la respuesta, **resuelve el pilar** siguiendo `referencias/pilares.md`. En el calendario:
    - en la Ficha, la línea «Calendario» dice el hecho del año 0, cómo se escriben los años (también los anteriores) y enlaza esta nota; la línea «Año actual» lleva el número. En una Ficha antigua, la línea «Presente y calendario» se sustituye por esas dos líneas. Pon el año también en la propiedad `ano_actual` del frontmatter de la Ficha (añádela si no está);
    - en `CLAUDE.md`, las dos reglas: `- Calendario: <lo decidido>. Las fechas se guardan como número de años respecto al año 0 (negativas si son anteriores).` y `- El presente es el año <n> del calendario: edades y fechas se calculan desde ahí.`
  - **En el motor** (`expandir-mundo`), nunca: el calendario de referencia lo pide siempre el usuario. Si el selector propone crearlo, vuelve a ejecutarlo con `--skip <referencia>`.
- **Los detalles** (los nombres de los meses y los días, las estaciones, las festividades, cómo se mide la hora) no son el pilar: los inventa Claude según la autonomía de la Ficha y los lista en el informe.

## Otros calendarios
Los de un pueblo, una fe o una institución que cuenta el tiempo a su manera: `referencia: false`.
- **Solo si existe el de referencia:** sin él, su año 0 no tendría con qué compararse. Si no existe, propón crear antes el de referencia; en el motor, vuelve a ejecutar el selector con `--skip <enlace>`.
- **`ano_cero`:** el año del eje en que empieza su cuenta, negativo si es anterior al año 0 del eje. Si su año 0 es el año -340 del eje, `ano_cero: -340`, y el año 412 del eje es su año 752.
- Suele tener la misma duración del año que el de referencia (es el mismo cielo), pero no los mismos nombres, ni el mismo inicio del año, ni la misma cuenta. Puede durar distinto si su base es otra (un año lunar).
- Las culturas que lo usan lo tienen en su `calendario`.

## Nombre
- En la lengua de la bóveda ("Cuenta del Último Encendido", "Calendario de los ribereños") y, en `aliases`, cómo lo llaman quienes lo usan en su propia lengua.
- Archivo en ASCII. H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué calendario es, quién lo usa y desde qué hecho cuenta los años.
- **Datos clave:** la tabla completa. «Días del año» es la suma de los meses; «Año actual», en este calendario.
- **Cómo se cuentan los años:** el hecho del año 0, cómo se escriben los años anteriores, cuándo empieza el año (una fecha, un fenómeno, una fiesta) y otras formas de contar que convivan (por reinados, por ciclos, años con nombre propio).
- **Las tablas las leen los scripts** (`world_calendar.py`, `check_note.py`), así que respeta sus columnas:
  - **Meses:** una fila por mes, en orden. `Días` es un número entero y `Estación`, el nombre de una estación de la tabla de estaciones. Los nombres no se repiten. Los días que quedan fuera de los meses (días intercalados, de duelo o de fiesta) van como un «mes» más, con su nombre y sus días.
  - **Semana:** una fila por día. Si no hay semana, sustituye la tabla por un párrafo que diga cómo se agrupan los días (por decenas, por fases de la luna, por días de mercado).
  - **Estaciones:** `Desde` y `Hasta` son nombres de meses de la tabla de meses. Si el mundo no tiene estaciones, un párrafo que explique por qué.
  - **Festividades:** de 3 a 6. `Fecha` es «15 de <Mes>» (el script la valida) o una regla si es movible («la primera luna llena de <Mes>»). Cada festividad es una entidad: va enlazada en la tabla y en `festividades`, a su nota o como enlace pendiente de tipo `costumbre`.
- **El día y la noche:** las partes del día, cómo se mide la hora y el astro o el fenómeno que guía el calendario. Respeta la tecnología de la Ficha: sin relojes mecánicos si no los hay (velas marcadas, campanas, relojes de agua o de sol).
- **Historia:** orígenes, de 2 a 5 momentos decisivos (reformas, días perdidos, disputas) y el presente.
- **Uso social:** quién lo usa y para qué (las cosechas, los ritos, los impuestos), quién lo guarda o lo corrige, y los calendarios rivales.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para una rueda del calendario: el soporte (disco de piedra, placa de bronce, tabla pintada, tapiz), cómo se dividen los meses, cómo se ven las estaciones, qué hay en el centro (el astro, el hecho del año 0) y algún detalle (las fiestas marcadas, los días fuera de los meses como un anillo aparte).
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `referencia`: `true` solo en el calendario de referencia; `false` en los demás.
- `ano_cero`: `0` en el de referencia; en los demás, el año del eje en que empieza su cuenta.
- `sufijo` y `sufijo_negativo`: cómo se escriben los años desde el año 0 y antes de él (`UE` y `AUE`: «412 UE», «45 AUE»). Si no tiene sufijo para los anteriores, se escriben con signo menos.
- `base`: `solar`, `lunar`, `lunisolar`, `estacional` (lo marcan la naturaleza o un fenómeno, no el cielo), `astral` (un astro raro) u `otra`.
- `inicio` y `fin`: años del eje desde los que se usa y en que dejó de usarse (vacío si sigue en uso).
- Relaciones, solo con enlaces:
  - `culturas` que lo usan (recíproca con su `calendario`) y `regiones` donde rige;
  - `evento_cero`: el hecho que marca su año 0;
  - `eras` que cuenta o que lo marcaron, y `festividades` con nota propia;
  - `guardianes`: quienes lo guardan o lo corrigen (una orden, un templo, un gremio);
  - `calendario_base` y `derivados`: de qué calendario nació y cuáles nacieron de él; recíprocas.
- `relevancia`: 5 el de referencia; 3 el de un pueblo o una fe; 2 uno marginal o en desuso.
- `ultima_revision` sin comillas.

## Fechas en el resto del mundo
Cuando existe el calendario de referencia:
- Las propiedades de fecha siguen siendo **números del eje** (`nacimiento: 380`).
- En el texto, las fechas se escriben **con sus nombres**: «el 15 de Siega de 412 UE», o solo el año, «412 UE». `world_calendar.py` lo muestra y convierte años entre calendarios.
- **`fecha_exacta`** (en los tipos que la tienen, como el personaje, que la usa para su nacimiento): el día exacto con los nombres del calendario de referencia, «15 de Siega de 380 UE». Su año debe coincidir con la fecha que precisa; `check_note.py` lo valida.

## Coherencia
- **Mundo inventado:** si la Ficha lo pide, ni nombres reales de meses o días ni equivalentes disfrazados, ni signos de calendarios reales.
- **Sonido:** si los nombres van en la lengua de una cultura, salen de su perfil de nombres o de su idioma.
- **Lo que ya existe:** las fechas y las fiestas que ya mencionan otras notas (`build_context.py`) deben caber en este calendario; si alguna no cabe, menciónalo en el informe y no la cambies.
- **El conflicto central:** si el mundo tiene uno, el calendario suele llevar su huella (un mes de duelo, un año 0 marcado por él, una fiesta para conjurarlo).
- **Reciprocidad:** cada cultura que ya existe y lo usa lo lista en `calendario`.
- **Glosario:** registra el nombre del calendario, su sufijo, los nombres de los meses (como términos) y las festividades (como costumbres).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 1 y 8 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota); con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- el hecho del año 0 (`evento_cero`), si no tiene nota, con su nombre (el de la Ficha, si lo nombra);
- quienes lo guardan (`guardianes`);
- su fiesta principal (`festividades`);
- una era que cuenta (`eras`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, el calendario guarda un secreto (está mal y lo saben pocos, se borraron años de la cuenta, una fiesta recuerda algo distinto de lo que se cree). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] Si es el de referencia: el año 0 y el año actual son los de la Ficha o los que decidió el usuario, y el pilar quedó resuelto (`referencias/pilares.md`).
- [ ] Si no lo es: existe el de referencia y `ano_cero` dice dónde empieza su cuenta en el eje.
- [ ] Las tablas de meses, estaciones y festividades respetan sus columnas, y `world_calendar.py --calendar <Nota>` lo muestra sin errores.
- [ ] Nada de nombres reales de meses ni de días.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
