import { invoke } from '@tauri-apps/api/core'
import { listen } from '@tauri-apps/api/event'
import { useEffect, useState } from 'react'

interface DrumEvent {
  type: 'kick' | 'snare' | 'hats'
  velocity: number
  timestamp: number
}

export function useTauriIntegration() {
  const [isOverlayOpen, setIsOverlayOpen] = useState(false)
  const [drumEvents, setDrumEvents] = useState<DrumEvent[]>([])

  useEffect(() => {
    // Listen for drum events from the backend
    const unlisten = listen<DrumEvent>('drum-event', (event) => {
      setDrumEvents(prev => [...prev, event.payload])
      // Trigger overlay effects
      if (event.payload.type === 'kick') {
        triggerKickEffect(event.payload.velocity)
      } else if (event.payload.type === 'snare') {
        triggerSnareEffect(event.payload.velocity)
      } else if (event.payload.type === 'hats') {
        triggerHatsEffect(event.payload.velocity)
      }
    })

    return () => {
      unlisten.then(fn => fn())
    }
  }, [])

  const openOverlay = async () => {
    try {
      await invoke('open_overlay_window')
      setIsOverlayOpen(true)
    } catch (error) {
      console.error('Failed to open overlay:', error)
    }
  }

  const closeOverlay = async () => {
    try {
      await invoke('close_overlay_window')
      setIsOverlayOpen(false)
    } catch (error) {
      console.error('Failed to close overlay:', error)
    }
  }

  const triggerKickEffect = (velocity: number) => {
    // Send kick event to overlay
    window.dispatchEvent(new CustomEvent('drum-kick', { detail: { velocity } }))
  }

  const triggerSnareEffect = (velocity: number) => {
    // Send snare event to overlay
    window.dispatchEvent(new CustomEvent('drum-snare', { detail: { velocity } }))
  }

  const triggerHatsEffect = (velocity: number) => {
    // Send hats event to overlay
    window.dispatchEvent(new CustomEvent('drum-hats', { detail: { velocity } }))
  }

  return {
    isOverlayOpen,
    drumEvents,
    openOverlay,
    closeOverlay,
    triggerKickEffect,
    triggerSnareEffect,
    triggerHatsEffect
  }
}