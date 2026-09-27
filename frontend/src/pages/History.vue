<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1>
<ul><li v-for="r in items" :key="r.id">
  <strong>#{{ r.id }}</strong> {{ r.window_name }} / {{ r.fabric_name }}
  <PanelCut
    :panels="r.result?.panels"
    :cut-height="r.result?.cut_height"
    :meters="r.result?.meters"
    :gross-cut-height="r.result?.gross_cut_height ?? 0"
    :pattern-repeat-cm="r.result?.pattern_repeat_cm ?? 0"
  />
</li></ul>
<p class="hint">开放视图保留花高字段；裁高取毛裁高，米数随列表接口返回。</p>
</div></template>
