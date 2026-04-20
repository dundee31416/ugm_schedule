<template>
  <div class="flex gap-2 items-center">
    <div class="flex-1">
      <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
      <input
        v-model="startDateValue"
        type="date"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        @change="onDateChange"
      />
    </div>
    <div class="flex-1">
      <label class="block text-sm font-medium text-gray-700 mb-1">End Date</label>
      <input
        v-model="endDateValue"
        type="date"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        @change="onDateChange"
      />
    </div>
    <button
      v-if="startDateValue || endDateValue"
      @click="clearDates"
      class="mt-6 px-3 py-2 text-sm text-gray-600 hover:text-gray-800"
      title="Clear dates"
    >
      <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  startDate: string | null
  endDate: string | null
}>()

const emit = defineEmits<{
  'update:startDate': [value: string | null]
  'update:endDate': [value: string | null]
}>()

const startDateValue = ref(props.startDate || '')
const endDateValue = ref(props.endDate || '')

function onDateChange() {
  emit('update:startDate', startDateValue.value || null)
  emit('update:endDate', endDateValue.value || null)
}

function clearDates() {
  startDateValue.value = ''
  endDateValue.value = ''
  emit('update:startDate', null)
  emit('update:endDate', null)
}

watch(() => props.startDate, (newValue) => {
  startDateValue.value = newValue || ''
})

watch(() => props.endDate, (newValue) => {
  endDateValue.value = newValue || ''
})
</script>
