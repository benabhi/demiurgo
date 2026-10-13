# Tipo: región

Las grandes extensiones del mundo: continentes, penínsulas, archipiélagos, desiertos, cordilleras, mares, planetas; los territorios políticos (reinos, provincias, ducados, sectores), y los planos o dimensiones. Es el tipo más enlazado: casi toda entidad está en alguna región.

## Identidad del tipo
- **Emoji del tipo:** 🗺️, al inicio del H1: `# 🗺️ Nombre`.
- **Emoji propio:** cada región tiene uno en la propiedad `emoji`, según su carácter (🏔️ montañosa, 🏜️ desértica, 🌊 costera, 🌫️ brumosa…).
- **Familia:** `lugar`. Los enlaces pendientes de tipo "lugar" de otras fichas (por ejemplo, la `region` de un personaje) se crean con este módulo cuando el contexto es una gran extensión.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Region.md`.
- **Módulo:** `modulo.json` (familia, emoji, rango de enlaces pendientes, carpeta según la categoría, mapa y relaciones).

## Categoría y carpeta
La propiedad `categoria` decide la carpeta (`check_note.py` la valida):

| categoria | Qué es | carpeta |
|---|---|---|
| `fisica` | Una gran extensión natural: continente, península, cordillera, desierto, mar, planeta | `10_Mundo/Grandes_Regiones` |
| `politica` | Un territorio definido por quién lo gobierna: reino, provincia, ducado, sector | `10_Mundo/Paises_y_Territorios` |
| `plano` | Otro nivel de existencia: plano, dimensión, más allá, espacio virtual | `70_Sistemas_y_Cosmologia/Planos_y_Dimensiones` |

Si una zona es a la vez natural y política (una isla que es un reino), crea la región `fisica` y deja la `politica` como enlace pendiente, o al revés, según lo que pida el usuario. No mezcles las dos en una sola nota.

## Escala y anidamiento
- `region_padre` enlaza a la región que la contiene (continente → región → comarca). Así se arma el mapa por niveles.
- **Cuanto mayor es la región, más general es la ficha.** El detalle fino (una ciudad, un templo) va en entidades propias, enlazadas (a su nota o como enlaces pendientes).
- Si la región es el **foco** de la Ficha del Mundo, merece el máximo detalle: es donde ocurrirá casi todo.

## Nombre
- Según la sonoridad de la Ficha y de los pueblos que la habitan. Genera candidatos con `generate_names.py` y elige o adapta uno. Una región puede tener nombres distintos para cada pueblo: van en `aliases`.
- Archivo en ASCII (`Reino_de_Ejemplo.md`). H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es y qué la hace única; no una lista de datos.
- **Datos clave:** la tabla completa. La población, aproximada ("unas cuarenta mil almas", "despoblada"). El estado actual, en una frase ("en guerra", "en declive", "aislada").
- **Descripción:** la experiencia de llegar. Qué se ve primero, el paisaje que domina, sonidos y olores, y lo que no existe en ningún otro sitio.
- **Geografía y clima:**
  - relieve y aguas: montañas, ríos, costas y lagos, con nombres cuando importen;
  - clima y estaciones: cómo cambia la vida a lo largo del año;
  - biomas: bosques, llanuras, pantanos y cómo se reparten.
- **Recursos y economía:** qué se obtiene, qué se fabrica, qué se comercia y qué falta. Las escaseces generan conflictos y ganchos.
- **Habitantes:**
  - qué pueblos y especies viven allí y en qué proporción;
  - cómo viven (nómadas, aldeas, ciudades);
  - qué creen;
  - cómo conviven y dónde están las tensiones.
- **Asentamientos y lugares notables:** de 3 a 6 entradas, cada una con su enlace y una línea que la defina. La capital o el centro, primero.
- **Mapa** (regiones físicas y políticas desde relevancia 4): la leyenda numerada del territorio: la capital, los asentamientos y lugares notables y los accidentes con nombre de su geografía, hasta 12, con su orientación, lo que se ve y sus conexiones (solo los caminos que cuenta la nota). La imagen espera a que haya 5 zonas. Si se sabe, la línea dice a cuántas jornadas queda de otra zona. Ver `referencias/mapas.md`.
- **Poder y fronteras:** quién manda (una facción, un gobierno, nadie), con qué vecinos limita y qué se disputa.
- **Rutas y viajes:**
  - las rutas principales, enlazadas (tipo `ruta`, en `rutas`), con lo que unen y cuántos días se tarda;
  - **cuánto se tarda** en cruzarla a pie, a caballo o en el medio que corresponda;
  - los pasos difíciles.

  Los tiempos de viaje evitan incoherencias más adelante: si ya hay rutas, los suyos mandan (`routes.py <A> <B>`).
- **Peligros:** naturales (clima, terreno), criaturas y otros (bandidos, fenómenos, guerras).
- **Historia:**
  - orígenes, en 1 o 2 párrafos;
  - momentos decisivos: de 3 a 6, con fechas relativas si no hay calendario y enlaces a eventos;
  - el presente: qué está pasando ahora.
- **Relación con el mundo:**
  - el papel concreto de la región ante el conflicto central de la Ficha;
  - cómo afecta ese conflicto a la vida diaria;
  - el tema de la Ficha que encarna.
- **Secretos y rumores:** como en todo tipo. Secreto solo si la tirada sale o el concepto lo pide; 2 o 3 rumores.
- **Ganchos:** de 2 a 4 situaciones abiertas: expediciones, disputas, misterios, amenazas.
- **Citas:** de 1 a 3 frases de habitantes, viajeros o crónicas sobre la región.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para el paisaje panorámico: el relieve dominante, la vegetación, el agua, un hito visible, el clima o la luz, y una señal del conflicto central si se ve.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- **Relaciones solo con enlaces** entre comillas, o vacías si se desconocen (el cuerpo lo explica).
- `clima` y `poblacion` son texto breve (no enlaces): `clima: templado y lluvioso`, `poblacion: unas cuarenta mil almas`.
- `capital`, `asentamientos` y `lugares_notables` enlazan a entidades de la familia `lugar` (asentamientos y sitios); `rutas`, a caminos, calzadas, pasos y portales (tipo `ruta`): cada una la tiene en sus `regiones`.
  - La capital también va en `asentamientos`. Los dos son recíprocos con la `region` del asentamiento.
- `control`: las facciones o gobiernos que mandan. `vecinos`: regiones limítrofes (la relación es recíproca: la región vecina también te lista).
- `fenomenos`: los fenómenos extraordinarios que actúan en la región. Es recíproca: el fenómeno la lista en sus `zonas_afectadas`.
- `especies`: las especies inteligentes que viven en la región. Es recíproca: la especie la lista en sus `regiones`.
- `pueblos`: las culturas que viven en la región. Es recíproca: la cultura la lista en sus `territorios`.
- `recursos`: los materiales y recursos de la región (sus metales, su sal, su agua). Es recíproca: el material la lista en sus `yacimientos`.
- `criaturas`: las criaturas que viven en la región. Es recíproca: la criatura la lista en su `habitat`.
- `relevancia`: de 1 a 5 según la Guía de Organización. Una gran región o la región foco suele ser 4 o 5; una comarca, 3.
- `ultima_revision` sin comillas.

## Coherencia
- **Escala de la Ficha:** en un mundo de escala local, una región es pequeña; en uno de varios mundos, puede ser un planeta.
- **Vecinos:** el clima, la geografía y los pueblos deben encajar con las regiones vecinas que ya existan. Léelas antes de escribir.
- **Pilares:** tecnología, poderes y especies según la Ficha. Una región no inventa una especie ni una civilización nueva por su cuenta: eso va como `Confirmar: …` en Preguntas Abiertas.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 3 y 10 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- la capital o un asentamiento (`capital`, `asentamientos`);
- un lugar notable (`lugares_notables`): una ruina, un santuario, un paso;
- una ruta (`rutas`);
- la facción que la controla (`control`);
- una criatura o un fenómeno locales (`criaturas`, `fenomenos`);
- un pueblo propio de la región (`pueblos`).

Algunos enlaces pendientes apuntan a tipos que aún no tienen módulo (una obra…). No pasa nada: quedan esperando hasta que exista el módulo.

## Secretos
Igual que en personaje: desde relevancia 3, tirada real con `roll_dice.py 1d4` (con 4, la región guarda un secreto), salvo que el concepto o el usuario lo pidan. El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] El nombre es único en la bóveda y en el Glosario.
- [ ] La categoría es la correcta y la nota está en su carpeta.
- [ ] Encaja con la escala de la Ficha, con sus vecinos y con los pilares.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
- [ ] Los hechos de canon grandes que no estaban en el pedido van a Preguntas Abiertas como `Confirmar: …`.
