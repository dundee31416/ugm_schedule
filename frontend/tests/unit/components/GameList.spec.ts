import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import GameList from '../../../src/components/GameList.vue'

describe('GameList.vue', () => {
  it('renders game list component', () => {
    const wrapper = mount(GameList, {
      props: {
        games: []
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('displays empty state when no games', () => {
    const wrapper = mount(GameList, {
      props: {
        games: []
      }
    })
    expect(wrapper.text()).toContain('No games')
  })

  it('renders games when provided', () => {
    const games = [
      {
        id: 1,
        league: { id: 1, name: 'Test League' },
        home_team: { id: 1, name: 'Team A' },
        away_team: { id: 2, name: 'Team B' },
        game_date: '2026-04-15',
        status: 'upcoming'
      }
    ]
    const wrapper = mount(GameList, {
      props: {
        games
      }
    })
    expect(wrapper.text()).toContain('Team A')
    expect(wrapper.text()).toContain('Team B')
  })
})
