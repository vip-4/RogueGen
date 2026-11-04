import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { LoadingSpinner } from './components/ui/LoadingSpinner'

const Landing = lazy(() => import('./pages/Landing').then(m => ({ default: m.Landing })))
const Workspace = lazy(() => import('./pages/Workspace').then(m => ({ default: m.Workspace })))
const History = lazy(() => import('./pages/History').then(m => ({ default: m.History })))
const GameStudio = lazy(() => import('./pages/GameStudio').then(m => ({ default: m.GameStudio })))
const Workshop = lazy(() => import('./pages/Workshop').then(m => ({ default: m.Workshop })))

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Suspense fallback={<div className="min-h-screen flex items-center justify-center bg-gray-950"><LoadingSpinner /></div>}>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/workspace" element={<Workspace />} />
          <Route path="/studio" element={<GameStudio />} />
          <Route path="/workshop" element={<Workshop />} />
          <Route path="/history" element={<History />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}
