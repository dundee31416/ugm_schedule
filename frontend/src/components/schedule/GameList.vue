<template>
  <div class="game-list">
    <div v-if="loading" class="text-center py-8">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <p class="mt-2 text-gray-600">Loading games...</p>
    </div>

    <div v-else-if="error" class="text-center py-8 text-red-600">
      <p>{{ error }}</p>
      <button
        @click="$emit('retry')"
        class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Retry
      </button>
    </div>

    <div v-else-if="games.length === 0" class="text-center py-8 text-gray-600">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
      </svg>
      <p class="mt-4">No games found</p>
      <p class="text-sm mt-2">Try adjusting your filters</p>
    </div>

    <div v-else class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <GameCard
        v-for="game in games"
        :key="game.id"
        :game="game"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Game } from '@/types'
import GameCard from './GameCard.vue'

defineProps<{
  games: Game[]
  loading: boolean
  error: string | null
}>()

defineEmits<{
  retry: []
}>()
</script>
