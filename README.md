# Skills de creación de mundos para Claude Code y Obsidian

Un conjunto de skills de [Claude Code](https://claude.com/claude-code) para crear mundos de ficción de cualquier género (fantasía, ciencia ficción, histórico, terror…) **dentro de una bóveda de Obsidian**. Una entrevista arma la base del mundo, cada entidad se crea como una nota completa y enlazada con las demás, un motor hace crecer el mundo por ciclos y cada nota lleva su imagen.

> **Pensado para Obsidian.** Las skills escriben notas Markdown con propiedades (frontmatter), enlaces `[[…]]`, índices automáticos con el plugin **Bases** y una estructura de carpetas pensada para un mundo. Sin Obsidian las notas se pueden leer, pero se pierden la navegación por enlaces, las propiedades y los índices.

## Qué hace
- **Una entrevista inicial** sobre los pilares del mundo (premisa, género, tono, poderes, tecnología, dioses, especies, calendario…), que crea la bóveda: carpetas con su README, guías de convenciones, índices, la **Ficha del Mundo** y un `CLAUDE.md` con las reglas que salen de tus respuestas.
- **21 tipos de entidad**, cada uno con su ficha, sus reglas y su validación: personajes, regiones, asentamientos, lugares, facciones, linajes, objetos, creencias, deidades, especies, culturas, idiomas, calendarios, eras, eventos, fenómenos, afecciones, criaturas, sistemas (poderes, tecnología, leyes del universo), mitos y secretos.
- **Un mundo entrelazado:** toda entidad que una nota nombra va enlazada. Las que todavía no existen quedan como **enlaces pendientes** con su tipo, y el mundo crece completándolos.
- **Un motor de generación** que elige qué crear según el estado del mundo, tira ingredientes con azar real, crea las entidades, las valida y hace un commit por ciclo.
- **Imágenes** de cada entidad (retratos, paisajes, emblemas, escenas…) con la técnica artística que elijas: acuarela, óleo, grabado, cómic…
- **Coherencia por script:** cada nota se valida al crearla, un auditor revisa el mundo entero (fechas, relaciones recíprocas, nombres repetidos…) y cada generación termina con un informe.
- **Lo que se sabe frente a lo que es:** las notas cuentan lo que el mundo sabe o cree, y la verdad oculta va aparte, en `80_Secretos`.

## Las skills
| Skill | Para qué |
|---|---|
| `inicializar-mundo` | Entrevista y bóveda inicial: estructura, guías, Ficha del Mundo y `CLAUDE.md`. |
| `crear-entidad` | Crea una entidad completa (`/crear-entidad personaje un herrero del puerto`) o completa un enlace pendiente (`/crear-entidad region hueco=Nombre_del_Enlace`). |
| `expandir-mundo` | Hace crecer el mundo por ciclos (`/expandir-mundo 3`), o en una rama aparte para revisarlo antes (`/expandir-mundo prueba`). |
| `generar-imagen` | La imagen de una entidad. La invoca `crear-entidad` sola; también sirve para regenerarla (`/generar-imagen Nombre_de_la_Nota acuarela`). |

Las cuatro van juntas: `expandir-mundo` usa los scripts de `crear-entidad`.

## Requisitos
- **Claude Code.**
- **Obsidian**, con el plugin principal **Bases** activado (los índices de cada sección lo usan).
- **Python 3.10 o posterior.** Los scripts solo usan la biblioteca estándar.
- **Git**, recomendado: el motor hace un commit por ciclo y el modo prueba trabaja en una rama.
- **Para las imágenes**, opcional:
  - Node.js 24 o posterior;
  - una cuenta de [Puter](https://puter.com), porque cada imagen gasta saldo de esa cuenta;
  - su librería, que la skill instala la primera vez que hace falta, con tu permiso (`npm install` en `skills/generar-imagen/scripts`).

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/benabhi/skills-world-building.git
   ```
2. Pon las cuatro carpetas de `skills/` donde Claude Code busca las skills:
   - en `~/.claude/skills/`, para tenerlas en todos tus proyectos;
   - o en `<tu proyecto>/.claude/skills/`, solo para un mundo.

   Mejor enlazarlas que copiarlas: así se actualizan con `git pull`.
   - **Windows**, con PowerShell y sin permisos de administrador (un *junction* por skill):
     ```powershell
     New-Item -ItemType Junction -Path "$HOME\.claude\skills\crear-entidad" -Target "C:\ruta\skills-world-building\skills\crear-entidad"
     ```
   - **macOS y Linux:**
     ```bash
     ln -s /ruta/skills-world-building/skills/crear-entidad ~/.claude/skills/crear-entidad
     ```

## Cómo empezar un mundo
1. Crea una carpeta para el mundo y abre Claude Code en ella. Conviene que sea un repositorio git.
2. Ejecuta `/inicializar-mundo`. Tras la entrevista crea la bóveda en `World_Building/` y el `CLAUDE.md` del mundo en la raíz.
3. Abre `World_Building/` como bóveda en Obsidian y activa el plugin principal Bases.
4. Crea las primeras entidades con `/crear-entidad <tipo> <idea>`. Lo más útil al principio es el foco del mundo y su conflicto central.
5. Deja que el mundo crezca con `/expandir-mundo`.

Los scripts buscan la bóveda en `World_Building/`. Si la tuya está en otra carpeta, todos aceptan `--vault <carpeta>`.

## Cómo es la bóveda
- `00_Sistema/`: la Ficha del Mundo, el índice de inicio, las preguntas abiertas, las convenciones (organización, nombres, canon, estilo, Glosario), las plantillas, los activos (imágenes) y el registro de enlaces pendientes.
- De `10_Mundo/` a `70_Sistemas_y_Cosmologia/`: las entidades, cada una en su carpeta según lo que es.
- `80_Secretos/`: la verdad oculta, que las notas de lore no enlazan.

Cada nota nace como `borrador` y solo tú la promueves a `canon`.

## Idioma
Las skills, las carpetas y las convenciones están en español. El idioma del contenido del mundo y de la conversación se elige en la entrevista.

## Estado
En desarrollo:
- faltan los tipos costumbre, ruta, material, flora, obra, ecosistema y astro;
- falta la skill `finalizar-mundo`, que cerrará los enlaces pendientes de un mundo.

El plan está en [PLAN.md](PLAN.md).

## Licencia
Por definir.
