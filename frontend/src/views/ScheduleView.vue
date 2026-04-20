<template>
  <div class="min-h-screen bg-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">UGM Schedules</h1>
        <p class="mt-2 text-gray-600">View and filter sports league schedules</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Filter Panel -->
        <div class="lg:col-span-1">
          <FilterPanel
            :leagues="scheduleStore.leagues"
            :teams="scheduleStore.teams"
            :fields="scheduleStore.fields"
            :available-fields="scheduleStore.availableFields"
            :available-dates="scheduleStore.availableDates"
            :league-id="scheduleStore.selectedLeagueId"
            :team-id="scheduleStore.selectedTeamId"
            :field-id="scheduleStore.selectedFieldId"
            :game-date="scheduleStore.selectedDate"
            :status="scheduleStore.selectedStatus"
            @update:league-id="scheduleStore.setLeagueFilter"
            @update:team-id="scheduleStore.setTeamFilter"
            @update:field-id="scheduleStore.setFieldFilter"
            @update:game-date="scheduleStore.setDateFilter"
            @update:status="scheduleStore.setStatusFilter"
            @clear-filters="scheduleStore.clearFilters"
          />
        </div>

        <!-- Game List -->
        <div class="lg:col-span-3">
          <GameList
            :games="scheduleStore.filteredGames"
            :loading="scheduleStore.loading"
            :error="scheduleStore.error"
            @retry="scheduleStore.fetchGames"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useScheduleStore } from '@/stores/schedule'
import FilterPanel from '@/components/schedule/FilterPanel.vue'
import GameList from '@/components/schedule/GameList.vue'

const scheduleStore = useScheduleStore()

onMounted(async () => {
  await scheduleStore.loadAllData()
})
</script>
