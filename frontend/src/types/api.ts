/**
 * TypeScript type definitions for API responses
 */

// Base types
export interface BaseModel {
  id: number
  created_at: string
  updated_at: string
}

// Game status enum
export type GameStatus = 'upcoming' | 'completed' | 'cancelled'

// League types
export interface League extends BaseModel {
  name: string
  source_url: string
  is_active: boolean
}

// Team types
export interface Team extends BaseModel {
  name: string
  normalized_name: string
}

// Field types
export interface Field extends BaseModel {
  name: string
  address?: string
  city?: string
}

// Game types
export interface Game extends BaseModel {
  league_id: number
  home_team_id: number
  away_team_id: number
  field_id?: number
  game_date: string
  game_time?: string
  home_score?: number
  away_score?: number
  status: GameStatus
  notes?: string
  external_id?: string
  scraped_at: string

  // Nested relationships
  league: League
  home_team: Team
  away_team: Team
  field?: Field
}

// Legacy summary types for backward compatibility
export interface LeagueSummary {
  id: number
  name: string
}

export interface TeamSummary {
  id: number
  name: string
}

export interface FieldSummary {
  id: number
  name: string
  city?: string
}

// Filter types
export interface GameFilters {
  team_name?: string
  field?: string
  start_date?: string
  end_date?: string
  status?: GameStatus
  league_id?: number
  limit?: number
  offset?: number
}

// List response types
export interface GameListResponse {
  games: Game[]
  total: number
  limit: number
  offset: number
  has_more: boolean
}

export interface TeamListResponse {
  teams: Team[]
  total: number
  limit: number
  offset: number
  has_more: boolean
}

export interface FieldListResponse {
  fields: Field[]
  total: number
  limit: number
  offset: number
  has_more: boolean
}

export interface LeagueListResponse {
  leagues: League[]
  total: number
  limit: number
  offset: number
  has_more: boolean
}
