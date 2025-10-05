<script setup>
import { ref, onMounted, onBeforeUnmount, reactive } from 'vue'
import { useAccessibilityStore } from '../stores/accessibilityStore.js'
import Header from '../components/Header.vue'
import heroImage from '../assets/images/hero.jpg'
import FadeIn from "../components/FadeIn.vue";

const accessibility = useAccessibilityStore()
accessibility.initLanguage()

const translations = reactive({
    en: {
    subText: "Visualizing and Mitigating Meteor Impacts", 
    visualization: "Visualization", 
    mitigation: "Mitigation",
    seismicAnalysis: "Seismic Analysis",
    impactAnalysis: "Impact Analysis",
    obliteration: "Obliteration",
    deflection: "Deflection",
    begin: "Begin Visualization",
    seismicAnalysisText: "When a meteor collides with Earth, the force of impact sends powerful seismic waves rippling through the planet’s crust and, if it strikes the ocean, can displace massive volumes of water. Our Seismic Analysis module visualizes how this energy travels—showing potential earthquakes and the generation of tsunamis radiating outward from the impact site.",
    impactAnalysisText: "The moment a meteor strikes, immense kinetic energy is released into the ground—compressing, heating, and reshaping the surface. Our Impact Analysis module visualizes these near-field effects: crater formation, ground deformation, and heat distribution across the impact zone.",
    obliterationText: "Obliteration aims to destroy or fragment an asteroid that’s too close or too massive to deflect in time. This could involve nuclear explosives, high-energy lasers, or other intense energy sources designed to break the asteroid apart or vaporize key sections.",
    deflectionText: "Deflection involves altering the asteroid's trajectory to ensure it safely bypasses Earth. Techniques may include kinetic impactors, which collide with the asteroid to change its path, or gravity tractors that use a spacecraft's gravitational pull to gradually shift the asteroid's course over time.",
    },

    es: {
    subText: "Visualizando y Mitigando Impactos de Meteoros", 
    visualization: "Visualización", 
    mitigation: "Mitigación",
    seismicAnalysis: "Análisis Sísmico",
    impactAnalysis: "Análisis de Impacto",
    obliteration: "Obliteración",
    deflection: "Desviación",
    begin: "Comenzar Visualización",
    seismicAnalysisText: "Cuando un meteoro choca con la Tierra, la fuerza del impacto envía poderosas ondas sísmicas que se propagan a través de la corteza del planeta y, si golpea el océano, puede desplazar enormes volúmenes de agua. Nuestro módulo de Análisis Sísmico visualiza cómo viaja esta energía, mostrando posibles terremotos y la generación de tsunamis que irradian desde el sitio de impacto.",
    impactAnalysisText: "En el momento en que un meteoro golpea, se libera una inmensa energía cinética en el suelo, comprimiendo, calentando y remodelando la superficie. Nuestro módulo de Análisis de Impacto visualiza estos efectos de campo cercano: formación de cráteres, deformación del terreno y distribución del calor en la zona de impacto.",
    obliterationText: "La obliteración tiene como objetivo destruir o fragmentar un asteroide que está demasiado cerca o es demasiado masivo para desviarlo a tiempo. Esto podría implicar explosivos nucleares, láseres de alta energía u otras fuentes de energía intensas diseñadas para romper el asteroide o vaporizar secciones clave.",
    deflectionText: "La desviación implica alterar la trayectoria del asteroide para asegurar que pase de manera segura por la Tierra. Las técnicas pueden incluir impactores cinéticos, que colisionan con el asteroide para cambiar su trayectoria, o tractores gravitacionales que utilizan la atracción gravitacional de una nave espacial para desplazar gradualmente el curso del asteroide con el tiempo.",
    },

    fr: {
    subText: "Visualisation et Atténuation des Impacts de Météores", 
    visualization: "Visualisation", 
    mitigation: "Atténuation",
    seismicAnalysis: "Analyse Sismique",
    impactAnalysis: "Analyse d’Impact",
    obliteration: "Oblitération",
    deflection: "Déviation",
    begin: "Commencer la Visualisation",
    seismicAnalysisText: "Lorsqu'une météorite entre en collision avec la Terre, la force de l'impact envoie de puissantes ondes sismiques à travers la croûte de la planète et, si elle frappe l'océan, peut déplacer d'énormes volumes d'eau. Notre module d'Analyse Sismique visualise la propagation de cette énergie, montrant les tremblements de terre potentiels et la génération de tsunamis irradiant depuis le site d'impact.",
    impactAnalysisText: "Le moment où une météorite frappe, une immense énergie cinétique est libérée dans le sol, comprimant, chauffant et remodelant la surface. Notre module d'Analyse d'Impact visualise ces effets de champ proche : formation de cratères, déformation du sol et distribution de la chaleur dans la zone d'impact.",
    obliterationText: "L'oblitération vise à détruire ou fragmenter un astéroïde trop proche ou trop massif pour être dévié à temps. Cela pourrait impliquer des explosifs nucléaires, des lasers à haute énergie ou d'autres sources d'énergie intenses conçues pour briser l'astéroïde ou vaporiser des sections clés.",
    deflectionText: "La déviation consiste à modifier la trajectoire de l'astéroïde pour s'assurer qu'il contourne la Terre en toute sécurité. Les techniques peuvent inclure des impacteurs cinétiques, qui entrent en collision avec l'astéroïde pour changer sa trajectoire, ou des tracteurs gravitationnels qui utilisent la traction gravitationnelle d'un vaisseau spatial pour déplacer progressivement la trajectoire de l'astéroïde au fil du temps.",
    },

    ru: {
    subText: "Визуализация и Смягчение Последствий Метеоритов", 
    visualization: "Визуализация", 
    mitigation: "Смягчение",
    seismicAnalysis: "Сейсмический анализ",
    impactAnalysis: "Анализ воздействия",
    obliteration: "Уничтожение",
    deflection: "Отклонение",
    begin: "Начать визуализацию",
    seismicAnalysisText: "Когда метеорит сталкивается с Землей, сила удара посылает мощные сейсмические волны, распространяющиеся по коре планеты, и, если он ударяется в океан, может сместить огромные объемы воды. Наш модуль сейсмического анализа визуализирует, как эта энергия распространяется, показывая потенциальные землетрясения и образование цунами, исходящих от места удара.",
    impactAnalysisText: "В момент удара метеорита в землю высвобождается огромная кинетическая энергия, сжимающая, нагревающая и изменяющая поверхность. Наш модуль анализа воздействия визуализирует эти эффекты ближнего поля: образование кратеров, деформацию грунта и распределение тепла по зоне удара.",
    obliterationText: "Уничтожение направлено на разрушение или фрагментацию астероида, который слишком близко или слишком массивен, чтобы его можно было отклонить вовремя. Это может включать ядерные взрывчатые вещества, высокоэнергетические лазеры или другие интенсивные источники энергии, предназначенные для разрушения астероида или испарения ключевых участков.",
    deflectionText: "Отклонение включает изменение траектории астероида, чтобы он безопасно обошел Землю. Техники могут включать кинетические импакторы, которые сталкиваются с астероидом, чтобы изменить его путь, или гравитационные тягачи, которые используют гравитационное притяжение космического корабля для постепенного изменения курса астероида со временем.",
    },

    zh: {
    subText: "可视化与缓解陨石撞击", 
    visualization: "可视化", 
    mitigation: "缓解",
    seismicAnalysis: "地震分析",
    impactAnalysis: "影响分析",
    obliteration: "湮灭",
    deflection: "偏转",
    begin: "开始可视化",
    seismicAnalysisText: "当陨石与地球碰撞时，冲击力会在行星的地壳中掀起强烈的地震波，如果它撞击海洋，还可能会位移大量的水。我们的地震分析模块可视化了这些能量的传播方式，展示了从撞击点辐射出来的潜在地震和海啸的生成。",
    impactAnalysisText: "当陨石撞击时，巨大的动能会释放到地面——压缩、加热并重塑地表。我们的影响分析模块可视化了这些近场效应：陨石坑的形成、地面的变形以及整个撞击区的热量分布。",
    obliterationText: "湮灭旨在摧毁或分解过于接近或过于庞大而无法及时偏转的小行星。这可能涉及核爆炸物、高能激光或其他旨在将小行星击碎或蒸发关键部分的强大能量源。",
    deflectionText: "偏转涉及改变小行星的轨道，以确保它安全地绕过地球。技术可能包括动能撞击器，它们与小行星碰撞以改变其路径，或引力拖船，利用航天器的引力逐渐改变小行星的轨道。",
    },

    ar: {
    subText: "تصور وتخفيف تأثيرات النيازك", 
    visualization: "التصور", 
    mitigation: "التخفيف",
    seismicAnalysis: "التحليل الزلزالي",
    impactAnalysis: "تحليل الأثر",
    obliteration: "الإبادة",
    deflection: "الانحراف",
    begin: "بدء التصور",
    seismicAnalysisText: "عندما يصطدم نيزك بالأرض، فإن قوة الاصطدام ترسل موجات زلزالية قوية تمتد عبر قشرة الكوكب، وإذا ضرب المحيط، يمكن أن يحرك كميات هائلة من الماء. يقوم وحدة التحليل الزلزالي لدينا بتصور كيفية انتقال هذه الطاقة - مظهراً الزلازل المحتملة وتوليد التسونامي الذي يشع من موقع الاصطدام.",
    impactAnalysisText: "عندما يصطدم نيزك، يتم إطلاق طاقة حركية هائلة في الأرض - مما يضغط ويسخن ويعيد تشكيل السطح. تقوم وحدة تحليل الأثر لدينا بتصور هذه التأثيرات القريبة: تكوين الفوهات، تشوه الأرض، وتوزيع الحرارة عبر منطقة الاصطدام.",
    obliterationText: "الابادة تهدف إلى تدمير أو تفتيت كويكب قريب جدًا أو ضخم جدًا بحيث لا يمكن تحويل مساره في الوقت المناسب. قد يشمل ذلك المتفجرات النووية، والليزر عالي الطاقة، أو مصادر طاقة مكثفة أخرى مصممة لتفتيت الكويكب أو تبخير أقسامه الرئيسية.",
    deflectionText: "الانحراف ينطوي على تغيير مسار الكويكب لضمان تجاوزه للأرض بأمان. قد تشمل التقنيات مؤثرات حركية، التي تصطدم بالكويكب لتغيير مساره، أو جرارات الجاذبية التي تستخدم الجاذبية الخاصة بمركبة فضائية لتغيير مسار الكويكب تدريجيًا مع مرور الوقت.",
    }
})

const t = (key) => translations[accessibility.language][key] || key

const scrollY = ref(0)

const handleScroll = () => {
  scrollY.value = window.scrollY
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <div class="min-h-screen text-gray-900">
    <section
    class="relative h-[100vh] flex items-center justify-center text-white overflow-hidden"
    :style="{
        backgroundImage: `url(${heroImage})`,
        backgroundSize: 'cover',
        backgroundAttachment: 'fixed',
        backgroundPosition: `center ${-scrollY.value * 0.3}px`,
    }"
    >
    <div class="relative z-10 p-8 rounded text-center flex flex-col items-center gap-6 h-145">
        <h1 class="text-4xl md:text-6xl font-bold">AstroAegis</h1>
        <p class="mt-4 text-lg md:text-2xl">{{ t('subText') }}</p>
        <router-link
        to="/visualization"
        class="px-6 py-3 bg-black hover:bg-white hover:text-black text-white rounded transition"
        >
        {{ t('begin') }}
        </router-link>
    </div>
    </section>


  <section class="relative overflow-hidden">
    <FadeIn>
  <div class="relative flex flex-col">

  <div class="min-h-[60vh] bg-white text-black flex flex-col items-center justify-start pt-12 pb-6">
      <h1 class="text-4xl font-bold mb-8 text-center">{{ t('visualization') }}</h1>

  <div class="flex flex-col md:flex-row gap-6 w-full max-w-4xl mx-auto mt-8 mb-12">

      <div class="flex-1 bg-black text-white rounded-xl shadow-lg p-6 flex flex-col items-center justify-center hover:scale-105 transition-transform duration-300">
        <h3 class="text-2xl font-semibold mb-4">{{ t('seismicAnalysis') }}</h3>
        <p class="text-sm text-gray-200 text-center mb-4">
        {{ t('seismicAnalysisText') }}
        </p>
      </div>

      <div class="flex-1 bg-black text-white rounded-xl shadow-lg p-6 flex flex-col items-center justify-center hover:scale-105 transition-transform duration-300">
        <h3 class="text-2xl font-semibold mb-4">{{ t('impactAnalysis') }}</h3>
        <p class="text-sm text-gray-200 text-center mb-4">
        {{t('impactAnalysisText') }}
        </p>
      </div>

      </div>
      <div class="h-10"></div>
    </div>

  <div class="min-h-[60vh] bg-black text-white flex flex-col items-center pt-12 pb-10">
    <h2 class="text-4xl font-bold mb-8 text-center">{{ t('mitigation') }}</h2>
    <div class="flex flex-col md:flex-row gap-6 w-full max-w-4xl mx-auto mt-8 mb-12">
      <div class="flex-1 bg-white text-black rounded-xl shadow-lg p-6 flex flex-col items-center justify-center hover:scale-105 transition-transform duration-300">
        <h3 class="text-2xl font-semibold mb-4">{{ t('obliteration') }}</h3>
        <p class="text-sm text-gray-700 text-center mb-4">
        {{t('obliterationText') }}
        </p>
      </div>
      <div class="flex-1 bg-white text-black rounded-xl shadow-lg p-6 flex flex-col items-center justify-center hover:scale-105 transition-transform duration-300">
        <h3 class="text-2xl font-semibold mb-4">{{ t('deflection') }}</h3>
        <p class="text-sm text-gray-700 text-center mb-4">
        {{t('deflectionText') }}
        </p>
      </div>
    </div>
  </div>

        </div>
    </FadeIn>
    </section>
  </div>
</template>
