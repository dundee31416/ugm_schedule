/**
 * Schedule store for managing games, teams, fields, and leagues.
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Game, Team, Field, League, GameStatus } from '@/types'
import api from '@/services/api'

export const useScheduleStore = defineStore('schedule', () => {
  // State
  const games = ref<Game[]>([])
  const teams = ref<Team[]>([])
  const fields = ref<Field[]>([])
  const leagues = ref<League[]>([])
  const availableDates = ref<string[]>([])
  const availableFields = ref<Field[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Filters
  const selectedLeagueId = ref<number | null>(null)
  const selectedTeamId = ref<number | null>(null)
  const selectedFieldId = ref<number | null>(null)
  const selectedDate = ref<string | null>(null)
  const selectedStatus = ref<GameStatus | null>(null)

  // Computed
  const filteredGames = computed(() => {
    // Note: Filtering is done server-side, so we just return the games
    return games.value
  })

  // Actions
  async function fetchGames() {
    loading.value = true
    error.value = null

    try {
      const params: Record<string, any> = {}

      if (selectedLeagueId.value) params.league_id = selectedLeagueId.value
      if (selectedTeamId.value) params.team_id = selectedTeamId.value
      if (selectedFieldId.value) params.field_id = selectedFieldId.value
      if (selectedDate.value) {
        // Use the selected date as both start and end date to filter for that specific date
        params.start_date = selectedDate.value
        params.end_date = selectedDate.value
      }
      if (selectedStatus.value) params.status = selectedStatus.value

      const response = await api.get<{ games: Game[] }>('/api/v1/games', { params })
      games.value = response.data.games

      // Update available fields based on fetched games
      updateAvailableFields()
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch games'
      console.error('Error fetching games:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchTeams() {
    try {
      const response = await api.get<{ teams: Team[] }>('/api/v1/teams')
      teams.value = response.data.teams
    } catch (err) {
      console.error('Error fetching teams:', err)
    }
  }

  async function fetchFields() {
    try {
      const response = await api.get<{ fields: Field[] }>('/api/v1/fields')
      fields.value = response.data.fields
    } catch (err) {
      console.error('Error fetching fields:', err)
    }
  }

  async function fetchLeagues() {
    try {
      const response = await api.get<{ leagues: League[] }>('/api/v1/leagues')
      leagues.value = response.data.leagues
    } catch (err) {
      console.error('Error fetching leagues:', err)
    }
  }

  async function fetchGameDates(leagueId: number) {
    try {
      const response = await api.get<string[]>('/api/v1/games/dates', {
        params: { league_id: leagueId }
      })
      availableDates.value = response.data
    } catch (err) {
      console.error('Error fetching game dates:', err)
      availableDates.value = []
    }
  }

  // Update available fields based on current games
  function updateAvailableFields() {
    if (games.value.length === 0) {
      availableFields.value = []
      return
    }

    // Get unique field IDs from current games
    const fieldIds = new Set<number>()
    games.value.forEach(game => {
      if (game.field?.id) {
        fieldIds.add(game.field.id)
      }
    })

    // Filter fields to only those present in current games
    availableFields.value = fields.value.filter(field => fieldIds.has(field.id))

    // Clear field filter if selected field is not in available fields
    if (selectedFieldId.value && !fieldIds.has(selectedFieldId.value)) {
      selectedFieldId.value = null
    }
  }

  async function loadAllData() {
    await Promise.all([fetchLeagues(), fetchTeams(), fetchFields()])
    // Don't fetch games initially - require league selection first
  }

  async function setLeagueFilter(leagueId: number | null) {
    selectedLeagueId.value = leagueId
    selectedDate.value = null // Reset date when league changes

    if (leagueId) {
      // Fetch available dates for the selected league
      await fetchGameDates(leagueId)
      // Fetch games for the selected league
      await fetchGames()
    } else {
      // Clear dates and games when no league selected
      availableDates.value = []
      games.value = []
    }
  }

  function setTeamFilter(teamId: number | null) {
    selectedTeamId.value = teamId
    fetchGames()
  }

  function setFieldFilter(fieldId: number | null) {
    selectedFieldId.value = fieldId
    fetchGames()
  }

  function setDateFilter(date: string | null) {
    selectedDate.value = date
    fetchGames()
  }

  function setStatusFilter(status: GameStatus | null) {
    selectedStatus.value = status
    fetchGames()
  }

  function clearFilters() {
    selectedLeagueId.value = null
    selectedTeamId.value = null
    selectedFieldId.value = null
    selectedDate.value = null
    selectedStatus.value = null
    availableDates.value = []
    availableFields.value = []
    games.value = []
  }

  return {
    // State
    games,
    teams,
    fields,
    leagues,
    availableDates,
    availableFields,
    loading,
    error,

    // Filters
    selectedLeagueId,
    selectedTeamId,
    selectedFieldId,
    selectedDate,
    selectedStatus,

    // Computed
    filteredGames,

    // Actions
    fetchGames,
    fetchTeams,
    fetchFields,
    fetchLeagues,
    fetchGameDates,
    updateAvailableFields,
    loadAllData,
    setLeagueFilter,
    setTeamFilter,
    setFieldFilter,
    setDateFilter,
    setStatusFilter,
    clearFilters,
  }
})
