<script setup>
defineProps({
  panels: Number,
  cutHeight: Number,
  meters: Number,
  grossCutHeight: { type: Number, default: 0 },
  patternRepeatCm: { type: Number, default: 0 },
})
</script>
<template>
  <div class="panel-cut">
    <div class="panel-row">
      <div v-for="n in Math.min(panels||0,8)" :key="n" class="panel" :style="{height: `${(cutHeight||1)*40}px`}"></div>
    </div>
    <p v-if="patternRepeatCm > 0" class="align-note">毛裁高 {{ grossCutHeight }} m，按花高 {{ patternRepeatCm }} cm 向上对齐 → 裁高 {{ cutHeight }} m</p>
    <p>{{ panels }} 幅 × {{ cutHeight }} m = {{ meters }} m</p>
  </div>
</template>
