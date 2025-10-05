<script setup>
import { ref, onMounted, watch, reactive, computed, nextTick } from 'vue'
import { useAccessibilityStore } from '../stores/accessibilityStore.js'
const accessibility = useAccessibilityStore()
accessibility.initLanguage()

// Use the language from the accessibility store
const language = computed(() => accessibility.language)

const translations = reactive({
  en: {
    equations: 'Equations',
    learnMore: 'Learn More',
    p1: 'AstroAegis utilizes meteor trajectory data from (source 1) to predict the extent of damages that could be caused by terrestrial impact.',
    p2: 'Distributions of velocity and meteor diameter data from previous objects were taken to provide accurate simulation data. The path of the meteor was tracked iteratively. Solutions to nonlinear differential equations were approximated via iteration over time steps of arbitrarily small size. These solutions can, to arbitrary closeness (limited by computation resources), approximate its angle of inclination, velocity, acceleration, and position when a meteor enters the edge of Earth’s atmosphere. Once intersecting with Earth’s atmosphere, the heat ablation and mass degradation of the meteor were quantified as rates with respect to time, and further iteratively updated, ending upon impact.',
    p3: 'Ram pressure on the leading edge of a meteor can exceed a material strength, resulting in mass degradation of small NEOs. According to NASA, if the entry radius of an object into the atmosphere is smaller than a defined critical radius:',
    p4: 'it will break into pieces without significant seismic or hydrologic effect before impact, therefore our analysis is finished. If larger, the mass rate of change was determined such that a mass and size at impact could be accurately represented. These rates of change have previously been defined, but prior models assume a constant incident cross sectional area. We aimed to improve these simulations by updating the cross sectional area over time so as to more closely model true behavior.',
    p5: 'By defining the distance from the leading edge of the meteor a and using a previously defined equation relating Brohnsten’s classic ablation equation:',
    p6: 'to incident cross sectional area:',
    p7: 'the distance of the center of an incoming meteor to its new leading edge were determined. This then, in conjunction with the rate of change of mass with respect to the distance from the leading edge:',
    p8: 'were used to develop a more intensive mass rate of change over time, one accounting for the changing cross sectional area as the leading edge ablates.',
    p9: 'The included terms in these rates can be defined as follows.',
    p10: 'Assuming a consistent angle of inclination with respect to a local horizontal plane, the velocity data and its magnitude were determined at impact. Impact here represents the intersection of distance past the atmospheric entry point and geographical elevation data at a given impact position.',
    p11: 'The impact parameters allow us to approximate the kinetic energy of impact:',
    p12: 'which was then converted to the TNT equivalent, as a more tangible metric. The impact energy, in concatenation with the remaining size of the meteor and striking angle at impact were used to categorize crater size and shape. This crater is notably dependent on incident surface density, which was pulled from Lawrence Livermore National Lab data. When striking water, the crater collapses near instantaneously, creating waves up to tsunami scale. When striking land, the impact crater quickly collapses into its final stable form. To find the final shape and size of the crater, we had to calculate the diameter of the transient crater.',
    p13: 'The final diameter of the axis perpendicular to impact can be easily calculated:',
    p14: 'To find the shape, we found the deviation of angle of incidence from the vertical, and scaled the length parallel to impact by a geometric function of the angle from the vertical.',
    p15: 'Since Earth has little data on meteor impact, each density was classified under three separate values of seismic efficiencies.',
    p16: 'One for crystalline rock, one for sedimentary rock, and one for water. These are the three categories for which estimations have been determined. The impact energy and seismic efficiency can quantify the magnitude of seismic activity on a Richter scale through the following equivalencies.',
    p17: 'Additionally, to calculate the vertical velocity of the transverse s wave from an earthquake, sources (cite) an empirical formula:',
    p18: 'As distance d from epicenter and TNT equivalent E_TNT vary with respect to time, specifically with respect to translational wave velocity, vertical acceleration can be calculated.',
    p19: 'According to (cite), s-waves approach triviality once the magnitude of the vertical acceleration reaches 5% of surface gravity, 9.81 m * (s)^-2 occurs at time',
    p20: 'Regarding tsunamis, meteoric impacts temporarily displace mass amounts of water from oceans. This displacement can, at large enough scales, produce waves spreading radially from the impact position. To model the propagation of these waves, we again performed an interactive simulation based on principles of shoaling and Green’s Law to find velocity v and wave height A as the waves expand outwards over ocean depth h.',
    p21: 'Wave height at coast defines an intensity under the Iida model:',
    p22: 'which serves as a surrogate for potential damages.'
  },
  es: {
    equations: 'Ecuaciones',
    learnMore: 'Aprende Más',
    p1: 'AstroAegis utiliza datos de trayectoria de meteoritos de (fuente 1) para predecir la extensión de los daños que podrían ser causados por el impacto terrestre.',
    p2: 'Se tomaron distribuciones de datos de velocidad y diámetro de meteoritos de objetos anteriores para proporcionar datos de simulación precisos. La trayectoria del meteorito se rastreó de manera iterativa. Las soluciones a ecuaciones diferenciales no lineales se aproximaron mediante iteración sobre pasos de tiempo de tamaño arbitrariamente pequeño. Estas soluciones pueden, con una cercanía arbitraria (limitada por los recursos computacionales), aproximar su ángulo de inclinación, velocidad, aceleración y posición cuando un meteorito entra en el borde de la atmósfera terrestre. Una vez que intersecta con la atmósfera terrestre, la ablación térmica y la degradación de masa del meteorito se cuantificaron como tasas con respecto al tiempo, y se actualizaron iterativamente, terminando en el impacto.',
    p3: 'La presión de impacto en el borde delantero de un meteorito puede exceder la resistencia del material, resultando en la degradación de la masa de pequeños NEOs. Según la NASA, si el radio de entrada de un objeto en la atmósfera es menor que un radio crítico definido:',
    p4: 'se romperá en pedazos sin un efecto sísmico o hidrológico significativo antes del impacto, por lo tanto, nuestro análisis termina aquí. Si es mayor, la tasa de cambio de masa se determinó de modo que una masa y tamaño en el impacto pudieran ser representados con precisión. Estas tasas de cambio se han definido previamente, pero los modelos anteriores asumen un área de sección transversal constante. Buscamos mejorar estas simulaciones actualizando el área de sección transversal a lo largo del tiempo para modelar un comportamiento más realista.',
    p5: 'Definiendo la distancia desde el borde delantero del meteorito a y usando una ecuación previamente definida relacionada con la ecuación clásica de ablación de Brohnsten:',
    p6: 'al área de sección transversal incidente:',
    p7: 'se determinó la distancia del centro de un meteorito entrante a su nuevo borde delantero. Esto, junto con la tasa de cambio de masa respecto a la distancia desde el borde delantero:',
    p8: 'se utilizó para desarrollar una tasa de cambio de masa más intensiva en el tiempo, una que tenga en cuenta el cambio del área de sección transversal a medida que el borde delantero se ablate.',
    p9: 'Los términos incluidos en estas tasas se pueden definir de la siguiente manera.',
    p10: 'Asumiendo un ángulo de inclinación constante respecto a un plano horizontal local, los datos de velocidad y su magnitud se determinaron en el impacto. El impacto aquí representa la intersección de la distancia pasada el punto de entrada atmosférica y los datos de elevación geográfica en una posición de impacto dada.',
    p11: 'Los parámetros de impacto nos permiten aproximar la energía cinética del impacto:',
    p12: 'que luego se convirtió al equivalente en TNT, como una métrica más tangible. La energía de impacto, junto con el tamaño restante del meteorito y el ángulo de impacto, se utilizaron para categorizar el tamaño y la forma del cráter. Este cráter depende notablemente de la densidad superficial incidente, que se obtuvo de datos del Laboratorio Nacional Lawrence Livermore. Al impactar en agua, el cráter colapsa casi instantáneamente, creando olas de escala de tsunami. Al impactar en tierra, el cráter de impacto colapsa rápidamente en su forma final estable. Para encontrar la forma y el tamaño final del cráter, tuvimos que calcular el diámetro del cráter transitorio.',
    p13: 'El diámetro final del eje perpendicular al impacto se puede calcular fácilmente:',
    p14: 'Para encontrar la forma, determinamos la desviación del ángulo de incidencia respecto a la vertical y escalamos la longitud paralela al impacto mediante una función geométrica del ángulo respecto a la vertical.',
    p15: 'Dado que la Tierra tiene pocos datos sobre impactos de meteoritos, cada densidad se clasificó bajo tres valores separados de eficiencias sísmicas.',
    p16: 'Uno para roca cristalina, uno para roca sedimentaria y uno para agua. Estas son las tres categorías para las que se han determinado estimaciones. La energía de impacto y la eficiencia sísmica pueden cuantificar la magnitud de la actividad sísmica en la escala de Richter mediante las siguientes equivalencias.',
    p17: 'Además, para calcular la velocidad vertical de la onda transversal s de un terremoto, las fuentes (citar) una fórmula empírica:',
    p18: 'A medida que la distancia d desde el epicentro y el equivalente en TNT E_TNT varían con el tiempo, específicamente con respecto a la velocidad de onda de traslación, se puede calcular la aceleración vertical.',
    p19: 'Según (citar), las ondas s se vuelven triviales una vez que la magnitud de la aceleración vertical alcanza el 5% de la gravedad superficial, 9.81 m * (s)^-2 ocurre en el tiempo',
    p20: 'En cuanto a los tsunamis, los impactos meteóricos desplazan temporalmente grandes cantidades de agua de los océanos. Este desplazamiento puede, a gran escala, producir olas que se expanden radialmente desde la posición de impacto. Para modelar la propagación de estas olas, nuevamente realizamos una simulación interactiva basada en principios de shoaling y la Ley de Green para encontrar la velocidad v y la altura de la ola A a medida que las olas se expanden hacia afuera sobre la profundidad del océano h.',
    p21: 'La altura de la ola en la costa define una intensidad bajo el modelo de Iida:',
    p22: 'que sirve como un sustituto de los posibles daños.'
  },
  fr: {
    equations: 'Équations',
    learnMore: 'En Savoir Plus',
    p1: "AstroAegis utilise des données de trajectoire de météores de (source 1) pour prédire l'étendue des dommages qui pourraient être causés par un impact terrestre.",
    p2: "Des distributions de données de vitesse et de diamètre de météores provenant d'objets précédents ont été prises pour fournir des données de simulation précises. Le chemin du météore a été suivi de manière itérative. Les solutions aux équations différentielles non linéaires ont été approximées par itération sur des pas de temps de taille arbitrairement petite. Ces solutions peuvent, à une proximité arbitraire (limitée par les ressources informatiques), approximer son angle d'inclinaison, sa vitesse, son accélération et sa position lorsqu'un météore entre dans le bord de l'atmosphère terrestre. Une fois qu'il intersecte avec l'atmosphère terrestre, l'ablation thermique et la dégradation de la masse du météore ont été quantifiées comme des taux par rapport au temps, et mises à jour de manière itérative, se terminant à l'impact.",
    p3: "La pression sur le bord d'attaque d'un météore peut dépasser la résistance du matériau, entraînant une dégradation de la masse des petits NEO. Selon la NASA, si le rayon d'entrée d'un objet dans l'atmosphère est inférieur à un rayon critique défini :",
    p4: "il se brisera en morceaux sans effet sismique ou hydrologique significatif avant l'impact, donc notre analyse est terminée. Si plus grand, le taux de changement de masse a été déterminé de sorte qu'une masse et une taille à l'impact puissent être représentées avec précision. Ces taux de changement ont déjà été définis, mais les modèles antérieurs supposent une aire de section constante. Nous avons cherché à améliorer ces simulations en mettant à jour l'aire de section au fil du temps pour modéliser un comportement plus réaliste.",
    p5: "En définissant la distance depuis le bord d'attaque du météore a et en utilisant une équation précédemment définie liée à l'équation classique d'ablation de Brohnsten :",
    p6: "à l'aire de section incidente :",
    p7: "la distance du centre d'un météore entrant à son nouveau bord d'attaque a été déterminée. Ceci, avec le taux de changement de masse par rapport à la distance depuis le bord d'attaque :",
    p8: "a été utilisé pour développer un taux de changement de masse plus intensif dans le temps, tenant compte du changement d'aire de section à mesure que le bord d'attaque s'ablate.",
    p9: "Les termes inclus dans ces taux peuvent être définis comme suit.",
    p10: "En supposant un angle d'inclinaison constant par rapport à un plan horizontal local, les données de vitesse et leur magnitude ont été déterminées à l'impact. L'impact ici représente l'intersection de la distance passée le point d'entrée atmosphérique et les données d'élévation géographique à une position d'impact donnée.",
    p11: "Les paramètres d'impact nous permettent d'approximer l'énergie cinétique de l'impact :",
    p12: "qui a ensuite été convertie en équivalent TNT, comme une métrique plus tangible. L'énergie d'impact, avec la taille restante du météore et l'angle d'impact, ont été utilisés pour catégoriser la taille et la forme du cratère. Ce cratère dépend notamment de la densité de surface incidente, obtenue à partir des données du Lawrence Livermore National Lab. Lorsqu'il frappe l'eau, le cratère s'effondre presque instantanément, créant des vagues de type tsunami. Lorsqu'il frappe la terre, le cratère d'impact s'effondre rapidement dans sa forme finale stable. Pour trouver la forme et la taille finales du cratère, nous avons dû calculer le diamètre du cratère transitoire.",
    p13: "Le diamètre final de l'axe perpendiculaire à l'impact peut être facilement calculé:",
    p14: "Pour trouver la forme, nous avons trouvé la déviation de l'angle d'incidence par rapport à la verticale et avons mis à l'échelle la longueur parallèle à l'impact par une fonction géométrique de l'angle par rapport à la verticale.",
    p15: "Comme la Terre a peu de données sur les impacts de météores, chaque densité a été classée sous trois valeurs distinctes d'efficacités sismiques.",
    p16: "Une pour la roche cristalline, une pour la roche sédimentaire et une pour l'eau. Ce sont les trois catégories pour lesquelles des estimations ont été déterminées. L'énergie d'impact et l'efficacité sismique peuvent quantifier l'ampleur de l'activité sismique sur l'échelle de Richter grâce aux équivalences suivantes.",
    p17: "De plus, pour calculer la vitesse verticale de l'onde transversale s d'un tremblement de terre, les sources (citer) une formule empirique :",
    p18: "À mesure que la distance d depuis l'épicentre et l'équivalent TNT E_TNT varient dans le temps, en particulier par rapport à la vitesse de l'onde de translation, l'accélération verticale peut être calculée.",
    p19: "Selon (citer), les ondes s deviennent négligeables une fois que l'amplitude de l'accélération verticale atteint 5% de la gravité de surface, 9,81 m * (s)^-2 se produit au temps",
    p20: "Concernant les tsunamis, les impacts météoriques déplacent temporairement de grandes quantités d'eau des océans. Ce déplacement peut, à grande échelle, produire des vagues qui se propagent radialement à partir de la position d'impact. Pour modéliser la propagation de ces vagues, nous avons de nouveau effectué une simulation interactive basée sur les principes du shoaling et la loi de Green pour trouver la vitesse v et la hauteur de vague A à mesure que les vagues s'étendent sur la profondeur de l'océan h.",
    p21: "La hauteur de la vague à la côte définit une intensité selon le modèle d'Iida :",
    p22: "qui sert de substitut aux dommages potentiels."
  },
  ru: {
    equations: 'Уравнения',
    learnMore: 'Узнать больше',
    p1: 'AstroAegis использует данные о траектории метеоров из (источник 1) для прогнозирования масштабов ущерба, который может быть вызван земным воздействием.',
    p2: 'Для обеспечения точных данных моделирования были взяты распределения данных о скорости и диаметре метеоров от предыдущих объектов. Путь метеора отслеживался итеративно. Решения нелинейных дифференциальных уравнений приближались путем итерации по временным шагам произвольно малого размера. Эти решения могут, с произвольной точностью (ограниченной вычислительными ресурсами), приближать его угол наклона, скорость, ускорение и положение, когда метеор входит в край атмосферы Земли. После пересечения с атмосферой Земли тепловое истирание и деградация массы метеора были количественно определены как скорости по времени и далее итеративно обновлялись, заканчиваясь при ударе.',
    p3: 'Давление на передней кромке метеора может превышать прочность материала, что приводит к деградации массы малых НЭО. По данным NASA, если радиус входа объекта в атмосферу меньше определенного критического радиуса:',
    p4: 'он распадется на части без значительного сейсмического или гидрологического эффекта до удара, поэтому наш анализ завершен. Если больше, скорость изменения массы определялась так, чтобы масса и размер при ударе могли быть точно представлены. Эти скорости изменения были определены ранее, но предыдущие модели предполагают постоянную площадь поперечного сечения. Мы стремились улучшить эти симуляции, обновляя площадь поперечного сечения со временем для более точного моделирования поведения.',
    p5: 'Определяя расстояние от передней кромки метеора a и используя ранее определенное уравнение, связанное с классическим уравнением абляции Бронштена:',
    p6: 'к инцидентной площади поперечного сечения:',
    p7: 'расстояние от центра входящего метеора до его новой передней кромки было определено. Это, вместе со скоростью изменения массы относительно расстояния от передней кромки:',
    p8: 'использовалось для разработки более интенсивной скорости изменения массы во времени, учитывающей изменение площади поперечного сечения по мере абляции передней кромки.',
    p9: 'Включенные в эти скорости термины можно определить следующим образом.',
    p10: 'Предполагая постоянный угол наклона относительно локальной горизонтальной плоскости, данные о скорости и их величина определялись при ударе. Удар здесь представляет собой пересечение расстояния после точки входа в атмосферу и данных о географической высоте в данной точке удара.',
    p11: 'Параметры удара позволяют нам приблизительно оценить кинетическую энергию удара:',
    p12: 'которая затем была преобразована в эквивалент TNT, как более наглядную метрику. Энергия удара, вместе с оставшимся размером метеора и углом удара, использовалась для категоризации размера и формы кратера. Этот кратер особенно зависит от плотности поверхности, которая была получена из данных Ливерморской национальной лаборатории. При ударе о воду кратер почти мгновенно разрушается, создавая волны до масштаба цунами. При ударе о сушу кратер быстро разрушается до своей окончательной стабильной формы. Чтобы найти окончательную форму и размер кратера, нам пришлось рассчитать диаметр переходного кратера.',
    p13: 'Окончательный диаметр оси, перпендикулярной удару, можно легко вычислить:',
    p14: 'Чтобы найти форму, мы определили отклонение угла падения от вертикали и масштабировали длину, параллельную удару, с помощью геометрической функции угла относительно вертикали.',
    p15: 'Поскольку на Земле мало данных о метеоритных ударах, каждая плотность классифицировалась по трем отдельным значениям сейсмической эффективности.',
    p16: 'Одна для кристаллической породы, одна для осадочной породы и одна для воды. Это три категории, для которых были определены оценки. Энергия удара и сейсмическая эффективность могут количественно определить величину сейсмической активности по шкале Рихтера с помощью следующих эквивалентов.',
    p17: 'Кроме того, для расчета вертикальной скорости поперечной s-волны от землетрясения источники (цитата) используют эмпирическую формулу:',
    p18: 'По мере того как расстояние d от эпицентра и эквивалент TNT E_TNT изменяются во времени, в частности относительно скорости продольной волны, можно рассчитать вертикальное ускорение.',
    p19: 'Согласно (цитата), s-волны становятся незначительными, когда величина вертикального ускорения достигает 5% от силы тяжести поверхности, 9,81 м * (с)^-2 происходит во времени',
    p20: 'Что касается цунами, метеоритные удары временно перемещают большие массы воды из океанов. Это перемещение может, в больших масштабах, создавать волны, распространяющиеся радиально от точки удара. Для моделирования распространения этих волн мы снова провели интерактивное моделирование на основе принципов shoaling и закона Грина, чтобы найти скорость v и высоту волны A по мере того, как волны распространяются по глубине океана h.',
    p21: 'Высота волны на побережье определяет интенсивность по модели Ииды:',
    p22: 'которая служит суррогатом для возможного ущерба.'
  },
  zh: {
    equations: '方程',
    learnMore: '了解更多',
    p1: 'AstroAegis 利用来自（来源 1）的陨石轨迹数据来预测可能由地面撞击造成的损害程度。',
    p2: '从先前的物体中获取了速度和陨石直径数据的分布，以提供准确的模拟数据。陨石的路径是通过迭代跟踪的。通过对任意小尺寸的时间步长进行迭代，近似求解非线性微分方程的解。这些解可以在任意接近（受计算资源限制）的情况下，近似其倾角、速度、加速度和位置，当陨石进入地球大气层边缘时。一旦与地球大气层相交，陨石的热烧蚀和质量退化就被量化为相对于时间的速率，并进一步迭代更新，直到撞击为止。',
    p3: '陨石前缘的冲击压力可能超过材料强度，导致小型近地天体的质量退化。根据 NASA，如果物体进入大气层的半径小于定义的临界半径：',
    p4: '它将在撞击前碎裂成碎片，不会产生显著的地震或水文效应，因此我们的分析到此结束。如果更大，则确定质量变化率，以便可以准确表示撞击时的质量和大小。这些变化率以前已被定义，但先前的模型假定入射横截面积恒定。我们旨在通过随时间更新横截面积来改进这些模拟，以更真实地模拟实际行为。',
    p5: '通过定义从陨石前缘到 a 的距离，并使用先前定义的与 Brohnsten 经典烧蚀方程相关的方程：',
    p6: '到入射横截面积：',
    p7: '确定了入射陨石中心到其新前缘的距离。这与质量随前缘距离变化率一起使用：',
    p8: '用于开发更密集的质量变化率，考虑到前缘烧蚀时横截面积的变化。',
    p9: '这些速率中包含的术语可以定义如下。',
    p10: '假设与局部水平面保持一致的倾角，撞击时确定了速度数据及其大小。这里的撞击代表了大气入口点之后的距离与给定撞击位置的地理高程数据的交点。',
    p11: '撞击参数使我们能够近似撞击的动能：',
    p12: '然后将其转换为 TNT 当量，作为更直观的度量。撞击能量与撞击时剩余的陨石大小和角度一起用于分类陨石坑的大小和形状。这个陨石坑显著依赖于入射表面密度，该密度取自劳伦斯利弗莫尔国家实验室的数据。当撞击水面时，陨石坑几乎瞬间坍塌，形成海啸级别的波浪。当撞击陆地时，撞击坑很快坍塌为其最终稳定形态。为了找到陨石坑的最终形状和大小，我们必须计算瞬态陨石坑的直径。',
    p13: '撞击垂直轴的最终直径可以很容易地计算出来：',
    p14: '为了找到形状，我们找到了入射角与垂直方向的偏差，并通过入射角的几何函数缩放了与撞击平行的长度。',
    p15: '由于地球上关于陨石撞击的数据很少，每种密度都根据三种不同的地震效率值进行分类。',
    p16: '一种用于结晶岩石，一种用于沉积岩石，一种用于水。这是为这些类别确定的估算值。撞击能量和地震效率可以通过以下等效关系量化里氏震级的地震活动。',
    p17: '此外，为了计算地震横波的垂直速度，来源（引用）了一个经验公式：',
    p18: '随着距离 d 从震中和 TNT 当量 E_TNT 随时间变化，特别是与平移波速度相关，可以计算垂直加速度。',
    p19: '根据（引用），一旦垂直加速度的幅度达到地表重力的 5%，9.81 m * (s)^-2，就会在该时间点变得微不足道',
    p20: '关于海啸，陨石撞击会暂时将大量水从海洋中移开。这种位移在足够大的规模下会产生从撞击点向外扩展的波浪。为了模拟这些波浪的传播，我们再次基于 shoaling 和格林定律进行了交互式模拟，以找到波浪在海洋深度 h 上向外扩展时的速度 v 和波高 A。',
    p21: '海岸的波高根据 Iida 模型定义了强度：',
    p22: '这可作为潜在损害的替代指标。'
  },
  ar: {
    equations: 'المعادلات',
    learnMore: 'معرفة المزيد',
    p1: 'يستخدم AstroAegis بيانات مسار النيازك من (المصدر 1) للتنبؤ بمدى الأضرار التي قد تسببها الاصطدامات الأرضية.',
    p2: 'تم أخذ توزيعات بيانات السرعة وقطر النيازك من الأجسام السابقة لتوفير بيانات محاكاة دقيقة. تم تتبع مسار النيزك بشكل تكراري. تم تقريب حلول المعادلات التفاضلية غير الخطية من خلال التكرار على خطوات زمنية ذات حجم صغير تعسفي. يمكن لهذه الحلول، بدقة تعسفية (محدودة بموارد الحوسبة)، تقريب زاوية الميل والسرعة والتسارع والموقع عندما يدخل النيزك حافة الغلاف الجوي للأرض. بمجرد التقاطع مع الغلاف الجوي للأرض، تم تحديد تآكل الحرارة وتدهور كتلة النيزك كمعدلات بالنسبة للوقت، وتم تحديثها بشكل تكراري، وتنتهي عند الاصطدام.',
    p3: 'يمكن أن يتجاوز الضغط على الحافة الأمامية للنيزك قوة المادة، مما يؤدي إلى تدهور كتلة الأجسام القريبة من الأرض الصغيرة. وفقًا لوكالة ناسا، إذا كان نصف قطر دخول الجسم إلى الغلاف الجوي أصغر من نصف قطر حرج محدد:',
    p4: 'سيتفتت إلى قطع دون تأثير زلزالي أو مائي كبير قبل الاصطدام، لذلك ينتهي تحليلنا هنا. إذا كان أكبر، تم تحديد معدل تغير الكتلة بحيث يمكن تمثيل الكتلة والحجم عند الاصطدام بدقة. تم تعريف هذه المعدلات سابقًا، لكن النماذج السابقة تفترض مساحة مقطع عرضي ثابتة. سعينا لتحسين هذه المحاكاة من خلال تحديث مساحة المقطع العرضي بمرور الوقت لنمذجة سلوك أكثر واقعية.',
    p5: 'من خلال تحديد المسافة من الحافة الأمامية للنيزك a واستخدام معادلة سبق تعريفها تتعلق بمعادلة التآكل الكلاسيكية لـ Brohnsten:',
    p6: 'إلى مساحة المقطع العرضي الحادث:',
    p7: 'تم تحديد المسافة من مركز النيزك القادم إلى حافته الأمامية الجديدة. هذا، جنبًا إلى جنب مع معدل تغير الكتلة بالنسبة للمسافة من الحافة الأمامية:',
    p8: 'تم استخدامه لتطوير معدل تغير الكتلة الأكثر كثافة بمرور الوقت، مع مراعاة تغير مساحة المقطع العرضي مع تآكل الحافة الأمامية.',
    p9: 'يمكن تعريف المصطلحات المدرجة في هذه المعدلات كما يلي.',
    p10: 'على افتراض زاوية ميل ثابتة بالنسبة لمستوى أفقي محلي، تم تحديد بيانات السرعة وحجمها عند الاصطدام. يمثل الاصطدام هنا تقاطع المسافة بعد نقطة الدخول إلى الغلاف الجوي وبيانات الارتفاع الجغرافي عند موضع الاصطدام.',
    p11: 'تسمح لنا معلمات الاصطدام بتقريب الطاقة الحركية للاصطدام:',
    p12: 'والتي تم تحويلها بعد ذلك إلى ما يعادل TNT، كمقياس أكثر واقعية. تم استخدام طاقة الاصطدام، جنبًا إلى جنب مع الحجم المتبقي للنيزك وزاوية الاصطدام، لتصنيف حجم وشكل الفوهة. تعتمد هذه الفوهة بشكل ملحوظ على كثافة السطح الحادث، والتي تم الحصول عليها من بيانات مختبر لورانس ليفرمور الوطني. عند الاصطدام بالماء، تنهار الفوهة تقريبًا على الفور، مما يخلق موجات تصل إلى مستوى تسونامي. عند الاصطدام بالأرض، تنهار فوهة الاصطدام بسرعة إلى شكلها النهائي المستقر. للعثور على الشكل والحجم النهائيين للفوهة، كان علينا حساب قطر الفوهة الانتقالية.',
    p13: 'يمكن حساب القطر النهائي للمحور العمودي على الاصطدام بسهولة:',
    p14: 'للعثور على الشكل، وجدنا انحراف زاوية السقوط عن العمودي وقمنا بتوسيع الطول الموازي للاصطدام بواسطة دالة هندسية للزاوية من العمودي.',
    p15: 'نظرًا لوجود بيانات قليلة على الأرض حول اصطدامات النيازك، تم تصنيف كل كثافة تحت ثلاث قيم منفصلة للكفاءات الزلزالية.',
    p16: 'واحدة للصخور البلورية، وواحدة للصخور الرسوبية، وواحدة للماء. هذه هي الفئات الثلاث التي تم تحديد تقديرات لها. يمكن أن تحدد طاقة الاصطدام والكفاءة الزلزالية حجم النشاط الزلزالي على مقياس ريختر من خلال المعادلات التالية.',
    p17: 'بالإضافة إلى ذلك، لحساب السرعة الرأسية لموجة s المستعرضة من الزلزال، تذكر المصادر (استشهاد) صيغة تجريبية:',
    p18: 'مع تغير المسافة d من مركز الزلزال وما يعادل TNT E_TNT مع الوقت، خاصة بالنسبة لسرعة الموجة الانتقالية، يمكن حساب التسارع الرأسي.',
    p19: 'وفقًا (لاستشهاد)، تصبح موجات s تافهة بمجرد أن يصل مقدار التسارع الرأسي إلى 5% من جاذبية السطح، 9.81 م * (ث)^-2 يحدث في الوقت',
    p20: 'فيما يتعلق بأمواج تسونامي، تتسبب اصطدامات النيازك مؤقتًا في إزاحة كميات كبيرة من المياه من المحيطات. يمكن أن ينتج عن هذا الإزاحة، على نطاق واسع بما فيه الكفاية، موجات تنتشر شعاعيًا من موضع الاصطدام. لنمذجة انتشار هذه الموجات، أجرينا مرة أخرى محاكاة تفاعلية بناءً على مبادئ shoaling وقانون Green للعثور على السرعة v وارتفاع الموجة A مع توسع الموجات للخارج فوق عمق المحيط h.',
    p21: 'يحدد ارتفاع الموجة عند الساحل شدة وفقًا لنموذج Iida:',
    p22: 'والتي تعمل كبديل للأضرار المحتملة.'
  }
  // Add other languages here (fr, ru, zh, ar, ...)
})

// Use your actual language state here:
function t(key) {
  let lang = language.value
  // Fallback to 'en' if language is not found
  if (!translations[lang]) {
    console.warn(`Language '${lang}' not found, falling back to 'en'`)
    lang = 'en'
  }
  console.log('Current language:', lang)
  if (translations[lang] && translations[lang][key]) return translations[lang][key]
  if (translations.en && translations.en[key]) return translations.en[key]
  return key
}

const equations = [
  `$$r_{\\text{crit}}=100\\Big(\\frac{P_{surface}}{1\\ 00000\\ kPa}\\Big)\\Big(\\frac{\\rho_m}{0.4\\ g\\cdot cm^{-3}}\\Big)^{-1}\\Big(\\frac{g_{min}}{9.81\\ m\\cdot s^{-2}}\\Big)^{-1}(\\sin(\\theta)\\sqrt{2})^{-1}$$`,
  `$$P_{\\text{surface}}=\\frac{\\frac{dv}{dt}m}{A}=\\frac{-0.5C_D\\rho_{atm}A|v|\\vec{v}-g\\hat{e}}{A}$$`,
  `$$\\xi \\frac{dm}{dt} = -\\frac{1}{2}C_H\\rho_{\\text{atm}}Av^3$$`,
  `$$A(a)=\\pi(2aR-a^2)$$`,
  `$$\\frac{dm}{da}=\\frac{\\pi}{3}\\rho_{\\text{met}}(-6aR+3a^2)$$`,
  `$$\\frac{da}{dt}=\\frac{-3\\rho_{atm}C_Hv^3}{4\\rho_m\\xi}+\\frac{(42R\\rho_{atm}C_Hv^3(\\frac{\\rho_m\\xi}{\\rho_{atm}C_Hv^3t})^3+9(\\frac{\\rho_m\\xi}{\\rho_{atm}C_Hv^3t^2})\\rho_m\\xi}{8\\rho_m\\xi(\\frac{\\rho_m\\xi}{\\rho_{atm}C_Hv^3t})^3\\sqrt{(3R)^2+\\frac{21R\\rho_{atm}C_Hv^3t}{\\rho_m\\xi}+(\\frac{3\\rho_{atm}C_Hv^3t}{2\\rho_m\\xi})^2}}$$`,
  `$$\\frac{dm}{dt} = \\frac{dm}{da}\\frac{da}{dt}$$`,
  `$$V_0 = \\frac{4}{3}\\pi R^3$$`,
  `$$V = V_0 - \\int_0^a\\pi(2bR-b^2)db = V_0 - \\pi(a^2R-\\frac{a^3}{3})$$`,
  `$$m=V\\rho_{\\text{met}}$$`,
  `$$h=\\sqrt{x^2+y^2+z^2}-R_{pl}$$`,
  `$$T(h):= \\begin{cases}-131.21+0.00299h & h>25000\\\\-56.46 &11000<h<25000\\\\15.04-0.000649h & h<11000\\end{cases}$$`,
  `$$P(h):= \\begin{cases}2.488-\\Big(\\frac{T(h)+273.1}{216.6}\\Big)^{-11.388} & h>25000\\\\22.65e^{1.73-0.000157h} &11000<h<25000\\\\101.29\\Big(\\frac{T(h)+273.1}{288.08}\\Big)^{5.256} & h<11000\\end{cases}$$`,
  `$$\\rho_{atm}=\\frac{P(h)}{0.2869+(T(h)+273.1)}$$`,
  `$$KE = \\frac{1}{2}mv^2$$`,
  
    `$$D_{\\text{tr}} = 0.70253\\left(\\frac{\\rho_{\\text{met}}}{\\rho_{\\text{surf}}}\\right)^{1/3} d_{\\text{met}}^{0.78} v_{\\text{met}}^{0.44} (\\sin(\\theta))^{1/3}$$`,
  //`$$D_{\text{f}} = \begin{cases} 1.25 D_{\text{tr}} & D_{\text{tr}} < 3\,\text{km} \\ 1.17 \frac{D_{\text{tr}}^{1.13}}{(3\,\text{km})^{0.13}} & D_{\text{tr}} > 3\,\text{km} \end{cases}$$`,
  `$$\\begin{align}k_{\\text{H}_2\\text{O}} &= 0.0003\\\\k_{\\text{unc}} &= 0.01\\\\k_{\\text{cons}} &= 0.05\\end{align}$$`,
  `$$E_s=KE\\cdot k$$`,
  `$$M = \\frac{\\log(E_s)-11.8}{1.5}$$`,
  `$$v(d,E_{TNT})=a_0d^bE_{TNT}^c$$`,
  `$$\\frac{dv}{dt} = \\frac{E_0^ca_0(2c-b)(v_{\\rightarrow}t)^b}{4^c\\pi^cv_{\\rightarrow}^{2c}t^{2c+1}}$$`,
  `$$t=\\Big(\\frac{0.4905\\cdot4^c\\pi^cv_{\\rightarrow}^{2c-b}}{E_0^ca_0(2c-b)}\\Big)^{1/(b-2c-1)}$$`,
  `$$v=\\sqrt{gh}$$`,
  `$$A\\propto \\frac{1}{h^{1/4}}$$`,
  `$$i = \\log_2(A_{\\text{max}})$$`
]

function buildInfoContent() {
  // Paragraph keys in order, insert equations after certain paragraphs
  const ps = [
    'p1','p2','p3', // eq 0,1
    'p4','p5', // eq 2
    'p6', // eq 3
    'p7', // eq 4
    'p8', // eq 5,6
    'p9', // eq 7,8,9
    'p10','p11', // eq 10
    'p12', // eq 11,12,13
    'p13', // eq 14
    'p14','p15', // eq 15
    'p16', // eq 16,17
    'p17', // eq 18
    'p18', // eq 19
    'p19', // eq 20
    'p20', // eq 21,22
    'p21', // eq 23
    'p22'
  ]
  let html = `<h2 class='text-xl font-bold mb-4'>${t('equations')}</h2>`
  for (let i = 0; i < ps.length; i++) {
    html += `<p>${t(ps[i])}</p>`
    // Insert equations at the right spots
    if (i === 2) { html += equations[0] + equations[1] } // after p3
    if (i === 3) { html += equations[2] } // after p4
    if (i === 4) { html += equations[3] } // after p5
    if (i === 5) { html += equations[4] } // after p6
    if (i === 6) { html += equations[5] + equations[6] } // after p7
    if (i === 7) { html += equations[7] + equations[8] + equations[9] } // after p8
    if (i === 9) { html += equations[10] } // after p10
    if (i === 10) { html += equations[11] + equations[12] + equations[13] } // after p11
    if (i === 12) { html += equations[14] } // after p13
    if (i === 14) { html += equations[15] } // after p15
    if (i === 15) { html += equations[16] + equations[17] } // after p16
    if (i === 16) { html += equations[18] } // after p17
    if (i === 17) { html += equations[19] } // after p18
    if (i === 18) { html += equations[20] } // after p19
    if (i === 19) { html += equations[21] + equations[22] } // after p20
    if (i === 20) { html += equations[23] } // after p21
  }
  return html
}

const infoContent = computed(() => buildInfoContent())

watch(infoContent, () => {
  nextTick(() => {
    if (window.MathJax) window.MathJax.typeset()
  })
})

onMounted(() => {
  if (window.MathJax) window.MathJax.typeset()
})
</script>

<template>
  <div class="min-h-screen bg-blue-50 text-gray-900">
    <main class="mt-16 p-4 max-w-3xl mx-auto">
      <h1 class="text-2xl font-bold mb-4">{{ t('learnMore') }}</h1>
      <div v-html="infoContent"></div>
    </main>
  </div>
</template>