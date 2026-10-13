# Tablas: Mapas

Ingredientes para la leyenda del mapa de un lugar (ver `crear-entidad/referencias/mapas.md`): su forma, su tamaño, sus niveles, sus salas, sus barrios, sus partes o sus accidentes. Así los lugares no salen todos iguales. Son genéricos: Claude los adapta al mundo, a su género y a su tecnología, y lo que cuenta la nota manda sobre la tirada. A más peso, más frecuente.

Cada clase de mapa usa las suyas: las de **Interior** (edificios, ruinas, mazmorras, torres), las de **Urbano** (asentamientos), las de **Paraje** (islas, bosques, montañas) y las de **Territorio** (regiones). Las de varias zonas se tiran con `--count`, que da resultados distintos entre sí.

## Interior: planta
| Peso | Resultado |
|---|---|
| 3 | Lineal: un eje que se recorre de un extremo a otro, con salas a los lados |
| 2 | Radial: una sala central de la que salen las demás |
| 2 | Ramificada: un camino que se divide una y otra vez, con salas al final de cada rama |
| 2 | En anillo: un circuito que vuelve sobre sí mismo |
| 2 | Irregular: cavidades naturales o ampliaciones hechas sin plan, unidas como se pudo |
| 1 | En cruz: dos ejes que se cortan en una sala o un patio |
| 1 | Simétrica: dos alas iguales a ambos lados de un eje central |
| 1 | Concéntrica: recintos dentro de recintos, cada uno más cerrado que el anterior |
| 1 | Laberíntica: pasillos que se cruzan, vuelven atrás y acaban en nada |
| 1 | Vertical: salas apiladas unas sobre otras, unidas por escaleras, pozos o rampas |
| 1 | Dispersa: varias construcciones sueltas dentro de un recinto o alrededor de un patio |
| 1 | Excavada en una pared: salas en fila o en gradas, abiertas a un precipicio, un río o una sima |

## Interior: tamaño
| Peso | Resultado |
|---|---|
| 3 | Pequeño: de 3 a 5 zonas |
| 3 | Mediano: de 6 a 9 zonas |
| 2 | Grande: de 10 a 12 zonas por nivel |
| 1 | Enorme: tantas zonas que pide varios niveles o pisos |

## Interior: niveles
| Peso | Resultado |
|---|---|
| 3 | Un solo nivel |
| 2 | Hacia abajo: sótanos, criptas o galerías bajo tierra |
| 2 | Hacia arriba: pisos, una torre, galerías altas |
| 1 | En los dos sentidos: una planta de entrada con pisos encima y sótanos debajo |
| 1 | Desniveles: medios pisos, gradas, rampas y entresuelos en lugar de pisos enteros |

## Interior: salas
| Peso | Resultado |
|---|---|
| 3 | Entrada, vestíbulo o antesala |
| 3 | La sala principal, la del poder o la del rito: un trono, un altar mayor, un puesto de mando, un salón |
| 2 | Dormitorios, celdas de descanso o barracones |
| 2 | Cocina, comedor o refectorio |
| 2 | Almacén, despensa o bodega |
| 2 | Taller, forja o sala de trabajo |
| 2 | Un pasillo o una galería con algo que la distingue |
| 2 | Sala de guardia o puesto de vigilancia |
| 1 | Archivo, biblioteca o sala de registros |
| 1 | Santuario, capilla u oratorio |
| 1 | Cámara del tesoro o de lo más valioso |
| 1 | Celdas, calabozo o jaulas |
| 1 | Patio, claustro o espacio abierto |
| 1 | Pozo, cisterna o fuente |
| 1 | Establos, cocheras o hangar, según la técnica del mundo |
| 1 | La sala del mecanismo o la máquina que mueve el lugar |
| 1 | Jardín, huerto o invernadero |
| 1 | Osario, cripta o sala de los muertos |
| 1 | Laboratorio, sala de estudio o de experimentos |
| 1 | Sala de audiencias o de recepción |
| 1 | Mirador, torre de vigía o balcón |
| 1 | Una sala derrumbada o inundada que ya no sirve para lo que era |
| 1 | La guarida de lo que ocupa ahora el lugar |
| 1 | Una cámara sellada que nadie ha abierto |
| 1 | Un paso natural: una grieta, una cueva o un túnel sin labrar |
| 1 | Una sala cuyo uso nadie entiende |

## Interior: labores de una explotación
| Peso | Resultado |
|---|---|
| 3 | Una galería de extracción, con el filón a la vista |
| 2 | Un pozo vertical con su torno o su escala |
| 2 | Una cámara grande, vaciada de tanto sacar |
| 2 | Un frente de trabajo, con andamios y herramientas |
| 1 | Una galería inundada o a medio hundir |
| 1 | Un depósito del material, a la espera de salir |
| 1 | Una sala de lavado, de cribado o de cocción |
| 1 | Un refugio de los trabajadores, con su altar o su amuleto |
| 1 | Un tramo apuntalado que nadie se atreve a cruzar |
| 1 | Una galería vieja, cegada a propósito |
| 1 | Rareza: una galería que nadie recuerda haber excavado |

## Interior: rasgo de una sala
| Peso | Resultado |
|---|---|
| 2 | Agua: charcos, goteras, un canal o el suelo inundado |
| 2 | Un derrumbe que la parte en dos o la cierra a medias |
| 2 | Un objeto central que la domina: una estatua, una mesa, una máquina, un pozo |
| 2 | Inscripciones, pinturas o grabados en los muros |
| 1 | Raíces, musgo u hongos que la invaden |
| 1 | Oscuridad completa, aunque fuera sea de día |
| 1 | Un eco o un ruido constante que no se sabe de dónde viene |
| 1 | Frío o calor que no corresponden a la estación |
| 1 | Restos de una lucha |
| 1 | Restos de un campamento reciente |
| 1 | Un desnivel: un foso, unas gradas, una rampa o un balcón interior |
| 1 | Columnas o pilares que la dividen |
| 1 | Una abertura al exterior: un ventanal, una grieta, una claraboya |
| 1 | Todo intacto, como si alguien acabara de salir |
| 1 | Huesos, restos o tumbas |
| 1 | Un olor intenso que delata lo que hubo o lo que hay |
| 1 | Un mecanismo: palancas, poleas, compuertas, un torno |
| 1 | Una puerta que no lleva a ninguna parte |

## Interior: conexiones
| Peso | Resultado |
|---|---|
| 3 | Una puerta |
| 2 | Un arco o un vano abierto |
| 2 | Un pasillo estrecho |
| 2 | Una escalera |
| 1 | Una escala, una trampilla o un pozo con cuerda |
| 1 | Una grieta o un túnel natural |
| 1 | Un puente sobre un foso, un río o una sima |
| 1 | Una puerta atrancada, tapiada o sellada |
| 1 | Un paso inundado que hay que cruzar con el agua al pecho |
| 1 | Una rampa o un plano inclinado |
| 1 | Un montacargas, una polea o un ascensor, según la técnica del mundo |

## Interior: estado
| Peso | Resultado |
|---|---|
| 3 | En uso y cuidado |
| 2 | En uso, pero venido a menos |
| 2 | Abandonado pero entero |
| 2 | Saqueado |
| 1 | Derrumbado en parte |
| 1 | Inundado, enterrado o invadido por la naturaleza |
| 1 | Ocupado por quien no lo construyó |
| 1 | A medio construir o a medio reformar |

## Interior: lo oculto
| Peso | Resultado |
|---|---|
| 3 | Nada oculto que se conozca |
| 2 | Un paso oculto |
| 2 | Una trampa |
| 1 | Un paso oculto y una trampa |
| 1 | Varias trampas: el lugar se hizo para defenderse |
| 1 | Un paso oculto del que se habla, pero nadie sabe dónde está (va en el texto, no en el mapa) |

## Trampa: mecanismo
| Peso | Resultado |
|---|---|
| 2 | Un suelo que cede sobre un foso o una sima |
| 2 | Algo que cae: una losa, una reja, escombros |
| 2 | Algo que encierra: una jaula, una red, una puerta que se cierra sola |
| 1 | Pinchos, cuchillas o agujas que salen de los muros o del suelo |
| 1 | Algo que dispara: dardos, virotes, un resorte |
| 1 | Gas, humo, polvo o esporas |
| 1 | Agua que sube y anega la sala |
| 1 | Fuego, aceite o brasas |
| 1 | Un derrumbe provocado |
| 1 | Algo que separa: un muro que baja, un suelo que gira, una escalera que se vuelve rampa |
| 1 | Una alarma que avisa a quien vive allí |
| 1 | Un engaño: un pasillo falso, una puerta pintada, un señuelo |
| 1 | La fuerza extraordinaria del mundo (un sello, un glifo, un don), si el mundo la tiene |
| 1 | Un peligro natural aprovechado: un nido, un hielo fino, una corriente |

## Trampa: disparador
| Peso | Resultado |
|---|---|
| 2 | Una losa que se pisa |
| 2 | Abrir algo: una puerta, una tapa, un cajón |
| 1 | Un hilo tendido |
| 1 | Llevarse algo: quitar el peso de un pedestal, sacar un objeto de su sitio |
| 1 | La luz: una antorcha, una contraventana que se abre |
| 1 | El ruido o la voz |
| 1 | Tocar lo que no se debe: una palanca equivocada, un pomo, una inscripción |
| 1 | Pasar sin la señal, la llave o la palabra |
| 1 | El tiempo: se activa a una hora, con la marea o con la estación |
| 1 | Alguien que vigila y la acciona a mano |

## Trampa: efecto
| Peso | Resultado |
|---|---|
| 2 | Herir o matar |
| 2 | Atrapar o encerrar |
| 1 | Separar a los que entran |
| 1 | Cerrar el camino de vuelta |
| 1 | Avisar a quien vive allí |
| 1 | Desgastar: agotar, enfermar, apagar las luces |
| 1 | Marcar a quien la dispara: un tinte, un olor, una señal que se ve después |
| 1 | Asustar: más ruido que daño, para que nadie siga |

## Trampa: quién la puso y para qué
| Peso | Resultado |
|---|---|
| 2 | Quienes lo construyeron, para proteger lo que guardaban |
| 2 | Quien ocupa ahora el lugar, contra los intrusos |
| 1 | Un cazador, para sus presas |
| 1 | Un saqueador anterior, para que nadie le siguiera |
| 1 | Una fe, como prueba o como castigo |
| 1 | Nadie: es el propio lugar, que se ha vuelto peligroso |
| 1 | Alguien que quería que lo encontraran, pero solo quien supiera cómo |
| 1 | Nadie lo recuerda: es tan vieja como el lugar |

## Paso oculto: forma
| Peso | Resultado |
|---|---|
| 2 | Una puerta disimulada en el muro |
| 2 | Una losa o una trampilla en el suelo |
| 2 | Un pasadizo tras un mueble, un tapiz o una estatua |
| 1 | Una grieta que parece no llevar a ningún sitio |
| 1 | Un conducto: de agua, de humo o de aire |
| 1 | Una escalera estrecha dentro de un muro |
| 1 | Un paso bajo el agua |
| 1 | Una chimenea o un pozo |
| 1 | Un mecanismo que gira un muro, un altar o una chimenea |
| 1 | Un hueco tapiado que se abre a golpes |

## Paso oculto: quién lo conoce
| Peso | Resultado |
|---|---|
| 2 | Los que lo usan a escondidas: contrabandistas, criados, fieles |
| 2 | Quien manda en el lugar, y pocos más |
| 1 | Los que lo construyeron, si queda alguno |
| 1 | Se descubrió hace poco y ya corre la voz |
| 1 | Lo conoce una sola persona |
| 1 | Se ve, pero nadie sabe adónde lleva |

## Urbano: forma
| Peso | Resultado |
|---|---|
| 2 | Amurallado en lo alto de una colina o un risco |
| 2 | A orillas de un río, con un puente o un vado |
| 2 | En un cruce de caminos, crecido a lo largo de ellos |
| 2 | En una bahía, una ensenada o la desembocadura de un río |
| 1 | En terrazas sobre una ladera |
| 1 | Alrededor de una fortaleza, un templo o un lugar que lo atrajo todo |
| 1 | Disperso entre campos, sin un centro claro |
| 1 | Apiñado dentro de una ruina más antigua |
| 1 | Excavado en la roca o bajo tierra |
| 1 | Sobre el agua: pilotes, puentes o embarcaciones |
| 1 | En el fondo de un cañón o una garganta |
| 1 | En anillos: un núcleo viejo rodeado de ensanches cada vez más pobres |
| 1 | Alargado, a lo largo de un único camino, una costa o una muralla |
| 1 | En una isla o un islote, unido a tierra o aislado |

## Urbano: barrios
| Peso | Resultado |
|---|---|
| 3 | La plaza mayor o el mercado |
| 2 | El puerto, los muelles o el embarcadero |
| 2 | Un barrio de artesanos de un oficio (curtidores, herreros, tintoreros…) |
| 2 | El barrio de los poderosos, ordenado y vigilado |
| 2 | Un arrabal pobre, apiñado y sin ley |
| 2 | El barrio de los templos o de una fe |
| 1 | Los cuarteles o el barrio de la guardia |
| 1 | El barrio de otro pueblo, con sus costumbres |
| 1 | Un barrio en ruinas o abandonado |
| 1 | Huertas, corrales y pastos dentro de la muralla |
| 1 | Almacenes y depósitos |
| 1 | Tabernas, juego y lo que no se hace a la luz del día |
| 1 | El cementerio o el barrio de los muertos |
| 1 | El barrio de un oficio peligroso o mal visto |
| 1 | Un campamento de recién llegados, refugiados o temporeros |
| 1 | La sede del gobierno |
| 1 | El barrio de los estudiosos, los archivos o las escuelas |
| 1 | Extramuros: lo que creció fuera de la muralla |
| 1 | El barrio de una facción o un gremio que lo controla todo |
| 1 | Un barrio levantado sobre otro más antiguo, que asoma por los sótanos |

## Urbano: hito
| Peso | Resultado |
|---|---|
| 2 | Una torre o una construcción que se ve desde lejos |
| 2 | Un templo o un edificio enorme para el tamaño del lugar |
| 1 | Un puente habitado, con casas encima |
| 1 | Una plaza con algo en el centro: una estatua, un árbol, un pozo, una horca |
| 1 | Una muralla interior que parte el asentamiento |
| 1 | Canales en lugar de calles |
| 1 | Una ruina en pleno centro que nadie derriba |
| 1 | Un mercado cubierto |
| 1 | Una fortaleza que lo domina |
| 1 | Una cicatriz que todavía se ve: un incendio, una inundación, un derrumbe |

## Urbano: bordes
| Peso | Resultado |
|---|---|
| 2 | Una muralla completa con puertas |
| 2 | Una empalizada, un terraplén o un foso |
| 2 | Sin murallas: acaba donde acaban las casas |
| 1 | Un río, un lago o el mar hacen de frontera |
| 1 | Un acantilado, una ladera o un desfiladero lo cierra por un lado |
| 1 | Una muralla vieja, rota y desbordada por las casas |

## Paraje: partes
| Peso | Resultado |
|---|---|
| 2 | Un claro, una pradera o un llano abierto |
| 2 | Una cumbre, un risco o un mirador natural |
| 2 | Una orilla: de un lago, un río o el mar |
| 1 | Una cueva o una sima |
| 1 | Una cascada o un salto de agua |
| 1 | Un vado o un paso estrecho |
| 1 | Una arboleda distinta del resto |
| 1 | Una ciénaga o un tremedal |
| 1 | Una ruina o una construcción solitaria |
| 1 | Un campamento, un refugio o una cabaña |
| 1 | Una formación rara: rocas, árboles o aguas que no se parecen a nada |
| 1 | Un manantial o una fuente |

## Territorio: accidentes
| Peso | Resultado |
|---|---|
| 2 | Una cordillera o una sierra |
| 2 | Un río grande con su valle |
| 2 | Un bosque extenso |
| 2 | Llanuras abiertas |
| 1 | Un lago |
| 1 | Pantanos o marismas |
| 1 | Una meseta o un altiplano |
| 1 | Un desierto, un yermo o un páramo |
| 1 | Una costa de acantilados |
| 1 | Una bahía, un golfo o un delta |
| 1 | Islas o un archipiélago |
| 1 | Un cañón o una garganta |
| 1 | Un volcán o tierras de fuego |
| 1 | Hielo: glaciares, tundra o cumbres nevadas |
| 1 | Colinas onduladas |
| 1 | Cuevas, simas o un mundo bajo tierra |
| 1 | Una tierra marcada por el conflicto central o por un fenómeno del mundo |

## Territorio: dónde vive la gente
| Peso | Resultado |
|---|---|
| 2 | A lo largo de un río o de la costa |
| 2 | En los valles y los llanos, lejos de las alturas |
| 1 | Alrededor de la capital, cada vez más disperso hacia los bordes |
| 1 | En los pasos y los cruces, donde se cobra el paso |
| 1 | Disperso: aldeas sueltas sin un centro |
| 1 | En unos pocos lugares fortificados, con tierra vacía entre ellos |
| 1 | Junto a un recurso: minas, salinas, bosques, pesquerías |
| 1 | Replegada hacia un borde, lejos de lo que hay en el otro |

## Territorio: caminos
| Peso | Resultado |
|---|---|
| 2 | Una gran ruta que la cruza de punta a punta |
| 2 | Caminos entre los asentamientos principales; senderos para el resto |
| 1 | Los ríos o la costa hacen de caminos |
| 1 | Casi sin caminos: se viaja por donde se puede |
| 1 | Caminos antiguos, mejores que lo que se construye hoy |
| 1 | Caminos cortados o abandonados que nadie repara |
| 1 | Un único paso que todos deben cruzar |
