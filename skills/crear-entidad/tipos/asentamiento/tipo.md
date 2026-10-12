# Tipo: asentamiento

Los lugares donde vive la gente: metrópolis, ciudades, villas, aldeas, caseríos, campamentos, refugios, colonias y estaciones. La ficha dice cómo se ve al llegar, cómo está repartido, quién manda, de qué vive, cómo se defiende, quién vive allí, qué sitios y qué personas importan, y qué problemas tiene.

**No es un asentamiento:**
- un edificio o un sitio concreto (`lugar`): una taberna, un templo, una fortaleza, un puerto o un mercado van en `lugar` y el asentamiento los enlaza en `lugares_notables`;
- un territorio (`region`): un reino, una provincia o una comarca contienen asentamientos;
- unas ruinas que ya nadie habita desde hace mucho (`lugar`, en `Ruinas_y_Zonas_Peligrosas`). Un asentamiento abandonado hace poco, que todavía se recuerda como tal, sí es un asentamiento (`situacion: abandonada`).

## Identidad del tipo
- **Emoji del tipo:** 🏘️, al inicio del H1: `# 🏘️ Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (🏙️ metrópoli, 🏰 ciudad amurallada, ⚓ puerto, 🛖 aldea, ⛺ campamento, 🕳️ refugio, 🛰️ estación…).
- **Carpeta:** fija, `10_Mundo/Ciudades_y_Asentamientos`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Asentamiento.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, valores permitidos y relaciones). Es de la familia `lugar` y su `completa` dice qué enlaces pendientes de otras fichas puede crear:
  - el lugar de nacimiento, la residencia o la ubicación actual de un personaje;
  - la capital y los asentamientos de una región;
  - el territorio de un pueblo y los vecinos de otro asentamiento;
  - la ubicación de un lugar, el escenario de un evento (una ciudad sitiada o saqueada) y la zona que afecta un fenómeno.

  Varios módulos de la familia pueden crear el mismo enlace pendiente: lee lo que dicen de él las notas que lo nombran y elige el que encaje. Si describen un edificio o un sitio («su taller», «la atalaya», «el campo de batalla»), es un `lugar`; si describen un territorio, una `region`.

## Categoría
- `metropoli`: una gran ciudad, centro de su mundo o de su región.
- `ciudad`: miles de habitantes, gobierno propio, mercados y oficios variados.
- `villa`: un pueblo grande o una ciudad pequeña.
- `aldea`: unas decenas de familias que viven de la tierra o del agua.
- `caserio`: unas pocas casas.
- `campamento`: temporal o móvil (de pastores, de un ejército, de refugiados).
- `refugio`: un lugar donde se esconde o resiste gente.
- `colonia`: fundada desde fuera, a menudo lejos de su origen.
- `estacion`: un puesto con una función (de paso, de vigilancia, de investigación; también en el espacio).
- `otro`.

**Hechos importantes:** una aldea, un caserío o un campamento son detalles que Claude puede inventar según la autonomía de la Ficha. Una ciudad grande, una metrópoli o una capital que no están en el canon son un hecho importante: van como `Confirmar: …` en Preguntas Abiertas, enlazando su nota.

## Fechas y situación
- `fundacion` y `abandono`: años del eje del calendario de referencia. `abandono` solo si fue abandonado.
- `fecha_exacta`: el día de su fundación con los nombres del calendario («3 de Siega de 412 UE»), del mismo año que `fundacion`. Vacía si no existe ese calendario o si nadie sabe el día.
- **Si el calendario está por definir,** las fechas quedan vacías y el texto usa fechas relativas («hace cuatro generaciones»). No decidas el calendario: es un pilar (ver `referencias/pilares.md`).
- `situacion`: `prospera`, `estable`, `en_declive` y `amenazada` son asentamientos vivos, sin `abandono`; `abandonada`, uno que ya nadie habita, con `abandono` si se sabe. `check_note.py` comprueba que encaje con el año actual.

## Nombre
- Su nombre en la lengua de quienes lo fundaron o lo habitan, con `generate_names.py --profile <Cultura>` (el perfil de su pueblo principal) o un nombre descriptivo en la lengua de la bóveda («Puerto Ceniza», «Las Tres Norias»). En `aliases`, cómo lo llaman otros pueblos o sus apodos.
- Archivo en ASCII. H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **completa**. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué lugar es, dónde está y qué lo hace reconocible.
- **Datos clave:** la tabla completa. La población, aproximada y coherente con la categoría y con el mundo (en un mundo arrasado, una ciudad de tres mil almas puede ser enorme).
- **Aspecto y ambiente:** lo que se ve al llegar por el camino (es lo que muestra la imagen), lo que se ve, se oye y se huele dentro, la arquitectura y los materiales, y cómo es de noche.
- **Barrios y zonas:** de 2 filas (una aldea) a 5 (una ciudad), con quién vive en cada una. Se nombran por lo que son («el barrio del puerto», «la ladera de los curtidores»); un barrio con nombre propio es un lugar y va enlazado (como enlace pendiente de tipo `lugar`).
- **Gobierno y ley:** quién manda, cómo se decide y las leyes o los castigos que llaman la atención.
- **Economía:** de qué vive, sus mercados y oficios, y lo que le falta y tiene que traer de fuera.
- **Defensas:** murallas, guardia o escondites, y de qué tiene que defenderse.
- **Gente:** los pueblos que viven allí y cómo conviven, las clases y sus tensiones, y cómo se trata a los forasteros.
- **Lugares notables:** de 3 a 6, cada uno con su enlace (los que no existen quedan como enlaces pendientes para el módulo `lugar`) y una línea que lo defina.
- **Personajes notables:** de 2 a 4, con su enlace y su papel: quien manda, quien se le opone, alguien a quien todos conocen.
- **Vida cotidiana:** un día cualquiera, sus fiestas y costumbres (con fechas del calendario, si existe) y sus creencias.
- **Historia:** su fundación (por qué está ahí: un vado, un pozo, una mina, un cruce, un refugio), de 2 a 5 momentos decisivos y el presente.
- **Problemas y tensiones:** de 2 a 4, concretos: son lo que lo hace jugable y lo que el motor puede desarrollar.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para un plano general desde el camino de llegada: la silueta del asentamiento, su arquitectura, lo que lo rodea, señales de vida y su hito más visible.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `situacion`, `fundacion`, `abandono` y `fecha_exacta`: ver arriba. `poblacion`: texto breve («unas ochocientas almas»).
- Relaciones, solo con enlaces:
  - `region`: la región que lo contiene; recíproca con sus `asentamientos` (la capital de una región también va en ellos);
  - `vecinos`: los asentamientos cercanos; recíprocos;
  - `rutas` que pasan por él y `lugares_notables` que contiene (edificios y sitios del módulo `lugar`, que lo tienen en su `ubicacion`);
  - `gobierno` (la institución que manda), `gobernante` (la persona) y otras `facciones` presentes (gremios, bandas, órdenes);
  - `figuras`: personajes notables;
  - `pueblos` que viven en él, recíproca con sus `territorios`, y `creencias` que se practican;
  - `fenomenos` que lo afectan, recíproca con sus `zonas_afectadas`;
  - `era` en que se fundó.
- `relevancia`: 5 la capital o la metrópoli del foco; 4 una ciudad importante; 3 una villa o un puerto con peso; 2 una aldea; 1 un caserío o un campamento de paso.
- `ultima_revision` sin comillas.

## Coherencia
- **La región:** encaja con su geografía, su clima y sus distancias; la región lo lista en `asentamientos` (y en `capital`, si lo es).
- **La Ficha:** la tecnología, los poderes y el conflicto central se notan en cómo vive (qué teme, qué le falta, cómo se defiende).
- **Lo que ya existe:** los personajes que viven o nacieron allí, los pueblos que lo habitan y los eventos que ocurrieron en él deben encajar con su historia y su gente. Léelos (`build_context.py`).
- **Reciprocidad:** la región, los vecinos, los pueblos y los fenómenos que ya existen lo listan en su propiedad inversa.
- **Glosario:** registra su nombre, sus apodos y los términos nuevos (cargos, oficios, expresiones).

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 3 y 10 nuevos** (los que solo nombra esta nota), de al menos dos tipos. Buenos candidatos:
- quien manda (`gobernante`) y la institución (`gobierno`);
- un lugar notable (`lugares_notables`);
- una facción presente (`facciones`);
- una figura (`figuras`);
- un asentamiento vecino (`vecinos`).

## Secretos
Tirada real con `roll_dice.py 1d4`: con 4, el asentamiento guarda un secreto (bajo sus calles hay algo, su fundación fue un crimen, quien manda no es quien parece, el pozo no da solo agua). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] La categoría, la población y la situación encajan entre sí y con el mundo.
- [ ] La región lo contiene y lo lista en `asentamientos`; los vecinos, pueblos y fenómenos que ya existen, también.
- [ ] Una ciudad grande o una capital que no estaba en el canon quedó como `Confirmar: …`.
- [ ] Ni el calendario ni otro pilar se decidieron sin el usuario.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y hay entre 3 y 10 enlaces pendientes nuevos, todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
