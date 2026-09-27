<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([]); const wid = ref(1); const fid = ref(1)
const prCm = ref(0); const out = ref(null); const err = ref('')
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
  syncPr()
})
function syncPr(){
  const f = fabrics.value.find(x => x.id === fid.value)
  prCm.value = f ? Number(f.pattern_repeat_cm || 0) : 0
}
watch(fid, syncPr)
function params(){
  const p = new URLSearchParams({ window_id: wid.value, fabric_id: fid.value })
  if (prCm.value !== null && prCm.value !== '') p.set('pattern_repeat_cm', Number(prCm.value))
  return p
}
async function go(save){
  err.value = ''
  try {
    out.value = save
      ? await postJSON('/api/estimate', { window_id: wid.value, fabric_id: fid.value, save: true, pattern_repeat_cm: Number(prCm.value || 0) })
      : await getJSON(`/api/estimate?${params().toString()}`)
  } catch (e) {
    out.value = null
    err.value = e.message
  }
}
</script>
<template><div class="page"><h1>算料</h1>
<select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<label>花高(cm) <input v-model.number="prCm" type="number" min="0" step="0.1" /><span class="hint">0 = 不按花高对齐</span></label>
<button @click="go(false)">试算</button><button @click="go(true)">保存</button>
<p v-if="err" class="err">{{ err }}</p>
<PanelCut v-if="out" :panels="out.panels" :cut-height="out.cut_height" :meters="out.meters" :gross-cut-height="out.gross_cut_height" :pattern-repeat-cm="out.pattern_repeat_cm" />
</div></template>
