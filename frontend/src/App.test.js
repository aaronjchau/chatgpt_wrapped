import { render, screen } from '@testing-library/svelte'
import { describe, expect, it } from 'vitest'

import App from './App.svelte'

describe('App', () => {
  it('renders page title and import button', () => {
    render(App)

    expect(screen.getByText('ChatGPT Wrapped')).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Import + Analyze' })).toBeTruthy()
  })
})
