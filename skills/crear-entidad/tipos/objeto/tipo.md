# Tipo: objeto

Las cosas del mundo: artefactos y reliquias, armas y armaduras, herramientas e instrumentos, vehículos y máquinas, prendas, joyas, muebles y objetos personales, materiales trabajados, consumibles y sustancias (pociones, medicinas, venenos, comidas, bebidas) y monedas. La ficha dice cómo es, para qué sirve, qué tiene de especial, quién lo hizo, de quién fue, dónde está y quién lo busca.

**Un objeto puede ser una pieza única o un tipo de objeto:**
- **Pieza única** (`unico: true`): una espada con nombre, la corona de un rey, un barco concreto. Tiene un creador, una historia de dueños y un sitio donde está hoy.
- **Tipo de objeto** (`unico: false`): una moneda, una poción, un modelo de barca, el arco de los cazadores de una región. Se fabrica o se usa en muchos sitios: «Poseedores» dice quiénes lo usan, y «Dónde está hoy», dónde se hace y dónde se encuentra.

**No es un objeto:**
- una materia prima en bruto (`material`, más adelante): el mineral es un material; el lingote o la tela, un objeto;
- un texto o una obra (`obra`, más adelante): el libro como obra es una obra; un ejemplar con historia propia puede ser también un objeto;
- un edificio o un sitio (`lugar`).

## Identidad del tipo
- **Emoji del tipo:** 🗝️, al inicio del H1: `# 🗝️ Nombre`.
- **Emoji propio:** en la propiedad `emoji`, según su carácter (⚔️ arma, 🛡️ armadura, 🔨 herramienta, ⛵ vehículo, 💍 joya, 🧪 sustancia, 🪙 moneda, 📿 reliquia, 👑 insignia de poder…).
- **Carpeta:** según la `categoria`, en `60_Objetos_y_Recursos`:
  - `artefacto` y `reliquia`: `Artefactos_y_Reliquias` (objetos únicos, legendarios o sagrados);
  - `arma` y `armadura`: `Armas_y_Armaduras`;
  - `herramienta` e `instrumento`: `Herramientas_y_Equipamiento`;
  - `vehiculo` y `maquina`: `Vehiculos_y_Maquinaria`;
  - `prenda`, `joya`, `mueble`, `objeto_personal` y `otro`: `Vestimenta_y_Objetos_Cotidianos`;
  - `material_procesado` (aleaciones, tejidos, cuero, papel, tintes): `Materiales_Procesados`;
  - `consumible` y `sustancia`: `Consumibles_y_Sustancias`;
  - `moneda`: `Monedas_y_Medios_de_Intercambio`.

  Una espada única y legendaria es `artefacto`; una espada corriente con su historia, `arma`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Objeto.md`.
- **Módulo:** `modulo.json` (emoji, rango de enlaces pendientes, carpeta, fechas, tiempo, valores permitidos y relaciones). El motor puede crear objetos desde cero.

**Hechos importantes:** un objeto corriente, una herramienta o una moneda local son detalles que Claude puede inventar según la autonomía de la Ficha. Un artefacto con poderes, una reliquia sagrada o un objeto legendario que no están en el canon son un hecho importante: van como `Confirmar: …` en Preguntas Abiertas, enlazando su nota.

## Poderes y técnica
- **La tecnología de la Ficha manda:** nada que el mundo no sepa fabricar (ni pólvora, ni imprenta, ni relojes mecánicos si la Ficha los excluye), salvo como algo único, excepcional y explicado.
- **Los poderes, con sus reglas:** si el objeto hace algo extraordinario, sigue la regla de poderes de la Ficha y las de su sistema (la magia o el pacto que lo anima), que enlaza en `sistemas`. "Propiedades especiales" dice qué hace, con qué **límites y qué precio** cobra a quien lo usa, y lo que se cree que hace (que puede ser más de lo que hace). Sin límites claros, no hay poder.
- **Si no tiene nada especial,** "Propiedades especiales" lo dice y cuenta por qué se le atribuye algo o por qué importa igualmente (su valor, su historia, lo que significa para alguien).

## Fechas y situación
- `creacion` y `destruccion`: años del eje del calendario de referencia; `destruccion` solo si ya no existe. En un tipo de objeto, `creacion` es cuándo empezó a fabricarse.
- **Si el calendario está por definir,** las fechas quedan vacías y el texto usa fechas relativas. No decidas el calendario: es un pilar (ver `referencias/pilares.md`).
- `situacion`: `en_uso`, `guardado` y `oculto` (existe hoy, sin `destruccion`); `perdido` (nadie sabe dónde está); `roto`; `destruido` (con `destruccion` si se sabe). `check_note.py` comprueba que encaje con el año actual.
- `rareza`: `comun`, `escaso`, `raro`, `unico` o `legendario`. `valor`, `material` y `tamano`: texto breve («tres sueldos de plata», «hierro negro y hueso», «un palmo, ligero»).

## Nombre
- Su nombre propio, si lo tiene («Colmillo de Escarcha», «la Corona Hueca»), o el nombre con que se lo conoce («el sueldo de cobre», «el aceite de vigía»). En `aliases`, sus otros nombres.
- Archivo en ASCII. H1 con la ortografía real.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Resumen:** qué es, de quién es o quién lo usa, y por qué importa.
- **Datos clave:** la tabla completa. «Origen» dice quién lo hizo y cuándo; «Dónde está», su ubicación (o dónde se encuentra, si es un tipo).
- **Aspecto y tacto:** cómo se ve, cómo se siente en la mano (peso, temperatura, textura), las señas del tiempo y del uso, y sus marcas o inscripciones (descritas: el texto de una inscripción va en la lengua de quien la hizo, con su traducción).
- **Uso:** para qué sirve, cómo se usa y quién sabe usarlo.
- **Propiedades especiales:** ver "Poderes y técnica".
- **Origen:** quién lo hizo y cuándo, cómo se hizo y por qué.
- **Poseedores:** en una pieza única, de 2 a 5 filas en orden (quién, cuándo, cómo lo consiguió, cómo lo perdió); en un tipo, quiénes lo fabrican, lo usan o lo comercian.
- **Dónde está hoy:** su ubicación, cómo se consigue (se compra, se hereda, se roba, se gana) y quién lo busca.
- **Variantes:** las copias, las versiones o los objetos parecidos, con enlace si tienen nota; si no tiene, una línea que lo diga.
- **Relación con el mundo, secretos y rumores, ganchos, citas:** como en todo tipo.
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos para el objeto solo: su forma, sus materiales, sus detalles y marcas, su desgaste y cómo le da la luz.
  - "Prompt": lo completa `generar-imagen`.

## Frontmatter
- `categoria`, `unico`, `rareza`, `situacion`, `valor`, `material`, `tamano`, `creacion` y `destruccion`: ver arriba.
- Relaciones, solo con enlaces:
  - `creador`: quien lo hizo;
  - `poseedor`: quien lo tiene hoy, que lo lista en sus `posesiones`; y `poseedores_anteriores`;
  - `ubicacion`: dónde está (un lugar, un asentamiento o una región);
  - `facciones` que lo fabrican, lo guardan o lo buscan: cada una lo lista en sus `objetos`;
  - `culturas` que lo hacen o lo usan, y `creencias` para las que es sagrado;
  - `sistemas` con los que funciona (el poder que lo anima, la técnica que lo hizo posible): cada uno lo tiene en sus `objetos`;
  - `eventos` en que tuvo un papel;
  - `variante_de` y `variantes`: de qué objeto es una versión y qué versiones tiene; recíprocas;
  - `era` en que se hizo.
- `relevancia`: 5 un objeto que cambia el mundo; 4 uno que cambia una región o una facción; 3 uno conocido en su comarca; 2 uno con historia local; 1 uno corriente.
- `ultima_revision` sin comillas.

## Coherencia
- **La Ficha:** técnica y poderes, ver arriba. El conflicto central suele dejar huella en los objetos (cómo se protegen, qué los corroe, qué se rescata).
- **Lo que ya existe:** su poseedor, su creador, el lugar donde está y las facciones que lo guardan deben encajar con lo que dicen sus notas. Si ya existe su poseedor, el objeto va en sus `posesiones`; si está en un lugar que ya existe, en sus `objetos`.
- **Reciprocidad:** el poseedor, las facciones y las variantes que ya existen lo listan en su propiedad inversa. `audit_world.py` avisa si su poseedor está muerto y el objeto sigue en uso.
- **Glosario:** registra su nombre, sus otros nombres y los términos nuevos.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 1 y 5 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota); con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- quien lo hizo (`creador`);
- quien lo tiene o lo tuvo (`poseedor`, `poseedores_anteriores`);
- dónde está (`ubicacion`);
- quien lo guarda o lo busca (`facciones`);
- el hecho en que se perdió o se usó (`eventos`).

## Secretos
Desde relevancia 3, tirada real con `roll_dice.py 1d4`: con 4, el objeto guarda un secreto (es una copia, su creador no es quien dicen, hace algo que nadie sospecha, lleva escondido otro objeto). El secreto se crea con el tipo `secreto` y la ficha nunca lo enlaza.

## Comprobaciones antes de escribir
- [ ] La categoría lo lleva a su carpeta, y `unico` dice si es una pieza o un tipo.
- [ ] Encaja con la técnica de la Ficha; si tiene poderes, con sus límites y su precio.
- [ ] Un artefacto, una reliquia o un objeto legendario que no estaba en el canon quedó como `Confirmar: …`.
- [ ] Su poseedor, sus facciones y sus variantes que ya existen lo listan.
- [ ] No queda ningún campo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las relaciones contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
