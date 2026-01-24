-- TOUR: CITY TOUR CUSCO PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CITY TOUR CUSCO PULL',
  'Recorrido guiado por los principales atractivos históricos y culturales de la ciudad del Cusco.',
  4,
  1,
  41.00,
  98.00,
  'CITY TOUR',
  'FACIL',
  '{"itinerario": "[Cusco, el Despertar de un Imperio] La Experiencia: \"Descubra el corazón palpitante de los Andes en un viaje a través del tiempo, donde la mampostería inca se funde con la elegancia colonial. Sienta la energía de antiguos muros de piedra y templos sagrados que susurran leyendas de un imperio glorioso. Esta experiencia es más que un tour; es una profunda introducción al espíritu mágico que define a la Ciudad Imperial del Cusco.\""}',
  '{"Lo que visitarás": ["✅ Catedral del Cusco (Arte religioso colonial)", "✅ Qoricancha (Templo del Sol Inca)", "✅ Sacsayhuamán (Fortaleza megalítica)", "✅ Qenqo (Laberinto sagrado)", "✅ Puka Pukara (Control militar inca)", "✅ Tambomachay (Templo del agua)"]}',
  '{"incluye": ["Guía profesional", "Transporte turístico", "Asistencia permanente"]}',
  '{"no_incluye": ["Entradas a atractivos", "Alimentación", "Gastos personales"]}',
  'city_tour_cusco',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: CITY TOUR CUSCO + CATEDRAL PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CITY TOUR CUSCO + CATEDRAL PULL',
  'Recorrido cultural por el Cusco incluyendo visita guiada al interior de la Catedral.',
  4,
  1,
  51.00,
  138.00,
  'CITY TOUR',
  'FACIL',
  '{"itinerario": "[Cusco Profundo y Sagrado] La Experiencia: \"Adéntrese en un museo vivo donde convergen siglos de historia. Desde los corredores sagrados donde se adoraba al Dios Sol hasta la grandeza artística de la fe colonial, cada rincón cuenta una historia de resistencia y belleza. Respire el aire de la montaña mientras contempla la ciudad desde inmensas fortalezas megalíticas, conectando profundamente con los ancestros de esta tierra sagrada.\""}',
  '{"Lo que visitarás": ["✅ Catedral del Cusco (Joya del arte cusqueño)", "✅ Qoricancha (Máxima expresión inca)", "✅ Sacsayhuamán (Ingeniería ciclópea)", "✅ Qenqo (Centro ceremonial subterráneo)", "✅ Puka Pukara (Vigía de los Andes)", "✅ Tambomachay (Culto al agua viva)"]}',
  '{"incluye": ["Guía profesional", "Transporte turístico", "Asistencia permanente"]}',
  '{"no_incluye": ["Entradas adicionales", "Alimentación", "Gastos personales"]}',
  'city_tour_cusco_catedral',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: VALLE SAGRADO VIP PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'VALLE SAGRADO VIP PULL',
  'Excursión de día completo por los principales atractivos culturales y paisajísticos del Valle Sagrado.',
  8,
  1,
  48.00,
  127.00,
  'FULL DAY',
  'MODERADO',
  '{"itinerario": "[El Valle de los Emperadores] La Experiencia: \"Sumérjase en el fértil valle que alimentó a un imperio, un paisaje impresionante de maizales y montañas infinitas. Recorra pueblos antiguos donde las tradiciones permanecen intactas al paso del tiempo y maravíllese con obras de ingeniería colgadas en los acantilados. Este viaje le invita a conectar con la cultura viva de los Andes, ofreciendo un festín para los ojos y serenidad para el alma.\""}',
  '{"Lo que visitarás": ["✅ Pisac (Terrazas y necrópolis)", "✅ Mercado de Pisac (Colores y artesanía)", "✅ Ollantaytambo (Ciudad inca viviente)", "✅ Chinchero (Tejido ancestral)"]}',
  '{"incluye": ["Guía profesional", "Transporte turístico", "Asistencia permanente"]}',
  '{"no_incluye": ["Entradas a atractivos", "Alimentación", "Gastos personales"]}',
  'valle_sagrado_vip',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: VALLE SAGRADO VIP (ROSARIO) PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'VALLE SAGRADO VIP (ROSARIO) PULL',
  'Recorrido extendido por el Valle Sagrado con paradas culturales y paisajísticas adicionales.',
  8,
  1,
  56.00,
  154.00,
  'FULL DAY',
  'MODERADO',
  '{"itinerario": "[Valle Sagrado: Esencia Andina] La Experiencia: \"Deambule por el Valle Sagrado de los Incas, un lugar de belleza mística y cultura vibrante. Experimente el bullicio de los mercados indígenas ricos en color y textura, y asómbrese ante ciudades fortaleza que protegieron el imperio. Este viaje extendido le lleva a lo más profundo del modo de vida andino, revelando vistas panorámicas y el espíritu perdurable del pueblo quechua.\""}',
  '{"Lo que visitarás": ["✅ Mirador Taray (Vista panorámica)", "✅ Pisac (Agricultura vertical)", "✅ Ollantaytambo (Fortaleza de resistencia)", "✅ Chinchero (Cultura textil)"]}',
  '{"incluye": ["Guía profesional", "Transporte turístico", "Asistencia permanente"]}',
  '{"no_incluye": ["Entradas a atractivos", "Alimentación", "Gastos personales"]}',
  'valle_sagrado_vip_rosario',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: MACHU PICCHU FULL DAY PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'MACHU PICCHU FULL DAY PULL',
  'Excursión de día completo al santuario histórico de Machu Picchu desde la ciudad del Cusco.',
  8,
  1,
  270.00,
  730.00,
  'FULL DAY',
  'MODERADO',
  '{"itinerario": "[Machu Picchu, La Ciudad Perdida] La Experiencia: \"Embárquese en una peregrinación a la Joya de la Corona de los Andes, una ciudad oculta entre las nubes. Sienta la emoción del descubrimiento mientras la niebla se disipa para revelar terrazas esmeralda y templos de granito que desafían la gravedad. No es solo una visita a ruinas; es un momento de conexión con un pasado misterioso, un encuentro impresionante con uno de los mayores logros de la humanidad.\""}',
  '{"Lo que visitarás": ["✅ Aguas Calientes (Pueblo cosmopolita)", "✅ Machu Picchu (Maravilla del Mundo)", "✅ Templo del Sol (Astronomía sagrada)", "✅ Intihuatana (Reloj solar)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'machu_picchu_full_day',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: LAGUNA HUMANTAY PULL
INSERT INTO tour (
    nombre,
    descripcion,
    duracion_horas,
    precio_base_usd,
    precio_nacional,
    categoria,
    dificultad,
    highlights,
    atractivos,
    servicios_incluidos,
    servicios_no_incluidos,
    carpeta_img,
    hora_inicio,
    activo
) VALUES (
    'LAGUNA HUMANTAY PULL',
    'Excursión de día completo a una de las lagunas más impresionantes de la cordillera andina, ideal para amantes de la naturaleza y caminatas de altura.',
    12,
    30.00,
    98.00,
    'Naturaleza y Aventura',
    'MODERADO',
    '{"itinerario": "[Humantay: El Espejo Turquesa] La Experiencia: \"Ascienda a una joya escondida acunada por picos nevados, donde el agua brilla como un espejo turquesa reflejando los cielos. El viaje en sí es una meditación, caminando a través de paisajes andinos prístinos para llegar a un santuario de silencio y belleza. Párese ante la montaña sagrada Salkantay y sienta el poder puro de la naturaleza en su forma más vibrante.\""}',
    '{"Lo que visitarás": ["✅ Mollepata (Desayuno andino)", "✅ Soraypampa (Campamento base)", "✅ Laguna Humantay (Turquesa glaciar)", "✅ Nevado Salkantay (Apu protector)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
    'laguna_humantay',
  '2026-01-01 08:00:00-05',
    TRUE
);

-- TOUR: MONTAÑA DE COLORES PULL
INSERT INTO tour (
    nombre,
    descripcion,
    duracion_horas,
    precio_base_usd,
    precio_nacional,
    categoria,
    dificultad,
    highlights,
    atractivos,
    servicios_incluidos,
    servicios_no_incluidos,
    carpeta_img,
    hora_inicio,
    activo
) VALUES (
    'MONTAÑA DE COLORES PULL',
    'Excursión de alta montaña hacia uno de los paisajes más icónicos del Perú, atravesando comunidades andinas y rutas naturales hasta la famosa Montaña de Colores.',
    14,
    32.00,
    104.00,
    'Naturaleza y Aventura',
    'DIFICIL',
    '{"itinerario": "[Vinicunca, El Arcoíris de Piedra] La Experiencia: \"Desafíe su espíritu en una caminata hacia el techo del mundo, donde la tierra se niega a ser de un solo color. Sea testigo de una obra maestra geológica pintada en franjas surrealistas de oro, rojo y turquesa. Estar en la cima de esta maravilla natural ofrece una perspectiva que pocos logran, un panorama impresionante de la cordillera del Vilcanota que quedará grabado en su memoria para siempre.\""}',
    '{"Lo que visitarás": ["✅ Cusipata (Pueblo tradicional)", "✅ Vinicunca (Montaña Arcoíris)", "✅ Valle Rojo (Paisaje marciano)", "✅ Nevado Ausangate (Vista lejana)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
    'montana_de_colores',
  '2026-01-01 08:00:00-05',
    TRUE
);

-- TOUR: PALCCOYO PULL
INSERT INTO tour (
    nombre,
    descripcion,
    duracion_horas,
    precio_base_usd,
    precio_nacional,
    categoria,
    dificultad,
    highlights,
    atractivos,
    servicios_incluidos,
    servicios_no_incluidos,
    carpeta_img,
    hora_inicio,
    activo
) VALUES (
    'PALCCOYO PULL',
    'Excursión alternativa a la Montaña de Colores que permite apreciar formaciones multicolores, paisajes abiertos y caminatas suaves en zonas altoandinas poco concurridas.',
    10,
    37.00,
    124.00,
    'Naturaleza y Aventura',
    'MODERADO',
    '{"itinerario": "[Palccoyo: La Cordillera Pintada] La Experiencia: \"Descubra la hermana serena de la Montaña de Colores, un lugar de majestuosidad tranquila donde la tierra fluye en olas de color. Camine suavemente a través de un bosque de piedras que parece de otro planeta, rodeado por la inmensidad del altiplano. Esto crea un encuentro íntimo con los altos Andes, perfecto para quienes buscan belleza sin multitudes.\""}',
    '{"Lo que visitarás": ["✅ Checacupe (Puente colonial)", "✅ Palccoyo (Tres montañas de colores)", "✅ Bosque de Piedras (Formaciones geológicas)", "✅ Río Rojo (Fenómeno natural)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
    'palccoyo',
  '2026-01-01 08:00:00-05',
    TRUE
);

-- TOUR: PUENTE QESWACHAKA + 4 LAGUNAS PULL
INSERT INTO tour (
    nombre,
    descripcion,
    duracion_horas,
    precio_base_usd,
    precio_nacional,
    categoria,
    dificultad,
    highlights,
    atractivos,
    servicios_incluidos,
    servicios_no_incluidos,
    carpeta_img,
    hora_inicio,
    activo
) VALUES (
    'PUENTE QESWACHAKA + 4 LAGUNAS PULL',
    'Excursión cultural y natural que combina historia viva inca con paisajes altoandinos, lagunas de altura y tradiciones ancestrales aún vigentes.',
    14,
    44.00,
    146.00,
    'Cultura y Naturaleza',
    'MODERADO',
    '{"itinerario": "[Qeswachaka y el Legado Vivo] La Experiencia: \"Sea testigo del increíble legado del último puente inca, una obra maestra tejida a mano cada año por la comunidad. Este viaje le lleva a través de un paisaje de lagunas brillantes y colinas ondulantes, pero lo más destacado es el espíritu humano. Viva una tradición que une el pasado y el presente, un testimonio de unidad y supervivencia cultural en el corazón de los Andes.\""}',
    '{"Lo que visitarás": ["✅ Laguna Pomacanchi (Espejo de agua)", "✅ Laguna Asnaqocha (Fauna andina)", "✅ Puente Qeswachaka (Ingeniería de ichu)", "✅ Río Apurímac (Gran hablador)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
    'puente_qeswachaka_4_lagunas',
  '2026-01-01 08:00:00-05',
    TRUE
);



-- TOUR: WAQRAPUKARA PULL
INSERT INTO tour (
    nombre,
    descripcion,
    duracion_horas,
    precio_base_usd,
    precio_nacional,
    categoria,
    dificultad,
    highlights,
    atractivos,
    servicios_incluidos,
    servicios_no_incluidos,
    carpeta_img,
    hora_inicio,
    activo
) VALUES (
    'WAQRAPUKARA PULL',
    'Excursión de aventura hacia un complejo arqueológico de ubicación estratégica, rodeado de cañones profundos y paisajes altoandinos de gran valor histórico.',
    13,
    39.00,
    130.00,
    'Aventura y Cultura',
    'MODERADO',
    '{"itinerario": "[Waqrapukara: La Fortaleza de los Cuernos] La Experiencia: \"Aventúrese fuera de los caminos trillados hacia la fortaleza en forma de cuernos de Waqrapukara. Esta aventura de trekking le recompensa con un sitio arqueológico dramático encaramado sobre un cañón profundo. Experimente la mezcla perfecta de historia pre-inca, formaciones geológicas impresionantes y soledad. Es un destino para verdaderos exploradores que buscan descubrir las joyas ocultas de Cusco.\""}',
    '{"Lo que visitarás": ["✅ Comunidad Acomayo (Cultura rural)", "✅ Waqrapukara (Fortaleza pre-inca)", "✅ Cañón del Apurímac (Abismo natural)", "✅ Pinturas Rupestres (Huellas antiguas)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
    'waqrapukara',
  '2026-01-01 08:00:00-05',
    TRUE
);

-- TOUR: SIETE LAGUNAS AUSANGATE PULL
INSERT INTO tour (
    nombre,
    descripcion,
    duracion_horas,
    precio_base_usd,
    precio_nacional,
    categoria,
    dificultad,
    highlights,
    atractivos,
    servicios_incluidos,
    servicios_no_incluidos,
    carpeta_img,
    hora_inicio,
    activo
) VALUES (
    'SIETE LAGUNAS AUSANGATE PULL',
    'Ruta de caminata escénica alrededor del nevado Ausangate que permite visitar lagunas de colores intensos y paisajes de alta montaña.',
    14,
    42.00,
    140.00,
    'Naturaleza y Aventura',
    'MODERADO',
    '{"itinerario": "[Ausangate y el Circuito de Cristal] La Experiencia: \"Entre en un paisaje onírico de gran altitud dominado por el poderoso Ausangate. Camine por un circuito de siete lagunas glaciares, cada una con un tono diferente de azul o verde imposible. Es una sinfonía visual de hielo y agua, un lugar donde el aire es fresco y el paisaje tan grandioso que evoca un sentido de humilde asombro ante la magnificencia de la tierra.\""}',
    '{"Lo que visitarás": ["✅ Pacchanta (Aguas termales)", "✅ Laguna Azulcocha (Azul intenso)", "✅ Laguna Pucacocha (Rojiza mineral)", "✅ Nevado Ausangate (Apu sagrado)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
    'siete_lagunas_ausangate',
  '2026-01-01 08:00:00-05',
    TRUE
);

-- TOUR: VALLE SUR PULL
INSERT INTO tour (
    nombre,
    descripcion,
    duracion_horas,
    precio_base_usd,
    precio_nacional,
    categoria,
    dificultad,
    highlights,
    atractivos,
    servicios_incluidos,
    servicios_no_incluidos,
    carpeta_img,
    hora_inicio,
    activo
) VALUES (
    'VALLE SUR PULL',
    'Recorrido cultural por el Valle Sur de Cusco que combina sitios arqueológicos, arquitectura colonial y tradiciones vivas de comunidades locales.',
    6,
    28.00,
    92.00,
    'Cultura',
    'FACIL',
    '{"itinerario": "[Valle Sur: Ingeniería y Fe] La Experiencia: \"Viaje por el camino menos transitado para descubrir la sofisticada ingeniería de las civilizaciones Wari e Inca. Maravíllese ante obras maestras hidráulicas donde el agua aún fluye por canales antiguos, y entre en una capilla colonial deslumbrante con oro y murales. Esta ruta teje los hilos del ingenio prehispánico y el arte colonial.\""}',
    '{"Lo que visitarás": ["✅ Tipón (Ingeniería hidráulica)", "✅ Pikillacta (Urbanismo Wari)", "✅ Andahuaylillas (Capilla Sixtina de América)", "✅ Laguna de Huacarpay (Humedal protegido)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
    'valle_sur',
  '2026-01-01 08:00:00-05',
    TRUE
);

-- TOUR: CHURIN PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CHURIN PULL',
  'Excursion a CHURIN PULL',
  0,
  1,
  28.0,
  94.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Churín: Santuario Termal] La Experiencia: \"Entréguese al abrazo curativo de la tierra en los baños termales de Churín. Deje que las aguas ricas en minerales laven el cansancio del mundo mientras se relaja en medio del tranquilo paisaje de montaña. Este es un santuario para el cuerpo y la mente, un escape restaurador que le invita a reducir la velocidad y encontrar el equilibrio.\""}',
  '{"Lo que visitarás": ["✅ Complejo Mamahuarmi (Pozas naturales)", "✅ Baños de Tingo (Aguas ferrosas)", "✅ Velo de la Novia (Cascada natural)", "✅ Plaza de Churín (Encanto serrano)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'churin',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: CIRCUITO MAGICO + LA CANDELARIA PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CIRCUITO MAGICO + LA CANDELARIA PULL',
  'Excursion a CIRCUITO MAGICO + LA CANDELARIA PULL',
  0,
  1,
  132.0,
  440.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Lima de Noche: Luces y Tradición] La Experiencia: \"Encienda sus sentidos en un deslumbrante espectáculo de luz, agua y música que da vida a la noche. Luego, sumérjase en los vibrantes ritmos del Perú con un show que celebra el diverso folclore de la nación. Es una alegre explosión de color y energía, una velada perfecta que muestra la creatividad moderna y el alma tradicional de la capital.\""}',
  '{"Lo que visitarás": ["✅ Parque de la Reserva (Patrimonio histórico)", "✅ Circuito Mágico (Fuentes ornamentales)", "✅ Show Multimedia (Proyección láser)", "✅ Cena Show (Danzas típicas)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'circuito_magico_la_candelaria',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: MORADA DE LOS DIOSES PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'MORADA DE LOS DIOSES PULL',
  'Excursion a MORADA DE LOS DIOSES PULL',
  0,
  1,
  15.0,
  44.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Apukunaq Tianan: Morada Divina] La Experiencia: \"Visite un santuario moderno tallado en la roca viva, donde el arte contemporáneo honra a las deidades antiguas. Camine entre esculturas gigantes que miran hacia la ciudad, un testimonio del poder perdurable de la mitología andina. Este sitio ofrece una perspectiva surrealista y artística de las montañas, mezclando los viejos dioses con una nueva visión.\""}',
  '{"Lo que visitarás": ["✅ Sencca (Escenario natural)", "✅ El Puma (Guardián terrestre)", "✅ La Pachamama (Madre Tierra)", "✅ Mirador del Cusco (Vista urbana)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'morada_de_los_dioses',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: RUTA DEL SOL CUSCO - PUNO PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'RUTA DEL SOL CUSCO - PUNO PULL',
  'Excursion a RUTA DEL SOL CUSCO - PUNO PULL',
  0,
  1,
  68.0,
  222.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[La Ruta del Sol: Altiplano Ancestral] La Experiencia: \"Transforme un simple traslado en una odisea a través del Altiplano. Atraviese las llanuras altas bajo un cielo expansivo, deteniéndose en templos, museos y pasos de montaña que marcan la columna vertebral del continente. Es un viaje de transiciones, observando cómo el paisaje cambia de valles verdes al ichu dorado de la meseta alta.\""}',
  '{"Lo que visitarás": ["✅ Andahuaylillas (Arte barroco)", "✅ Raqchi (Templo de Wiracocha)", "✅ La Raya (Límite regional)", "✅ Pucará (Museo lítico)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'ruta_del_sol_cusco_puno',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: BARRANCO + HUACA PUCLLANA PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'BARRANCO + HUACA PUCLLANA PULL',
  'Excursion a BARRANCO + HUACA PUCLLANA PULL',
  0,
  1,
  57.0,
  189.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Lima: Contrastes de Tiempo] La Experiencia: \"Experimente el cautivador contraste de Lima, donde una pirámide de adobe pre-inca se alza en medio de la ciudad moderna. Luego, deambule por las calles románticas y llenas de arte de Barranco, respirando la atmósfera bohemia y la brisa del océano. Este tour pinta un retrato de una ciudad con muchas caras, uniendo cimientos antiguos con la vida contemporánea vibrante.\""}',
  '{"Lo que visitarás": ["✅ Huaca Pucllana (Pirámide de adobe)", "✅ Puente de los Suspiros (Romance limeño)", "✅ Bajada de Baños (Arte urbano)", "✅ Malecón (Vista al Pacífico)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'barranco_huaca_pucllana',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: PACHACAMAC + CABALLOS DE PASO PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'PACHACAMAC + CABALLOS DE PASO PULL',
  'Excursion a PACHACAMAC + CABALLOS DE PASO PULL',
  0,
  1,
  144.0,
  482.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Pachacamac: Oráculo y Tradición] La Experiencia: \"Párese ante el oráculo del Pacífico, un templo que atrajo peregrinos durante siglos. Luego, sea testigo de la gracia y elegancia del Caballo Peruano de Paso, un símbolo de la tradición costeña. Esta experiencia casa el misticismo de las antiguas pirámides de arena con la orgullosa herencia de las haciendas.\""}',
  '{"Lo que visitarás": ["✅ Templo del Sol (Adobe y mar)", "✅ Museo de Sitio (Piezas arqueológicas)", "✅ Hacienda Mamacona (Caballos de Paso)", "✅ Show Ecuestre (Marinera y elegancia)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'pachacamac_caballos_de_paso',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: SOBREVUELO LINEAS DE NAZCA - NAZCA PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'SOBREVUELO LINEAS DE NAZCA - NAZCA PULL',
  'Excursion a SOBREVUELO LINEAS DE NAZCA - NAZCA PULL',
  0,
  1,
  135.0,
  453.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Nazca: Mensajes del Cielo] La Experiencia: \"Vuele sobre el enigma del desierto donde líneas antiguas dibujan mensajes a los dioses. Desde el cielo, sea testigo de las colosales figuras de animales y formas grabadas en la tierra árida. Esta perspectiva aérea ofrece una conexión escalofriante con una civilización perdida y sus misterios de astronomía.\""}',
  '{"Lo que visitarás": ["✅ Aeropuerto Nazca (Despegue)", "✅ El Colibrí (Geoglifo perfecto)", "✅ El Mono (Símbolo de agua)", "✅ La Araña (Ritual de lluvia)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'sobrevuelo_lineas_de_nazca_nazca',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: LUNAHUANA PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'LUNAHUANA PULL',
  'Excursion a LUNAHUANA PULL',
  0,
  1,
  25.0,
  82.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Lunahuaná: Aventura y Vino] La Experiencia: \"Escápese a la capital de la aventura de Lima, Lunahuaná. Disfrute del canotaje en el río Cañete y visite viñedos locales para probar vinos y pisco. Este tour combina perfectamente los deportes de aventura al aire libre con el placer gastronómico en un valle cálido y fértil.\""}',
  '{"Lo que visitarás": ["✅ Río Cañete (Canotaje)", "✅ Catapalla (Puente colgante)", "✅ Viñedos (Cata de vinos)", "✅ Apicultura (Miel local)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'lunahuana',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: PARACAS Y HUACACHINA PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'PARACAS Y HUACACHINA PULL',
  'Excursion a PARACAS Y HUACACHINA PULL',
  0,
  1,
  56.0,
  188.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Paracas y Huacachina: Mar y Dunas] La Experiencia: \"Explore lo mejor de la costa sur. Navegue hacia las Islas Ballestas para ver lobos marinos y pingüinos, luego diríjase al Oasis de Huacachina. Monte en tubulares a través de dunas masivas y pruebe el sandboarding. Este tour lleno de acción combina la vida marina con la adrenalina del desierto.\""}',
  '{"Lo que visitarás": ["✅ Islas Ballestas (Fauna marina)", "✅ El Candelabro (Geoglifo costero)", "✅ Oasis Huacachina (Laguna en el desierto)", "✅ Dunas (Sandboarding)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'paracas_y_huacachina',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: PLAYA LA MINA PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'PLAYA LA MINA PULL',
  'Excursion a PLAYA LA MINA PULL',
  0,
  1,
  34.0,
  112.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[La Mina: Paraíso Costero] La Experiencia: \"Relájese en una de las playas más hermosas de la Reserva de Paracas. Famosa por sus aguas turquesas claras y el entorno de acantilados dramáticos, es un paraíso para nadadores. Este tour ofrece un día de playa sin complicaciones rodeado por el impresionante paisaje desértico.\""}',
  '{"Lo que visitarás": ["✅ Reserva de Paracas (Desierto protegido)", "✅ Playa La Mina (Aguas cristalinas)", "✅ Playa Lagunillas (Almuerzo marino)", "✅ Miradores (Vistas al acantilado)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'playa_la_mina',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: MARAS, MORAY Y SALINERAS PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'MARAS, MORAY Y SALINERAS PULL',
  'Excursion a MARAS, MORAY Y SALINERAS PULL',
  0,
  1,
  43.0,
  107.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Maras y Moray: Ingenio Inca] La Experiencia: \"Visite los laboratorios agrícolas enigmáticos de Moray y las espectaculares minas de sal de Maras. Vea miles de pozas de sal cayendo en cascada por el cañón. Este tour destaca el ingenio de los Incas y ofrece algunos de los paisajes más únicos y fotogénicos de la región.\""}',
  '{"Lo que visitarás": ["✅ Moray (Laboratorio agrícola)", "✅ Salineras de Maras (Espejos de sal)", "✅ Pueblo de Maras (Portadas coloniales)", "✅ Cordillera Vilcanota (Fondo escénico)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'maras_moray_y_salineras',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: CORDILLERA PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CORDILLERA PULL',
  'Excursion a CORDILLERA PULL',
  0,
  1,
  28.0,
  94.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Cordillera: Reino del Hielo] La Experiencia: \"Experimente la belleza cruda de los Andes en la Cordillera. Maravíllese con picos irregulares, lagunas glaciares y valles extensos. Este tour le sumerge en el dramático ambiente de alta montaña, un escape ideal para quienes buscan silencio y majestuosidad.\""}',
  '{"Lo que visitarás": ["✅ Lagunas Glaciares (Espejos de agua)", "✅ Nevados (Cumbres eternas)", "✅ Valles (Pastoreo de alpacas)", "✅ Flora Altoandina (Ichu y yareta)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'cordillera',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: PLAYA TUQUILLO PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'PLAYA TUQUILLO PULL',
  'Excursion a PLAYA TUQUILLO PULL',
  0,
  1,
  34.0,
  112.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Tuquillo: La Piscina del Pacífico]\n\nLa Experiencia: \"Descubra la ''Piscina del Pacífico'' en la playa de Tuquillo. Disfrute de aguas tranquilas y cristalinas y arenas doradas en esta joya costera escondida. Este tour es una escapada de verano perfecta, ofreciendo tranquilidad y belleza costera virgen lejos de las multitudes.\""}',
  '{"Lo que visitarás": ["✅ Playa Tuquillo (Aguas mansas)", "✅ Playa Pocitas (Piscinas naturales)", "✅ Huarmey (Gastronomía marina)", "✅ Balneario (Relax total)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'playa_tuquillo',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: MUSEO LARCO PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'MUSEO LARCO PULL',
  'Excursion a MUSEO LARCO PULL',
  0,
  1,
  69.0,
  231.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Museo Larco: Tesoros del Pasado] La Experiencia: \"Viaje en el tiempo en el Museo Larco, hogar de una incomparable colección de arte precolombino. Admire tesoros de oro y plata y la famosa galería de cerámica erótica. Ubicado en una hermosa mansión del siglo XVIII, este tour ofrece una inmersión sofisticada en la historia peruana.\""}',
  '{"Lo que visitarás": ["✅ Galería de Oro (Joyas reales)", "✅ Sala Erótica (Dualidad andina)", "✅ Depósitos (Colección visible)", "✅ Jardines (Entorno colonial)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'museo_larco',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: CUATRIMOTO HUAYPO Y SALINERAS PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CUATRIMOTO HUAYPO Y SALINERAS PULL',
  'Excursion a CUATRIMOTO HUAYPO Y SALINERAS PULL',
  0,
  1,
  42.0,
  138.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Cuatrimotos: Aventura sobre Ruedas] La Experiencia: \"Acelere su adrenalina con una aventura en cuatrimotos por Chinchero. Visite la serena laguna de Huaypo y conduzca hacia los miradores de las Salineras de Maras. Este tour ofrece una forma divertida y rápida de ver los paisajes del Valle Sagrado.\""}',
  '{"Lo que visitarás": ["✅ Laguna Huaypo (Aguas tranquilas)", "✅ Pampa de Chinchero (Campos de cultivo)", "✅ Salineras (Vista panorámica)", "✅ Comunidades (Vida rural)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'cuatrimoto_huaypo_y_salineras',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: PARACAS Y HUACACHINA SUNSET PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'PARACAS Y HUACACHINA SUNSET PULL',
  'Excursion a PARACAS Y HUACACHINA SUNSET PULL',
  0,
  1,
  64.0,
  213.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Paracas y Atardecer en el Desierto] La Experiencia: \"Experimente la magia del atardecer en el desierto. Visite las Islas Ballestas, luego diríjase a Huacachina para los tubulares. Concluya viendo el sol esconderse tras las dunas masivas, pintando la arena de oro y rojo—un final romántico y emocionante para el día.\""}',
  '{"Lo que visitarás": ["✅ El Candelabro (Misterio en arena)", "✅ Islas Ballestas (Pingüinos y lobos)", "✅ Oasis Huacachina (Espejismo real)", "✅ Sunset (Puesta de sol)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'paracas_y_huacachina_sunset',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: CUATRIMOTO MORAY, MARAS Y SALINERAS PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CUATRIMOTO MORAY, MARAS Y SALINERAS PULL',
  'Excursion a CUATRIMOTO MORAY, MARAS Y SALINERAS PULL',
  0,
  1,
  34.0,
  113.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Cuatrimotos: Moray y Salineras] La Experiencia: \"Conduzca cuatrimotos a través de las llanuras de Cruzpata para visitar las terrazas de Moray y las Salineras. Sienta el viento en su cara mientras atraviesa caminos rurales. Este tour añade un giro emocionante al circuito cultural clásico, perfecto para amantes de la aventura.\""}',
  '{"Lo que visitarás": ["✅ Cruzpata (Inicio de aventura)", "✅ Moray (Círculos agrícolas)", "✅ Salineras (Minas de sal)", "✅ Vistas del Valle (Nevados al fondo)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'cuatrimoto_moray_maras_y_salineras',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: CUATRIMOTO MONTAÑA DE COLORES + VALLE ROJO PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CUATRIMOTO MONTAÑA DE COLORES + VALLE ROJO PULL',
  'Excursion a CUATRIMOTO MONTAÑA DE COLORES + VALLE ROJO PULL',
  0,
  1,
  66.0,
  218.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Cuatrimotos a la Montaña de Colores] La Experiencia: \"Combine la emoción de los ATVs con la belleza de la Montaña de Colores. Conduzca para reducir el tiempo de caminata, permitiéndole llegar a Vinicunca y al Valle Rojo con más energía. La forma más divertida y rápida de ver las montañas coloridas.\""}',
  '{"Lo que visitarás": ["✅ Valle del Sur (Ruta escénica)", "✅ Cuatrimotos (Aventura off-road)", "✅ Vinicunca (La cima colorida)", "✅ Valle Rojo (Contraste natural)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'cuatrimoto_montana_de_colores_valle_rojo',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: SOBREVUELO LINEAS DE NAZCA - PISCO PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'SOBREVUELO LINEAS DE NAZCA - PISCO PULL',
  'Excursion a SOBREVUELO LINEAS DE NAZCA - PISCO PULL',
  0,
  1,
  348.0,
  1165.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Nazca desde Pisco: Vuelo Directo] La Experiencia: \"Desbloquee el misterio de las Líneas de Nazca con la comodidad de una salida costera. Vuele sobre el lienzo del desierto para descifrar los mensajes dejados por los antiguos. Esta experiencia perfecta acerca la maravilla del mundo a usted.\""}',
  '{"Lo que visitarás": ["✅ Aeropuerto Pisco (Comodidad)", "✅ Geoglifos (12 figuras principales)", "✅ Desierto de Ica (Mar de dunas)", "✅ Costa Peruana (Vista aérea)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'sobrevuelo_lineas_de_nazca_pisco',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: PALLAY PUNCHU PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'PALLAY PUNCHU PULL',
  'Excursion a PALLAY PUNCHU PULL',
  0,
  1,
  45.0,
  150.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Pallay Punchu: La Montaña Filuda] La Experiencia: \"Descubra las crestas afiladas , similares a un poncho, de Pallay Punchu. Este destino de senderismo más nuevo ofrece formaciones rocosas irregulares y coloridas y vistas de la laguna Langui. Es una alternativa fantástica a Vinicunca, ofreciendo geología dramática y menos multitudes.\""}',
  '{"Lo que visitarás": ["✅ Laguna Langui (Espejo oscuro)", "✅ Pallay Punchu (Formación afilada)", "✅ Canas (Provincia alta)", "✅ Vistas (Valle interandino)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'pallay_punchu',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: LOMAS DE LACHAY  PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'LOMAS DE LACHAY  PULL',
  'Excursion a LOMAS DE LACHAY  PULL',
  0,
  1,
  36.0,
  119.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Lomas de Lachay: Oasis de Niebla] La Experiencia: \"Visite el oasis de niebla estacional de Lomas de Lachay. Camine a través de colinas verdes llenas de flora única y aves que florecen en la niebla del desierto. Este tour es un escape natural refrescante perfectamente adecuado para ecoturistas.\""}',
  '{"Lo que visitarás": ["✅ Reserva Nacional (Ecosistema único)", "✅ Senderos (Caminata suave)", "✅ Flora (Mito y Tara)", "✅ Fauna (Aves y zorros)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'lomas_de_lachay',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: CHANCAY PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CHANCAY PULL',
  'Excursion a CHANCAY PULL',
  0,
  1,
  30.0,
  99.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Castillo de Chancay: Historia y Mar] La Experiencia: \"Adéntrese en una curiosa mezcla de historia y fantasía en el Castillo de Chancay. Explore las torres eclécticas y túneles encaramados en el borde del acantilado. Es un día de descubrimiento considerando tanto tesoros prehispánicos como arquitectura caprichosa.\""}',
  '{"Lo que visitarás": ["✅ Castillo (Arquitectura ecléctica)", "✅ Museo (Cultura Chancay)", "✅ Mirador (Vista al océano)", "✅ Plaza de Armas (Centro histórico)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'chancay',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: CIUDADELA SAGRADA DE CARAL PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CIUDADELA SAGRADA DE CARAL PULL',
  'Excursion a CIUDADELA SAGRADA DE CARAL PULL',
  0,
  1,
  219.0,
  733.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Caral: La Civilización Más Antigua] La Experiencia: \"Camine por las calles de la ciudad más antigua de América. Sienta el peso de 5,000 años de paz e ingeniería en el polvo de Caral. Esta es una peregrinación a la cuna de la cultura andina.\""}',
  '{"Lo que visitarás": ["✅ Ciudadela (Patrimonio Mundial)", "✅ Pirámides (Arquitectura monumental)", "✅ Plazas Circulares (Centros ceremoniales)", "✅ Valle de Supe (Cuna civilizatoria)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'ciudadela_sagrada_de_caral',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: ISLAS PALOMINO PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'ISLAS PALOMINO PULL',
  'Excursion a ISLAS PALOMINO PULL',
  0,
  1,
  82.0,
  273.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Islas Palomino: Nado con Lobos] La Experiencia: \"Sumérjase en el Pacífico para nadar con los juguetones guardianes de la costa. Flotar entre cientos de curiosos lobos marinos es un encuentro de pura alegría. Rodeado de aves marinas, este es un momento para sentirse verdaderamente vivo.\""}',
  '{"Lo que visitarás": ["✅ Callao (Puerto histórico)", "✅ Islas Palomino (Colonia de lobos)", "✅ El Frontón (Isla prisión)", "✅ Fauna (Aves guaneras)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'islas_palomino',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: ANTIOQUIA PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'ANTIOQUIA PULL',
  'Excursion a ANTIOQUIA PULL',
  0,
  1,
  23.0,
  75.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Antioquía: El Pueblo de Colores] La Experiencia: \"Entre en un libro de cuentos donde cada pared es un lienzo de flores y ángeles. El pueblo de Antioquía es un estallido de color en el valle de Lurín. Pruebe productos de manzana locales y deambule por calles que parecen una pintura.\""}',
  '{"Lo que visitarás": ["✅ Pueblo Pintado (Arte mural)", "✅ Iglesia (Arquitectura colonial)", "✅ Huertos (Manzanas y membrillos)", "✅ Mirador (Vista del valle)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'antioquia',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: PACHACAMAC + BARRANCO PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'PACHACAMAC + BARRANCO PULL',
  'Excursion a PACHACAMAC + BARRANCO PULL',
  0,
  1,
  44.0,
  147.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Lima: Pasado y Bohemio] La Experiencia: \"Atraviese el tiempo desde los rituales de barro de Pachacamac hasta el arte callejero de Barranco. Experimente el profundo misticismo de los templos costeros y luego déjese llevar por las vibrantes y coloridas calles del distrito artístico de Lima.\""}',
  '{"Lo que visitarás": ["✅ Pachacamac (Oráculo pre-inca)", "✅ Barranco (Barrio bohemio)", "✅ Puente de los Suspiros (Tradición)", "✅ Arte Urbano (Murales modernos)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'pachacamac_barranco',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: CIRCUITO MAGICO DEL AGUA PULL
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CIRCUITO MAGICO DEL AGUA PULL',
  'Excursion a CIRCUITO MAGICO DEL AGUA PULL',
  0,
  1,
  22.0,
  72.0,
  'TURISMO',
  'FACIL',
  '{"itinerario": "[Circuito Mágico: Fantasía Acuática] La Experiencia: \"Deje que la noche brille en una fantasía de agua y luz. Deambule entre fuentes que bailan con música y proyectan historias en paredes de niebla. Es un lugar de puro capricho y deleite en el corazón de la ciudad.\""}',
  '{"Lo que visitarás": ["✅ Fuente Mágica (80 metros de altura)", "✅ Fuente de la Fantasía (Show láser)", "✅ Túnel de las Sorpresas (Caminata bajo agua)", "✅ Parque de la Reserva (Jardines históricos)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'circuito_magico_del_agua',
  '2026-01-01 08:00:00-05',
  TRUE
);

-- TOUR: CITY TOUR LIMA COLONIAL Y MODERNA
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CITY TOUR LIMA COLONIAL Y MODERNA',
  'Recorrido por el centro histórico de Lima y los distritos modernos.',
  4,
  1,
  30.0,
  101.0,
  'Cultura',
  'FACIL',
  '{"itinerario": "[Lima: La Ciudad de los Reyes]\n\nLa Experiencia: \"Viaje a través de los siglos en la Ciudad de los Reyes. Desde la majestuosidad colonial de la Plaza Mayor y sus balcones tallados hasta la vibrante modernidad de Miraflores frente al Pacífico. Explore catacumbas misteriosas y sienta el pulso de una capital que nunca deja de reinventarse.\""}',
  '{"Lo que visitarás": ["✅ Plaza Mayor (Arquitectura virreinal)", "✅ Catedral de Lima (Arte religioso)", "✅ Catacumbas San Francisco (Criptas coloniales)", "✅ Miraflores (Vistas al océano)", "✅ Parque del Amor (Romance costero)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'city_tour_lima_colonial_y_moderna',
  '2026-01-01 09:00:00-05',
  TRUE
);

-- TOUR: TOUR GASTRONOMICO PERUANO
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'TOUR GASTRONOMICO PERUANO',
  'Experiencia culinaria con visita al mercado y clases de cocina.',
  4,
  1,
  104.0,
  349.0,
  'Gastronomía',
  'FACIL',
  '{"itinerario": "[Sabores del Perú: Aventura Culinaria]\n\nLa Experiencia: \"Sumerja sus sentidos en la capital gastronómica de América. Comience seleccionando ingredientes frescos en un mercado local vibrante, aprenda los secretos del ceviche perfecto y brinde con un Pisco Sour preparado por sus propias manos. Es un viaje delicioso al corazón de la identidad peruana.\""}',
  '{"Lo que visitarás": ["✅ Mercado Local (Frutas exóticas)", "✅ Clase de Cocina (Ceviche y Lomo)", "✅ Degustación de Pisco (Cóctel nacional)", "✅ Almuerzo (Fiesta de sabores)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'tour_gastronomico_peruano',
  '2026-01-01 09:00:00-05',
  TRUE
);

-- TOUR: CITY TOUR NOCTURNO
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'CITY TOUR NOCTURNO',
  'Recorrido panorámico de la ciudad iluminada.',
  3,
  1,
  78.0,
  262.0,
  'Cultura',
  'FACIL',
  '{"itinerario": "[Luces de la Noche: Encanto Urbano]\n\nLa Experiencia: \"Descubra una cara diferente de la ciudad cuando el sol se pone y los monumentos históricos se visten de luz dorada. Recorra plazas vibrantes y calles bohemias envueltas en el romance de la noche, culminando con vistas panorámicas que hacen brillar la metrópolis bajo las estrellas.\""}',
  '{"Lo que visitarás": ["✅ Centro Histórico Iluminado (Monumentos brillantes)", "✅ Plaza San Martín (Elegancia nocturna)", "✅ Barranco (Vida nocturna)", "✅ Puente de los Suspiros (Mística nocturna)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'city_tour_nocturno',
  '2026-01-01 09:00:00-05',
  TRUE
);

-- TOUR: TOUR MISTICO
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'TOUR MISTICO',
  'Ceremonia de pago a la tierra y lectura de coca.',
  3,
  1,
  25.0,
  82.0,
  'Místico',
  'FACIL',
  '{"itinerario": "[Conexión Sagrada: Ritual Andino]\n\nLa Experiencia: \"Conecte con la sabiduría ancestral de los Andes en una ceremonia privada. Guiado por un chamán local, participe en un Pago a la Tierra (Pachamama) y descubra lo que las hojas de coca revelan sobre su camino. Es una experiencia de profunda gratitud y renovación espiritual.\""}',
  '{"Lo que visitarás": ["✅ Altar Sagrado (Espacio ceremonial)", "✅ Chamán Andino (Guía espiritual)", "✅ Lectura de Coca (Sabiduría antigua)", "✅ Ofrenda a la Pachamama (Gratitud universal)"]}',
  '{"incluye": ["Transporte", "Guia", "Asistencia"]}',
  '{"no_incluye": ["Gastos extras"]}',
  'tour_mistico',
  '2026-01-01 09:00:00-05',
  TRUE
);

-- TOUR: DIA LIBRE
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'DIA LIBRE',
  'Día dedicado al descanso o actividades personales sin guía.',
  0,
  1,
  0.00,
  0.00,
  'LIBRE',
  'FACIL',
  '{"itinerario": "[Día Libre: Su Propio Ritmo]\n\nLa Experiencia: \"Disfrute de la libertad de explorar a su propio ritmo. Ya sea que desee sumergirse en los mercados locales, probar ese platillo que le recomendaron, o simplemente descansar y contemplar la belleza de la ciudad, este día es para usted. Sin horarios, sin prisas; solo usted y el espíritu del lugar.\""}',
  '{"Lo que visitarás": ["✅ Exploración personal (A su ritmo)", "✅ Gastronomía local (Sugerencias abiertas)", "✅ Descanso y relax (Tiempo de pausa)", "✅ Compras y artesanía (Opcional)"]}',
  '{"incluye": ["Asistencia informativa"]}',
  '{"no_incluye": ["Guiado", "Transporte", "Entradas", "Alimentacion"]}',
  'dia_libre',
  '2026-01-01 00:00:00-05',
  TRUE
);

-- TOUR: RECEPCION EN EL AEROPUERTO
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'RECEPCION EN EL AEROPUERTO',
  'Recepción en el aeropuerto y traslado al hotel seleccionado.',
  0,
  1,
  0.00,
  0.00,
  'LOGISTICA',
  'FACIL',
  '{"itinerario": "[Bienvenida al Perú: Comience su Aventura]\n\nLa Experiencia: \"A su llegada, nuestro equipo lo estará esperando con una cálida bienvenida. Olvídese de las preocupaciones logísticas mientras lo trasladamos cómodamente a su hotel. Es el inicio de un viaje inolvidable, donde cada detalle está cuidado para que usted solo se dedique a disfrutar y aclimatarse.\""}',
  '{"Lo que visitarás": ["✅ Recepción personalizada (Cartel con nombre)", "✅ Traslado privado (Comodidad y seguridad)", "✅ Asistencia de equipaje (Servicio incluido)", "✅ Briefing del viaje (Información clave)"]}',
  '{"incluye": ["Transporte privado", "Asistencia personalizada"]}',
  '{"no_incluye": ["Alimentación", "Propinas"]}',
  'recepcion_aeropuerto',
  '2026-01-01 00:00:00-05',
  TRUE
);

-- TOUR: DIA LIBRE Y SALIDA AL AEROPUERTO
INSERT INTO tour (
  nombre,
  descripcion,
  duracion_horas,
  duracion_dias,
  precio_base_usd,
  precio_nacional,
  categoria,
  dificultad,
  highlights,
  atractivos,
  servicios_incluidos,
  servicios_no_incluidos,
  carpeta_img,
  hora_inicio,
  activo
) VALUES (
  'DIA LIBRE Y SALIDA AL AEROPUERTO',
  'Mañana libre para actividades personales y traslado al aeropuerto.',
  0,
  1,
  0.00,
  0.00,
  'LOGISTICA',
  'FACIL',
  '{"itinerario": "[Despedida: Memorias y Últimos Tesoros]\n\nLa Experiencia: \"Aproveche sus últimas horas para comprar esos recuerdos finales o dar un último paseo por la ciudad. A la hora coordinada, lo recogeremos de su hotel para trasladarlo al aeropuerto, asegurando que su partida sea tan fluida y agradable como su llegada. ¡Hasta la próxima aventura!\""}',
  '{"Lo que visitarás": ["✅ Tiempo libre (Compras o paseos finales)", "✅ Recojo de hotel (Puntualidad garantizada)", "✅ Traslado al aeropuerto (Tranquilidad total)", "✅ Asistencia en embarque (Soporte informativo)"]}',
  '{"incluye": ["Transporte privado", "Asistencia"]}',
  '{"no_incluye": ["Alimentación", "Gastos personales"]}',
  'dia_libre_salida',
  '2026-01-01 00:00:00-05',
  TRUE
);

-- =================================================================================
-- PAQUETE: PER� PARA EL MUNDO (8 D�as / 7 Noches)
-- =================================================================================
DO 
DECLARE
    p_id INTEGER;
    t_id INTEGER;
BEGIN
    -- 1. Limpiar versiones previas del paquete para evitar duplicados
    DELETE FROM paquete WHERE nombre = 'PER� PARA EL MUNDO 8D/7N';

    -- 2. Crear el Paquete Maestro
    INSERT INTO paquete (nombre, descripcion, dias, noches, precio_sugerido, temporada, destino_principal, activo)
    VALUES ('PER� PARA EL MUNDO 8D/7N', 'Recorrido completo desde la costa de Lima y Paracas hasta el coraz�n de los Andes en Cusco.', 8, 7, 0.00, 'TODO EL A�O', 'PER�', TRUE)
    RETURNING id_paquete INTO p_id;

    -- 3. Asignar Tours (Orden secuencial)
    
    -- D�A 1: LIMA
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'CITY TOUR LIMA COLONIAL Y MODERNA' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 1, 1); END IF;

    -- D�A 2: PARACAS Y HUACACHINA
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'PARACAS Y HUACACHINA PULL' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 2, 2); END IF;

    -- D�A 3: CUSCO CIUDAD
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'CITY TOUR CUSCO PULL' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 3, 3); END IF;

    -- D�A 4: VALLE SAGRADO
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'VALLE SAGRADO VIP PULL' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 4, 4); END IF;

    -- D�A 5: MACHU PICCHU
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'MACHU PICCHU FULL DAY PULL' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 5, 5); END IF;

    -- D�A 6: LAGUNA HUMANTAY
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'LAGUNA HUMANTAY PULL' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 6, 6); END IF;

    -- D�A 7: MONTA�A DE COLORES
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'MONTA�A DE COLORES PULL' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 7, 7); END IF;

    -- D�A 8: SALIDA
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'DIA LIBRE Y SALIDA AL AEROPUERTO' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 8, 8); END IF;

END $$;
-- =================================================================================
-- PAQUETE: CUSCO TRADICIONAL (5 D�as / 4 Noches)
-- =================================================================================
DO 
DECLARE
    p_id INTEGER;
    t_id INTEGER;
BEGIN
    -- 1. Limpiar versiones previas
    DELETE FROM paquete WHERE nombre = 'CUSCO TRADICIONAL 5D/4N';

    -- 2. Crear el Paquete
    INSERT INTO paquete (nombre, descripcion, dias, noches, precio_sugerido, temporada, destino_principal, activo)
    VALUES ('CUSCO TRADICIONAL 5D/4N', 'Lo esencial de la Capital Imperial: Arqueolog�a, Valles Sagrados y la Maravilla del Mundo.', 5, 4, 0.00, 'TODO EL A�O', 'CUSCO', TRUE)
    RETURNING id_paquete INTO p_id;

    -- 3. Asignar Tours
    
    -- D�A 1: CITY TOUR
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'CITY TOUR CUSCO PULL' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 1, 1); END IF;

    -- D�A 2: VALLE SAGRADO
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'VALLE SAGRADO VIP PULL' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 2, 2); END IF;

    -- D�A 3: MACHU PICCHU
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'MACHU PICCHU FULL DAY PULL' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 3, 3); END IF;

    -- D�A 4: HUMANTAY
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'LAGUNA HUMANTAY PULL' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 4, 4); END IF;

    -- D�A 5: MONTA�A DE COLORES
    SELECT id_tour INTO t_id FROM tour WHERE nombre = 'MONTA�A DE COLORES PULL' LIMIT 1;
    IF t_id IS NOT NULL THEN INSERT INTO paquete_tour (id_paquete, id_tour, orden, dia_del_paquete) VALUES (p_id, t_id, 5, 5); END IF;

END ;
