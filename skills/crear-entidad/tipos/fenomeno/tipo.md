# Tipo: fenómeno

Las fuerzas y anomalías extraordinarias que actúan en el presente del mundo: una tormenta que nunca amaina, una zona donde el tiempo se detiene, una radiación, una maldición sobre una tierra, una marea que devuelve a los muertos. Casi todo lo demás convive con ellos o los sufre, y el conflicto central de un mundo suele ser uno.

**No es un fenómeno:**
- una enfermedad de las personas (`afeccion`), aunque la provoque un fenómeno;
- un sistema de poder o una tecnología que alguien usa a voluntad (`sistema`);
- un hecho del pasado que ya terminó (`evento`): el fenómeno sigue actuando hoy;
- un cuerpo celeste (`astro`).

## Identidad del tipo
- **Emoji del tipo:** 🌫️, al inicio del H1: `# 🌫️ Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según cómo se manifiesta (🌪️ tormenta, 🔥 fuego, ❄️ frío, 🌑 oscuridad, 🌀 anomalía…).
- **Carpeta:** fija, `70_Sistemas_y_Cosmologia/Fenomenos_Extraordinarios`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Fenomeno.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, escalas, valores permitidos y relaciones).

## El fenómeno central
Si la Ficha del Mundo lo nombra (en la premisa o como conflicto central), es **canon de base**: casi todo el mundo depende de él.
- Construye sobre lo que dicen la Ficha y las notas `canon`, sin contradecirlas ni ampliarlas a lo grande por tu cuenta.
- Lo que la Ficha deja abierto se queda abierto:
  - en "Lo que se sabe y lo que se cree", como creencias enfrentadas;
  - si es una decisión importante (su origen exacto, si avanza, cómo se detendría), además como `Confirmar: …` en Preguntas Abiertas;
  - si ya hay una pregunta abierta sobre eso, no la respondas: menciónala.
- `comportamiento: desconocido` mientras su evolución esté por decidir.
- `relevancia: 5`.
- En "Relación con el mundo", "Ante el conflicto central" dice que **es** el conflicto central y qué parte de él encarna.

## Reglas y límites (lo más importante)
Un fenómeno sin reglas es un comodín que rompe la coherencia. Toda ficha deja claro:
- lo que hace **siempre** y lo que **nunca** hace;
- lo que lo frena o lo detiene, aunque sea poco y a un coste;
- al menos una protección que funciona a medias y una que es falsa o dudosa;
- algo que nadie entiende todavía: un misterio deliberado, no un dato que falta.

Las reglas respetan los pilares de la Ficha. Si los poderes extraordinarios tienen límites claros, el fenómeno también; si la tecnología es medieval, nadie lo mide con instrumentos modernos.

## Nombre
- Muchos fenómenos tienen un nombre descriptivo en la lengua común ("la marea roja", "el silencio"); los grandes, un nombre propio. Para un nombre propio, genera candidatos con `generate_names.py`.
- Los apodos y los nombres de cada pueblo van en `aliases`.
- Archivo en ASCII (`Marea_Roja.md`). H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, qué hace y por qué importa. No una lista de datos.
- **Datos clave:** la tabla completa. "Desde cuándo", con el año del calendario o de forma relativa si está por definir.
- **Manifestación:** cómo se percibe con los sentidos, cómo avisa de su llegada y si cambia de intensidad.
- **Reglas y límites:** ver arriba.
- **Efectos:** concretos, sobre los seres vivos, los objetos y materiales, los lugares y la sociedad (economía, costumbres, miedos). Qué le pasa a una espada, a un pozo, a un niño.
- **Zonas afectadas:** dónde actúa y con qué intensidad, con enlaces a regiones y lugares.
- **Cómo protegerse:** lo que funciona, lo que no y lo que cuesta.
- **Origen e historia:**
  - el origen, según lo que se sabe;
  - de 3 a 6 momentos decisivos, con fechas o relativos;
  - el presente.
- **Lo que se sabe y lo que se cree:** lo comprobado frente a las creencias, teorías y supersticiones de cada pueblo o grupo. Es donde viven las dudas del mundo.
- **Quién lo estudia o lo explota:** grupos o personas, con enlaces, y también quién gana con él.
- **Relación con el mundo, secretos y rumores, ganchos y citas:** como en todo tipo.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para un plano atmosférico: el fenómeno a la escala del paisaje, el paisaje donde actúa, su huella en la tierra, una figura pequeña que dé escala, su luz y su color, y la sensación que transmite.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `naturaleza`: `natural`, `sobrenatural`, `artificial` o `desconocida`.
- `alcance`: `local`, `regional`, `continental`, `mundial` o `cosmico`.
- `permanencia`: `permanente`, `ciclico` o `esporadico`.
- `comportamiento`: `estable`, `en_expansion`, `en_retroceso`, `fluctuante` o `desconocido`.
- `peligrosidad`: del 1 (molesto) al 5 (mortal o catastrófico).
- `inicio` y `fin`: años del calendario de la Ficha, o vacíos si está por definir. `fin`, solo si terminó.
- Relaciones, solo con enlaces:
  - `zonas_afectadas`: regiones y lugares; recíproca con `fenomenos` de la región;
  - `causas`: el evento que lo provocó; recíproca con los `fenomenos` del evento;
  - `fenomeno_padre` y `derivados`: fenómenos que nacen de otro; recíprocas;
  - `afecciones` que provoca y `criaturas` que crea o transforma (cada una lo tiene en sus `fenomenos`);
  - `protecciones` y `estudiosos`: cualquier entidad (un material, un rito, una orden, una persona);
  - `creencias` que giran en torno a él.
- `relevancia`: 5 si es el fenómeno central; 3 o 4 si marca una región; 2 si es local.
- `ultima_revision` sin comillas.

## Coherencia
- **Escala:** su alcance encaja con la escala de la Ficha y con las regiones que afecta. Léelas antes de escribir.
- **Reciprocidad:** cada zona afectada que ya existe lo nombra en su propiedad `fenomenos`.
- **Derivados:** un fenómeno derivado (las tormentas que desata una marea maldita) respeta las reglas de su padre y lo enlaza en `fenomeno_padre`.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 3 y 8 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Los de `protecciones` y `estudiosos`, que admiten cualquier entidad, llevan su tipo en el registro (`pending_links.py --set`). Buenos candidatos:
- un fenómeno derivado (`derivados`);
- una zona afectada (`zonas_afectadas`);
- una afección que provoca (`afecciones`);
- una criatura que nace o cambia con él (`criaturas`);
- el evento que lo causó (`causas`), si aún no existe;
- una creencia que gira en torno a él (`creencias`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 3 o 4, el fenómeno guarda un secreto (su verdadera naturaleza, quién lo provocó, cómo se detendría). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza. Un secreto sobre el fenómeno central es un hecho enorme: además, va como `Confirmar: …` en Preguntas Abiertas, enlazando al fenómeno y no al secreto.

## Comprobaciones antes de escribir
- [ ] El nombre es único en la bóveda y en el Glosario.
- [ ] Tiene reglas, límites y protecciones claras, y respeta los pilares de la Ficha.
- [ ] Si es el fenómeno central, no decide nada que la Ficha deje abierto.
- [ ] Las zonas afectadas que ya existen lo listan en `fenomenos`.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
- [ ] Los hechos de canon grandes que no estaban en el pedido van a Preguntas Abiertas como `Confirmar: …`.
