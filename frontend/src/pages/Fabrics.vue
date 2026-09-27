<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
const items = ref([])
const drafts = ref({})
const saving = ref({})
const errs = ref({})
onMounted(async () => {
  items.value = (await getJSON('/api/fabrics')).items
  for (const f of items.value) drafts.value[f.id] = Number(f.pattern_repeat_cm || 0)
})
async function saveRepeat(f){
  errs.value[f.id] = ''
  const v = Number(drafts.value[f.id])
  if (!(v >= 0)) { errs.value[f.id] = '花高不能为负'; return }
  saving.value[f.id] = true
  try {
    const updated = await patchJSON(`/api/fabrics/${f.id}`, { pattern_repeat_cm: v })
    Object.assign(f, updated)
  } catch (e) {
    errs.value[f.id] = e.message
  } finally {
    saving.value[f.id] = false
  }
}
</script>
<template><div class="page"><h1>面料</h1>
<div v-for="f in items" :key="f.id" class="fab">
  <span>{{ f.name }} 门幅{{ f.fabric_width }}m</span>
  <label>默认花高(cm)
    <input v-model.number="drafts[f.id]" type="number" min="0" step="0.1" />
  </label>
  <button :disabled="saving[f.id]" @click="saveRepeat(f)">保存花高</button>
  <small class="hint">只影响此后的试算，不改已保存编号</small>
  <p v-if="errs[f.id]" class="err">{{ errs[f.id] }}</p>
</div>
</div></template>
