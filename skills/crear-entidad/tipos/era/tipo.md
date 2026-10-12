# Tipo: era

Los grandes periodos de la historia del mundo: eras, edades, épocas y periodos con nombre propio, también los legendarios y los que se profetizan. La ficha dice cuándo empezó y terminó, qué la definió, quién dominaba, cómo se vivía y cómo se la recuerda hoy.

**No es una era:**
- un hecho puntual, aunque sea enorme (`evento`): la guerra, la caída o la coronación que abre o cierra una era se enlazan desde ella;
- la forma de contar los años (`calendario`): el calendario cuenta las eras, no al revés.

## Identidad del tipo
- **Emoji del tipo:** ⏳, al inicio del H1: `# ⏳ Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (👑 un imperio, ⚔️ guerras, 🔥 una catástrofe, 🌾 una edad de abundancia, 🌑 una edad oscura, 🕯️ una fe, 📜 un saber…).
- **Carpeta:** fija, `40_Historia/Eras_y_Periodos`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Era.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, valores permitidos y relaciones). Lleva `crear_desde_cero: false`: una era es un hecho importante de la historia, así que el motor solo crea las que otra nota ya nombra como enlace pendiente (la era de una figura, la siguiente de otra era), nunca una de la nada.

## Fechas (lo más importante)
- `inicio` y `fin` son **años del eje** del calendario de referencia (negativos antes del año 0). En el texto se escriben con sus nombres («120 TN», «12 AN»).
- **Si el calendario está por definir,** se quedan vacíos y el cuerpo usa fechas relativas («hace unos tres siglos», «durante cuatro generaciones»). No decidas el calendario: es un pilar (ver `referencias/pilares.md`). En el informe, menciona que con un calendario de referencia (`/crear-entidad calendario`) la era tendría fechas.
- **La línea del tiempo:** `build_context.py` lista las eras que ya existen, en orden. La nueva debe encajar con ellas: si continúa a otra, empieza cuando aquella termina (`anterior` y `siguiente`); si es un periodo de otra, cabe dentro de ella (`era_padre` y `periodos`).
- **Situación:**
  - `actual`: la era del presente; sin `fin`, e `inicio` no posterior al año actual. "Cómo terminó" dice que aún no ha terminado y hacia dónde parece ir.
  - `pasada`: ya terminó; su `fin` no es posterior al año actual.
  - `legendaria`: tan antigua o tan discutida que sus fechas son inciertas; pueden quedar vacías aunque haya calendario, y el cuerpo dice qué se cree.
  - `profetizada`: aún no ha llegado; sin `inicio` o con uno posterior al año actual. Es lo que se cree que vendrá, no un hecho.
- **Alcance:** `mundial`, `regional`, `local` o `de_un_pueblo` (la era tal como la cuenta un pueblo). Pueden convivir eras de distinto alcance en las mismas fechas.

## Nombre
- Cómo se la llama hoy en la lengua de la bóveda («la Edad de las Coronas», «los Años del Hambre») y, en `aliases`, otros nombres: cómo la llamaban quienes la vivieron y cómo la llaman otros pueblos. Que dos pueblos la nombren de forma opuesta es una buena fuente de conflicto.
- Archivo en ASCII. H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué fue la era y qué la define, no una lista de fechas.
- **Datos clave:** la tabla completa. Las fechas, con sus nombres del calendario (o en relativo); la duración, en años.
- **Qué la define:** su rasgo principal, lo que entonces era posible y hoy no (o al revés) y lo que entonces era impensable.
- **Cómo empezó:** el hecho o el proceso que la abrió, con su fecha.
- **Cronología:** de 4 a 8 filas, de la más antigua a la más reciente, con sus fechas dentro de la era. `check_note.py` avisa si una fecha cae fuera o si el orden falla. Los hechos que merezcan nota propia van enlazados: a su evento, si existe, o como enlaces pendientes de tipo `evento` (en `evento_inicio` o `evento_fin`, o con su tipo en el registro).
- **Cómo terminó:** el hecho o el proceso que la cerró; en la era actual, hacia dónde parece ir.
- **Potencias y figuras:** quién mandaba (reinos, órdenes, imperios), qué pueblos dominaban o sufrían, y de 2 a 4 figuras. Nombres nuevos, con `generate_names.py`.
- **Cómo se vivía:** la vida cotidiana, lo que se veía, se oía y se olía, las creencias y el saber y la técnica de entonces.
- **Cómo se la recuerda:** la versión común, otras versiones (de otros pueblos, de los vencidos) y lo que queda de ella en el presente: ruinas, leyes, palabras, heridas, fiestas.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo. Las citas, de cronistas o de gente de entonces.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para una escena **alegórica** que resuma la era entera: la fuerza que la define, figuras anónimas que la encarnan, su paisaje o su arquitectura, sus símbolos y la luz o el ánimo. No un momento concreto: los momentos son de los eventos.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `situacion` y `alcance`: ver arriba.
- `inicio` y `fin`: años del eje, o vacíos.
- Relaciones, solo con enlaces:
  - `calendarios` que la cuentan (recíproca con sus `eras`);
  - `era_padre` y `periodos`: la era que la contiene y los periodos en que se divide; recíprocas;
  - `anterior` y `siguiente`: las eras que la preceden y la siguen; recíprocas;
  - `evento_inicio` y `evento_fin`: los hechos que la abren y la cierran;
  - `regiones` donde transcurre, `culturas` que la protagonizan y `potencias` dominantes (facciones, reinos, órdenes);
  - `figuras`: personajes que la encarnan; cada uno la tiene en su propiedad `era`.
- `relevancia`: 5 una era mundial que explica el presente; 4 una era importante o la del foco; 3 un periodo regional; 2 un periodo menor.
- `ultima_revision` sin comillas.

## Coherencia
- **La Ficha:** el conflicto central y la premisa suelen nacer en alguna era: la que lo causó merece relevancia alta. Lo que la Ficha deja abierto queda abierto.
- **Tecnología y poderes:** las reglas de la Ficha valen también en el pasado. Una era con más saber o más poder que el presente (una edad dorada perdida) es un hecho importante: va como `Confirmar: …` en Preguntas Abiertas, o se cuenta como lo que se cree, no como lo que fue.
- **Lo que ya existe:** las entidades que la enlazan en su `era` (personajes, pueblos, lenguas, lugares) deben caer dentro de sus fechas; `audit_world.py` avisa si no. Lee las eras vecinas antes de escribir.
- **Hechos importantes nuevos** (una guerra, un imperio, una catástrofe que no están en el canon): como enlaces pendientes, y en Preguntas Abiertas como `Confirmar: …`, enlazándolos.
- **Reciprocidad:** las eras vecinas, la era madre y los calendarios que ya existen la listan; las figuras la tienen en su `era`.
- **Glosario:** registra el nombre de la era, sus otros nombres y los términos nuevos.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 2 y 8 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- el hecho que la abrió o la cerró (`evento_inicio`, `evento_fin`);
- la potencia dominante (`potencias`);
- una figura (`figuras`);
- un periodo (`periodos`);
- la era anterior o la siguiente (`anterior`, `siguiente`), si no existen.

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, la era guarda un secreto (su final no fue como se cuenta, una figura venerada causó la desgracia, se borraron años o pueblos de la crónica). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] Encaja en la línea del tiempo: empieza cuando termina la anterior y cabe en su era madre.
- [ ] La situación cuadra con sus fechas y con el año actual de la Ficha.
- [ ] La cronología va en orden y dentro de sus fechas (o en relativo, si el calendario está por definir).
- [ ] Ni el calendario ni otro pilar se decidieron sin el usuario.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
