import { useState, useCallback } from 'react'
import Header from './components/Header.tsx'
import PromptInput from './components/PromptInput.tsx'
import Pipeline from './components/Pipeline.tsx'
import GovernancePanel from './components/GovernancePanel.tsx'
import OutputKit from './components/OutputKit.tsx'

// ── Types ──
export interface StageResult {
  stage_id: number
  stage_name: string
  status: 'pending' | 'running' | 'passed' | 'failed' | 'corrected'
  duration_ms: number
  result: Record<string, unknown>
  error?: string
}

export interface PipelineResponse {
  pipeline_id: string
  user_prompt: string
  status: 'completed' | 'failed' | 'partial'
  started_at: string
  completed_at?: string
  total_duration_ms: number
  stages: StageResult[]
  deployment_kit?: Record<string, unknown>
  governance_report?: Record<string, unknown>
}

export type PipelineState = {
  status: 'idle' | 'running' | 'completed' | 'failed'
  stages: StageResult[]
  response: PipelineResponse | null
  error: string | null
}

// ── API Call ──
async function runPipeline(prompt: string): Promise<PipelineResponse> {
  const res = await fetch('/api/run-pipeline', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_prompt: prompt }),
  })
  if (!res.ok) {
    const err = await res.text()
    throw new Error(`Pipeline failed: ${res.status} — ${err}`)
  }
  return res.json()
}

// ── Simulated Progressive Execution ──
// For demo purposes, we simulate stage-by-stage progress before the real API call.
// This gives the UI the animated "stages running one by one" experience.
function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

export default function App() {
  const [pipeline, setPipeline] = useState<PipelineState>({
    status: 'idle',
    stages: [],
    response: null,
    error: null,
  })

  const handleSubmit = useCallback(async (prompt: string) => {
    // Reset state
    setPipeline({ status: 'running', stages: [], response: null, error: null })

    // Define the 4 stages for progressive UI
    const stageNames = [
      { id: 1, name: 'Intent Extraction', subtitle: 'granite-3-8b-instruct' },
      { id: 2, name: 'Architecture Mapping', subtitle: 'granite-3-8b-instruct' },
      { id: 3, name: 'Governance Guardrail', subtitle: 'Policy Engine' },
      { id: 4, name: 'Secure Code Synthesis', subtitle: 'granite-20b-code' },
    ]

    // Show each stage as "running" with a short delay for visual effect
    let currentStages: StageResult[] = []
    for (let i = 0; i < stageNames.length; i++) {
      currentStages = [
        ...currentStages.map(s => s),
        {
          stage_id: stageNames[i].id,
          stage_name: stageNames[i].name,
          status: 'running' as const,
          duration_ms: 0,
          result: {},
        }
      ]
      setPipeline(prev => ({
        ...prev,
        stages: currentStages,
      }))
      // Visual pacing
      await delay(600)
    }

    // Now make the actual API call (which runs everything server-side)
    try {
      const response = await runPipeline(prompt)

      // Update stages with real results from the server
      setPipeline({
        status: response.status === 'completed' ? 'completed' : 'failed',
        stages: response.stages,
        response: response,
        error: null,
      })
    } catch (err) {
      setPipeline({
        status: 'failed',
        stages: currentStages.map(s => ({ ...s, status: 'failed' as const })),
        response: null,
        error: err instanceof Error ? err.message : 'Unknown error',
      })
    }
  }, [])

  const handleReset = useCallback(() => {
    setPipeline({ status: 'idle', stages: [], response: null, error: null })
  }, [])

  // Derived state
  const isRunning = pipeline.status === 'running'
  const isComplete = pipeline.status === 'completed'
  const governanceReport = pipeline.response?.governance_report as Record<string, unknown> | null
  const deploymentKit = pipeline.response?.deployment_kit as Record<string, unknown> | null

  return (
    <div className="app-shell">
      <Header />

      <main className="main-content">
        {/* Prompt Input */}
        <PromptInput
          onSubmit={handleSubmit}
          disabled={isRunning}
        />

        {/* Summary Bar — shown when pipeline has run */}
        {pipeline.response && (
          <div className="summary-bar">
            <div className="summary-card">
              <div className="summary-card__label">Status</div>
              <div className={`summary-card__value summary-card__value--${isComplete ? 'green' : 'blue'}`}>
                {isComplete ? '✓ Completed' : '✗ Failed'}
              </div>
            </div>
            <div className="summary-card">
              <div className="summary-card__label">Duration</div>
              <div className="summary-card__value summary-card__value--blue text-mono">
                {pipeline.response.total_duration_ms}ms
              </div>
            </div>
            <div className="summary-card">
              <div className="summary-card__label">Compliance</div>
              <div className={`summary-card__value ${
                governanceReport?.status === 'corrected'
                  ? 'summary-card__value--yellow'
                  : 'summary-card__value--green'
              }`}>
                {governanceReport?.status === 'corrected' ? '↻ Auto-Corrected' : '✓ Passed'}
              </div>
            </div>
            <div className="summary-card">
              <div className="summary-card__label">Files Generated</div>
              <div className="summary-card__value summary-card__value--green">
                {(deploymentKit?.files as unknown[])?.length || 0} files
              </div>
            </div>
            <div style={{ marginLeft: 'auto' }}>
              <button className="btn btn--ghost btn--sm" onClick={handleReset}>
                ↺ New Build
              </button>
            </div>
          </div>
        )}

        {/* Pipeline Stages */}
        {pipeline.stages.length > 0 && (
          <Pipeline stages={pipeline.stages} />
        )}

        {/* Governance Panel — shown when Stage 3 has data */}
        {governanceReport && (
          <GovernancePanel report={governanceReport} />
        )}

        {/* Output Kit — shown when pipeline completes successfully */}
        {isComplete && deploymentKit && (
          <OutputKit kit={deploymentKit} />
        )}

        {/* Error state */}
        {pipeline.error && (
          <div style={{
            background: 'rgba(218, 30, 40, 0.1)',
            border: '1px solid var(--ibm-red-400)',
            borderRadius: 'var(--border-radius)',
            padding: '16px',
            color: 'var(--ibm-red-300)',
            fontSize: '14px',
          }}>
            <strong>Pipeline Error:</strong> {pipeline.error}
          </div>
        )}
      </main>
    </div>
  )
}
