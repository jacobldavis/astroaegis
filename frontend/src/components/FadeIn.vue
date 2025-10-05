<template>
  <div
    class="opacity-0 translate-y-4 transition-all duration-1750 ease-out"
    :class="{ 'opacity-100 translate-y-0': isVisible }"
    ref="fadeElement"
  >
    <slot></slot>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const fadeElement = ref(null);
const isVisible = ref(false);

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          isVisible.value = true;
          observer.unobserve(entry.target); // Only trigger once
        }
      });
    },
    { threshold: 0.2 } // Adjust when it should start fading in
  );

  if (fadeElement.value) observer.observe(fadeElement.value);
});
</script>
