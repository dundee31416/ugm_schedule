<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-semibold">Filters</h2>
      <button
        @click="$emit('clear-filters')"
        class="text-sm text-blue-600 hover:text-blue-800"
      >
        Clear All
      </button>
    </div>

    <div class="space-y-4">
      <!-- League Filter (REQUIRED - First) -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          League <span class="text-red-500">*</span>
        </label>
        <select
          :value="leagueId"
          @change="onLeagueChange"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option :value="null">Select a league...</option>
          <option v-for="league in sortedLeagues" :key="league.id" :value="league.id">
            {{ formatLeagueName(league) }}
          </option>
        </select>
      </div>

      <!-- Team Filter (Single Searchable) -->
      <div class="relative">
        <label class="block text-sm font-medium text-gray-700 mb-1">Team</label>
        <input
          type="text"
          v-model="teamSearchQuery"
          @focus="showTeamDropdown = true"
          @blur="handleTeamBlur"
          placeholder="Search teams..."
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <div
          v-if="showTeamDropdown && filteredTeams.length > 0"
          class="absolute z-10 mt-1 w-full max-h-60 overflow-auto bg-white border border-gray-300 rounded-lg shadow-lg"
        >
          <div
            v-for="team in filteredTeams"
            :key="team.id"
            @mousedown="selectTeam(team)"
            class="px-3 py-2 cursor-pointer hover:bg-blue-50"
          >
            {{ team.name }}
          </div>
        </div>
      </div>

      <!-- Date Filter (Single Date Dropdown) -->
      <div v-if="leagueId">
        <label class="block text-sm font-medium text-gray-700 mb-1">Game Date</label>
        <select
          :value="gameDate"
          @change="onDateChange"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option :value="null">All Dates</option>
          <option v-for="date in availableDates" :key="date" :value="date">
            {{ formatDate(date) }}
          </option>
        </select>
      </div>

      <!-- Field Filter -->
      <div v-if="availableFields.length > 0">
        <label class="block text-sm font-medium text-gray-700 mb-1">Field</label>
        <select
          :value="fieldId"
          @change="onFieldChange"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option :value="null">All Fields</option>
          <option v-for="field in availableFields" :key="field.id" :value="field.id">
            {{ field.name }}
            <span v-if="field.city">({{ field.city }})</span>
          </option>
        </select>
      </div>

      <!-- Status Filter -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
        <select
          :value="status"
          @change="onStatusChange"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option :value="null">All Statuses</option>
          <option value="upcoming">Upcoming</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Team, Field, League, GameStatus } from '@/types'

const props = defineProps<{
  leagues: League[]
  teams: Team[]
  fields: Field[]
  availableFields: Field[]
  availableDates: string[]
  leagueId: number | null
  teamId: number | null
  fieldId: number | null
  gameDate: string | null
  status: GameStatus | null
}>()

const emit = defineEmits<{
  'update:leagueId': [value: number | null]
  'update:teamId': [value: number | null]
  'update:fieldId': [value: number | null]
  'update:gameDate': [value: string | null]
  'update:status': [value: GameStatus | null]
  'clear-filters': []
}>()

const teamSearchQuery = ref('')
const showTeamDropdown = ref(false)

const sortedLeagues = computed(() => {
  return [...props.leagues].sort((a, b) => {
    const yearA = extractYear(a.name)
    const yearB = extractYear(b.name)
    return yearB - yearA
  })
})

const filteredTeams = computed(() => {
  const sortedTeams = [...props.teams].sort((a, b) =>
    a.name.localeCompare(b.name, 'fr', { sensitivity: 'base' })
  )

  if (!teamSearchQuery.value) {
    return sortedTeams.slice(0, 100)
  }

  const query = teamSearchQuery.value.toLowerCase()
  return sortedTeams
    .filter(team => team.name.toLowerCase().includes(query))
    .slice(0, 100)
})

function extractYear(name: string): number {
  const yearMatch = name.match(/(\d{4})/)
  return yearMatch ? parseInt(yearMatch[1]) : 0
}

function formatLeagueName(league: League): string {
  const year = extractYear(league.name)
  return year ? `${year} - ${league.name}` : league.name
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function onLeagueChange(event: Event) {
  const target = event.target as HTMLSelectElement
  const value = target.value ? parseInt(target.value) : null
  emit('update:leagueId', value)
}

function onDateChange(event: Event) {
  const target = event.target as HTMLSelectElement
  emit('update:gameDate', target.value || null)
}

function onFieldChange(event: Event) {
  const target = event.target as HTMLSelectElement
  const value = target.value ? parseInt(target.value) : null
  emit('update:fieldId', value)
}

function onStatusChange(event: Event) {
  const target = event.target as HTMLSelectElement
  emit('update:status', (target.value as GameStatus) || null)
}

function selectTeam(team: Team) {
  teamSearchQuery.value = team.name
  emit('update:teamId', team.id)
  showTeamDropdown.value = false
}

function handleTeamBlur() {
  setTimeout(() => {
    showTeamDropdown.value = false
  }, 200)
}
</script>
