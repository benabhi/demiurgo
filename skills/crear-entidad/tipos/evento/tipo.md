# Tipo: evento

Los hechos con fecha que cambiaron algo: guerras, batallas, asedios, rebeliones, catástrofes, fundaciones, tratados, coronaciones y sucesiones, descubrimientos, migraciones, prodigios y crímenes. La ficha dice qué pasó, cuándo y dónde, por qué, cómo se desarrolló, quiénes participaron, qué consecuencias tuvo y cómo se recuerda, con sus versiones enfrentadas.

**No es un evento:**
- un periodo con nombre (`era`): la era se enlaza desde los eventos que la abren y la cierran;
- lo que se repite cada año (`costumbre`): el evento es lo que pasó; la fiesta que lo recuerda, una costumbre;
- una fuerza que sigue actuando (`fenomeno`): el evento la desató y la enlaza en `fenomenos`;
- un relato de los orígenes sin fecha ni testigos (`mito`).

## Identidad del tipo
- **Emoji del tipo:** 📜, al inicio del H1: `# 📜 Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (⚔️ batalla, 🔥 catástrofe, 👑 sucesión, ✍️ tratado, 🏛️ fundación, 🗡️ crimen, ✨ prodigio, 🧭 migración…).
- **Carpeta:** según la `categoria`:
  - `guerra`, `batalla`, `asedio`, `rebelion` y `enfrentamiento` (un conflicto sin batallas) van en `40_Historia/Guerras_y_Conflictos`;
  - `catastrofe`, `fundacion`, `tratado`, `sucesion` (coronaciones, abdicaciones, muertes de soberanos), `descubrimiento`, `migracion`, `prodigio` (una manifestación extraordinaria), `crimen` y `otro` van en `40_Historia/Acontecimientos`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Evento.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, valores permitidos y relaciones). Lleva `crear_desde_cero: false`: una guerra o una catástrofe nueva es un hecho importante, así que el motor solo crea los eventos que otra nota ya nombra como enlace pendiente (el hecho del año 0 de un calendario, el que abre una era, la causa de un fenómeno), nunca uno de la nada.

## Fechas
- `inicio` y `fin` son **años del eje** del calendario de referencia. Un hecho de un solo año lleva solo `inicio`; `fin` se usa cuando dura varios años (una guerra, una migración).
- `fecha_exacta`: el día en que empezó, con los nombres del calendario de referencia («3 de Siega de 412 UE»), del mismo año que `inicio`. Vacía si no existe ese calendario o si nadie sabe el día.
- `duracion`: texto breve («tres días», «doce años», «una noche»).
- **Si el calendario está por definir,** las fechas quedan vacías y el texto usa fechas relativas («hace unos dos siglos»). No decidas el calendario: es un pilar (ver `referencias/pilares.md`).
- **Situación:**
  - `concluido`: ya terminó; no termina después del año actual.
  - `en_curso`: sigue ocurriendo (una guerra abierta, un éxodo que no cesa); sin `fin`.
  - `legendario`: se discute cuándo pasó, o si pasó; las fechas pueden quedar vacías aunque haya calendario.
  - `profetizado`: se espera que ocurra; sin `inicio` o con uno posterior al año actual.
- **El desarrollo** es una tabla con sus fechas: `check_note.py` avisa si una cae fuera de las fechas del evento o si el orden falla.

## Nombre
- Cómo se lo llama hoy en la lengua de la bóveda («la Batalla del Vado», «el Tratado de las Dos Orillas», «la Noche de las Campanas») y, en `aliases`, cómo lo llaman otros, sobre todo los vencidos o los que lo sufrieron.
- Archivo en ASCII. H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué pasó, cuándo y por qué importa.
- **Datos clave:** la tabla completa. «Resultado» dice quién ganó o qué quedó decidido; «Coste», lo que se perdió (vidas, tierras, alianzas, un saber).
- **Causas:** las profundas (lo que venía de lejos), el detonante (lo que lo hizo estallar) y lo que pudo evitarlo. Las causas que merezcan nota propia van en `causas` (otros eventos).
- **Desarrollo:** de 3 a 6 fases, de la más antigua a la más reciente, con sus fechas dentro de las del evento (con el día, si se conoce).
- **Momentos clave:** de 2 a 4: el giro, el instante decisivo, el error, el sacrificio.
- **Participantes:** de 2 a 5 filas: quién, qué papel tuvo, qué hizo y qué fue de él. Nombres nuevos, con `generate_names.py`. Los que ya existen se enlazan y deben estar vivos en esas fechas (`audit_world.py` lo comprueba).
- **Cómo se vivió:** lo que se vio, se oyó y se olió, y lo que fue para la gente común, no solo para los poderosos.
- **Consecuencias:** inmediatas, a largo plazo y lo que cambió para siempre. Las que sean eventos con nota propia van en `consecuencias`; un fenómeno que desató, en `fenomenos`.
- **Cómo se recuerda:** **al menos dos versiones enfrentadas** (vencedores y vencidos, un pueblo y otro, la crónica y la canción) y sus huellas: monumentos, fiestas, canciones, cicatrices en el paisaje, palabras que nacieron de él.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas, de testigos, cronistas o canciones.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para una escena dramática del **momento clave**: el instante congelado, las figuras (sin nombres), el escenario, un detalle que lo cuente y la luz. Nada gráfico, aunque el mundo sea crudo: se sugiere, no se muestra.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `situacion` y `alcance` (`mundial`, `regional` o `local`): ver arriba.
- `inicio`, `fin`, `fecha_exacta` y `duracion`: ver "Fechas".
- Relaciones, solo con enlaces:
  - `lugares` donde ocurrió y `bandos` (facciones, reinos, ejércitos);
  - `participantes`: personajes;
  - `causas` y `consecuencias`: otros eventos; recíprocas;
  - `evento_padre` y `subeventos`: la guerra a la que pertenece una batalla y las batallas de una guerra; recíprocas;
  - `fenomenos` que desató: recíproca con las `causas` del fenómeno;
  - `era` en que ocurrió.
- `relevancia`: 5 un hecho que cambió el mundo (el que abre una era, el que desató el conflicto central); 4 uno que cambió una región; 3 uno local importante; 2 uno menor.
- `ultima_revision` sin comillas.

## Coherencia
- **La Ficha:** si el evento es el que la Ficha nombra (el gran desastre, la guerra que lo empezó todo), lo que la Ficha dice manda y lo que deja abierto queda abierto.
- **La línea del tiempo:** cae dentro de su `era`; si abre o cierra una era, sus fechas coinciden con las de ella; cada causa empieza antes que su consecuencia; una batalla cabe en las fechas de su guerra. `build_context.py` lista las eras en orden y `audit_world.py` avisa de lo que no encaja.
- **Participantes:** vivos en esas fechas, con edades coherentes. Si un personaje que ya existe participó, añade el evento a sus "Momentos decisivos" (reciprocidad en el cuerpo).
- **Poderes y tecnología:** las reglas de la Ficha valen en todos los tiempos; un prodigio o una intervención de las entidades superiores es excepcional y discutido, como dice la Ficha.
- **Hechos importantes nuevos** (otra guerra, un reino, una alianza que no están en el canon): como enlaces pendientes, y en Preguntas Abiertas como `Confirmar: …`, enlazándolos.
- **Reciprocidad:** las causas, consecuencias, guerra madre, batallas y fenómenos que ya existen lo listan en su propiedad inversa.
- **Glosario:** registra el nombre del evento, sus otros nombres y los términos nuevos.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 2 y 8 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- una causa o una consecuencia (`causas`, `consecuencias`);
- un participante (`participantes`);
- un bando (`bandos`);
- el lugar (`lugares`);
- una batalla, si es una guerra (`subeventos`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, el evento guarda un secreto (no fue como se cuenta, el héroe fue el traidor, alguien lo provocó a propósito, el resultado se pactó antes). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] La categoría lleva el evento a su carpeta.
- [ ] Encaja en la línea del tiempo: su era, sus causas y consecuencias, su guerra madre.
- [ ] La situación cuadra con sus fechas y con el año actual; el desarrollo va en orden y dentro de sus fechas.
- [ ] "Cómo se recuerda" tiene al menos dos versiones enfrentadas.
- [ ] Ni el calendario ni otro pilar se decidieron sin el usuario.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
