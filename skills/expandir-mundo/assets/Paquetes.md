# Paquetes de generación

Un paquete es un grupo de entidades que se crean **juntas en un mismo ciclo**, pensadas como una red: así el mundo crece conectado y no como entidades sueltas. Solo se usa un paquete si existen los módulos de todos sus tipos.

Formato: cada paquete es una sección `## Nombre`, con una línea `Peso: N` (a más peso, más frecuente) y una línea `- tipo: cantidad (papel)` por cada tipo.

## Personaje con vínculos
Peso: 3
- personaje: 1 (principal)
- personaje: 2 (vinculados al principal: familia, mentor o rival)

## Familia
Peso: 2
- personaje: 3 (un progenitor, un hijo o hija y un pariente incómodo)

## Región con su gente
Peso: 2
- region: 1 (la región)
- personaje: 2 (habitantes notables de la región)

## Asentamiento y su gente
Peso: 3
- asentamiento: 1 (una aldea o una villa de la región foco)
- personaje: 2 (quien manda allí y quien no está de acuerdo)

## Asentamiento con un secreto
Peso: 1
- asentamiento: 1 (un lugar que esconde algo)
- personaje: 1 (quien lo sabe y calla)
- secreto: 1 (lo que esconde)

## Lugar y su guardián
Peso: 2
- lugar: 1 (un edificio, un santuario o un paraje de la región foco)
- personaje: 1 (quien lo cuida, lo regenta o lo vigila)

## Ruina con un secreto
Peso: 2
- lugar: 1 (unas ruinas, una mazmorra o una zona peligrosa)
- personaje: 1 (quien la explora o la saquea)
- secreto: 1 (lo que esconde)

## Fenómeno y sus testigos
Peso: 2
- fenomeno: 1 (el fenómeno)
- personaje: 2 (quien lo sufre y quien lo estudia o lo aprovecha)

## Rivalidad
Peso: 2
- personaje: 2 (dos rivales con una historia en común)
- secreto: 1 (lo que uno sabe del otro)

## El forastero
Peso: 1
- personaje: 1 (alguien que acaba de llegar y no es lo que parece)
- personaje: 1 (quien lo acoge, o quien desconfía de él)

## Facciones enfrentadas
Peso: 2
- faccion: 2 (dos facciones rivales de la región foco, con un objetivo que choca)
- personaje: 1 (alguien atrapado entre las dos)

## Conspiración
Peso: 2
- faccion: 1 (quienes conspiran)
- personaje: 2 (quien la dirige y quien está a punto de descubrirla)
- secreto: 1 (el plan)

## Objeto perdido
Peso: 1
- objeto: 1 (algo que se perdió y alguien quiere recuperar)
- personaje: 2 (quien lo busca y quien lo tiene sin saber lo que es)

## Reliquia
Peso: 2
- objeto: 1 (la reliquia)
- personaje: 1 (quien la custodia o la busca)
- secreto: 1 (lo que la reliquia es de verdad)

## Fe y su santuario
Peso: 2
- creencia: 1 (una fe, un culto o una superstición de la región foco)
- lugar: 1 (su santuario o su lugar sagrado)
- personaje: 1 (quien la predica, la guarda o duda de ella)

## Herejía
Peso: 1
- creencia: 1 (una herejía o un culto prohibido)
- faccion: 1 (quienes la persiguen)
- personaje: 1 (quien la practica a escondidas)
- secreto: 1 (lo que la herejía sabe, o cree saber)

## Leyenda local
Peso: 2
- mito: 1 (la leyenda)
- lugar: 1 (donde ocurrió, o donde dicen que ocurrió)
- personaje: 1 (quien la mantiene viva)

## Fiesta de un pueblo
Peso: 2
- costumbre: 1 (una festividad o un rito del pueblo de la región foco)
- mito: 1 (el relato que la justifica)
- lugar: 1 (donde se celebra)

## Ley y quien la impone
Peso: 1
- costumbre: 1 (una ley o un tabú, con su castigo)
- faccion: 1 (quien la dicta y la hace cumplir)
- personaje: 1 (quien la rompió, o quien la paga)

## Profecía
Peso: 1
- mito: 1 (una profecía que se espera en la región foco)
- personaje: 2 (quien cree que la profecía habla de él y quien quiere impedir que se cumpla)
- secreto: 1 (lo que dice de verdad, o quién la amañó)

## Cuento de miedo
Peso: 1
- mito: 1 (un cuento con que se asusta a los niños de la región foco)
- criatura: 1 (lo que el cuento nombra)
- personaje: 1 (quien jura que lo vio)

## Asentamiento vivo
Peso: 3
- asentamiento: 1 (el asentamiento)
- personaje: 3 (quien lo gobierna, quien lo abastece y alguien con un problema)
- faccion: 1 (quien manda de verdad)
- secreto: 1 (lo que esconde)

## Casa y su heredero
Peso: 2
- linaje: 1 (una familia o una casa de la región foco)
- personaje: 2 (su cabeza y quien le disputa la herencia)

## Casas enfrentadas
Peso: 1
- linaje: 2 (dos familias con una enemistad antigua)
- personaje: 1 (alguien de una de ellas, atrapado en la enemistad)

## Casa con un secreto
Peso: 1
- linaje: 1 (una casa con un pasado que no cuenta)
- personaje: 1 (quien lo sabe en la familia y calla)
- secreto: 1 (lo que la familia esconde)

## Brote
Peso: 2
- afeccion: 1 (un mal que se extiende por la región foco)
- personaje: 2 (quien lo sufre y quien intenta curarlo)

## Remedio prohibido
Peso: 1
- afeccion: 1 (un mal sin cura conocida)
- personaje: 1 (quien vende o guarda el remedio)
- secreto: 1 (lo que de verdad cura, o lo que cuesta)

## Cacería
Peso: 2
- criatura: 1 (una bestia o un monstruo que amenaza la región foco)
- personaje: 2 (quien la caza y quien preferiría que nadie lo hiciera)

## Bestia y su guarida
Peso: 1
- criatura: 1 (una criatura que nadie ha visto bien)
- lugar: 1 (su guarida)
- personaje: 1 (quien la vio y sobrevivió)

## Maestro y aprendiz
Peso: 2
- sistema: 1 (un arte, un don o un saber de la región foco)
- personaje: 2 (quien lo domina y quien aprende de él, o quiere arrebatárselo)

## Arte prohibido
Peso: 1
- sistema: 1 (un poder o un saber prohibido en la región foco)
- faccion: 1 (quienes lo persiguen)
- personaje: 1 (quien lo practica a escondidas)
- secreto: 1 (por qué está prohibido de verdad)

## Saber perdido
Peso: 1
- sistema: 1 (un saber que se perdió, o casi)
- lugar: 1 (donde quedó su último rastro)
- personaje: 1 (quien lo busca)

## Ruta de comercio
Peso: 2
- ruta: 1 (una ruta comercial que parte de un lugar que ya existe)
- faccion: 1 (quien la controla o vive de ella: un gremio, una compañía, una casa)
- asentamiento: 1 (una parada o su destino: un mercado de cruce, una villa de paso)

## Paso disputado
Peso: 1
- ruta: 1 (un paso de montaña, un desfiladero, un vado o un estrecho que todos necesitan)
- lugar: 1 (lo que lo cierra o lo vigila: una fortaleza, una torre, un puesto)
- faccion: 1 (quien lo cobra o lo reclama)

## Camino de peregrinación
Peso: 1
- ruta: 1 (el camino de los peregrinos, desde un lugar que ya existe)
- lugar: 1 (el santuario al que lleva)
- costumbre: 1 (el rito del camino)

## El sendero que se pierde
Peso: 1
- ruta: 1 (un sendero sin salida que parte de un lugar que ya existe)
- lugar: 1 (lo último que se ve antes de que se pierda: una ruina, una tumba, un mojón)
- mito: 1 (lo que se cuenta de lo que habría más allá)

## La ruta del texto antiguo
Peso: 1
- ruta: 1 (una ruta perdida o dudosa, que solo cuenta un texto antiguo)
- lugar: 1 (adonde llevaría: un lugar perdido)
- personaje: 1 (quien la busca)

## Ruta de contrabando
Peso: 1
- ruta: 1 (una senda que evita los controles)
- faccion: 1 (quienes la usan)
- objeto: 1 (lo que pasa por ella)

## La puerta entre dos lugares
Peso: 1
- ruta: 1 (un portal, si los poderes del mundo lo permiten; si no, un túnel o un paso secreto)
- lugar: 1 (el sitio donde se abre)
- secreto: 1 (lo que nadie sabe de ella)

## La caravana
Peso: 1
- ruta: 1 (la ruta que recorre)
- personaje: 2 (quien la guía y alguien que viaja con ella por sus propias razones)

## Mina y su gente
Peso: 2
- material: 1 (lo que se saca)
- lugar: 1 (la explotación: una mina, una cantera, una salina)
- personaje: 1 (quien manda allí, o quien baja cada día)

## Fiebre del metal
Peso: 1
- material: 1 (un hallazgo reciente que vale mucho)
- asentamiento: 1 (el campamento o la villa que nació de él)
- faccion: 1 (quien quiere quedárselo)

## Materia prohibida
Peso: 1
- material: 1 (un material que alguien prohíbe sacar, vender o usar)
- faccion: 1 (quien lo prohíbe o quien lo trafica)
- secreto: 1 (por qué está prohibido de verdad)

## Lo que vale una bestia
Peso: 1
- criatura: 1 (la bestia)
- material: 1 (lo que se saca de ella)
- personaje: 1 (quien la caza)

## El agua de todos
Peso: 1
- material: 1 (un recurso del que dependen muchos: agua, suelo fértil, pesca)
- faccion: 1 (quien controla el acceso)
- asentamiento: 1 (quien depende de él)
