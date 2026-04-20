<template>
  <div class="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
    <div class="flex justify-between items-start mb-2">
      <div class="flex-1">
        <div class="text-sm text-gray-500 mb-1">
          {{ formatDate(game.game_date) }}
          <span v-if="game.game_time" class="ml-2">{{ formatTime(game.game_time) }}</span>
        </div>
        <div class="font-semibold text-lg">
          {{ game.home_team.name }}
          <span v-if="game.home_score !== null" class="ml-2 text-blue-600">{{ game.home_score }}</span>
        </div>
        <div class="font-semibold text-lg">
          {{ game.away_team.name }}
          <span v-if="game.away_score !== null" class="ml-2 text-blue-600">{{ game.away_score }}</span>
        </div>
      </div>
      <div>
        <span
          :class="statusClass"
          class="px-2 py-1 rounded text-xs font-medium"
        >
          {{ game.status }}
        </span>
      </div>
    </div>

    <div v-if="game.field" class="text-sm text-gray-600 mt-2">
      <svg class="inline-block w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
      </svg>
      {{ game.field.name }}
      <span v-if="game.field.city" class="text-gray-500">- {{ game.field.city }}</span>
    </div>

    <div class="text-xs text-gray-500 mt-2">
      {{ game.league.name }}
    </div>

    <div v-if="game.notes" class="text-sm text-gray-600 mt-2 italic">
      {{ game.notes }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Game } from '@/types'

const props = defineProps<{
  game: Game
}>()

const statusClass = computed(() => {
  switch (props.game.status) {
    case 'upcoming':
      return 'bg-blue-100 text-blue-800'
    case 'completed':
      return 'bg-green-100 text-green-800'
    case 'cancelled':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
})

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function formatTime(timeString: string): string {
  // timeString is in HH:MM:SS format
  const [hours, minutes] = timeString.split(':')
  const hour = parseInt(hours, 10)
  const ampm = hour >= 12 ? 'PM' : 'AM'
  const displayHour = hour % 12 || 12
  return `${displayHour}:${minutes} ${ampm}`
}
</script>
