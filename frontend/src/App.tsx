



import { useEffect, useState } from 'react'



import './App.css'



const API_URL = 'http://127.0.0.1:8000'



type ProjectPlan = {



  name: string



  description: string



  features: string[]



  technologies: string[]



  database: string



  testing_requirements: string[]



  deployment_requirements: string[]



}



type TaskStatus = 'Pending' | 'In Progress' | 'Done'



type DevelopmentTask = {



  id: string



  title: string



  description: string



  priority: string



  estimated_hours: number



  dependencies: string[]



  status: TaskStatus



}



type TaskBreakdownResponse = {



  project_name: string



  tasks: DevelopmentTask[]



  total_estimated_hours: number



}



type SavedProject = {



  id: number



  project_name: string



  requirement: string



  total_estimated_hours: number



  created_at: string



}



type Activity = {



  id: number



  project_id: number



  project_name: string



  task_code: string | null



  task_title: string | null



  activity_type: string



  description: string



  old_status: string | null



  new_status: string | null



  created_at: string



}



type ProjectProgress = {

  id: number

  project_name: string

  created_at: string

  total_tasks: number

  completed_tasks: number

  in_progress_tasks: number

  pending_tasks: number

  completion_percentage: number

  total_estimated_hours: number

  completed_estimated_hours: number

}



type ProgressResponse = {

  summary: {

    total_projects: number

    total_tasks: number

    completed_tasks: number

    in_progress_tasks: number

    pending_tasks: number

    completion_percentage: number

    total_estimated_hours: number

    completed_estimated_hours: number

  }

  projects: ProjectProgress[]

}



type AnalyticsResponse = {
  summary: {
    total_projects: number
    total_tasks: number
    status_counts: Record<string, number>
    total_estimated_hours: number
    completed_estimated_hours: number
    unfinished_tasks_count: number
  }
  projects: Array<{
    project_id: number
    project_name: string
    total_tasks: number
    completed_tasks: number
    in_progress_tasks: number
    pending_tasks: number
    completion_percentage: number
    total_estimated_hours: number
    completed_estimated_hours: number
  }>
  unfinished_tasks: Array<{
    project_id: number
    project_name: string
    task_code: string
    title: string
    priority: string
    status: TaskStatus
    estimated_hours: number
  }>
}


type RecommendedTask = AnalyticsResponse['unfinished_tasks'][number] & {
  reason: string
}

function getRecommendedTasks(analytics: AnalyticsResponse | null): RecommendedTask[] {
  if (!analytics) return []

  const priorityScore: Record<string, number> = { High: 3, Medium: 2, Low: 1 }

  return [...analytics.unfinished_tasks]
    .sort((a, b) => {
      const priorityDifference =
        (priorityScore[b.priority] ?? 0) - (priorityScore[a.priority] ?? 0)
      if (priorityDifference !== 0) return priorityDifference
      return a.estimated_hours - b.estimated_hours
    })
    .slice(0, 5)
    .map((task) => ({
      ...task,
      reason:
        task.priority === 'High'
          ? 'High priority — consider tackling this first.'
          : task.priority === 'Medium'
            ? 'Medium priority — work on this after high-priority tasks.'
            : 'Low priority — schedule this after higher-priority work.',
    }))
}


type View =



  | 'overview'



  | 'new-project'



  | 'saved-projects'



  | 'activity'



  | 'settings'



function App() {



  const [view, setView] = useState<View>('overview')



  const [backendOnline, setBackendOnline] = useState(false)



  const [checkingBackend, setCheckingBackend] = useState(true)



  const [requirement, setRequirement] = useState('')



  const [loading, setLoading] = useState(false)



  const [tasksLoading, setTasksLoading] = useState(false)



  const [savedLoading, setSavedLoading] = useState(false)



  const [error, setError] = useState('')



  const [taskError, setTaskError] = useState('')



  const [savedError, setSavedError] = useState('')



  const [plan, setPlan] = useState<ProjectPlan | null>(null)



  const [taskBreakdown, setTaskBreakdown] =



    useState<TaskBreakdownResponse | null>(null)



  const [savedProjects, setSavedProjects] = useState<SavedProject[]>([])



  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(



    null,



  )



  const [activity, setActivity] = useState<Activity[]>([])



  const [activityLoading, setActivityLoading] = useState(false)



  const [activityError, setActivityError] = useState('')

  const [progress, setProgress] = useState<ProgressResponse | null>(null)

  const [progressLoading, setProgressLoading] = useState(false)

  const [progressError, setProgressError] = useState('')

  const [analytics, setAnalytics] = useState<AnalyticsResponse | null>(null)
  const [analyticsLoading, setAnalyticsLoading] = useState(false)
  const [analyticsError, setAnalyticsError] = useState('')

  const recommendedTasks = getRecommendedTasks(analytics)



  const [lastChecked, setLastChecked] = useState('Not checked yet')



  async function checkBackend() {



    setCheckingBackend(true)



    try {



      const response = await fetch(`${API_URL}/`)



      if (!response.ok) throw new Error('Backend health check failed')



      setBackendOnline(true)



      setLastChecked(new Date().toLocaleTimeString())



    } catch {



      setBackendOnline(false)



      setLastChecked(new Date().toLocaleTimeString())



    } finally {



      setCheckingBackend(false)



    }



  }



  async function loadSavedProjects() {



    setSavedLoading(true)



    setSavedError('')



    try {



      const response = await fetch(`${API_URL}/projects/saved`)



      if (!response.ok) {



        throw new Error(`Unable to load saved projects (${response.status})`)



      }



      const data: { projects: SavedProject[] } = await response.json()



      setSavedProjects(data.projects)



    } catch (err) {



      setSavedError(



        err instanceof Error ? err.message : 'Unable to load saved projects.',



      )



    } finally {



      setSavedLoading(false)



    }



  }



  async function loadProjectTasks(projectId: number) {



    setTasksLoading(true)



    setSavedError('')



    setTaskError('')



    try {



      const response = await fetch(



        `${API_URL}/projects/saved/${projectId}/tasks`,



      )



      if (!response.ok) {



        throw new Error(`Unable to load tasks (${response.status})`)



      }



      const data: { project_id: number; tasks: Array<{



        task_code: string



        title: string



        description: string



        priority: string



        estimated_hours: number



        dependencies: string[]



        status: TaskStatus



      }> } = await response.json()



      const project = savedProjects.find((item) => item.id === projectId)



      setSelectedProjectId(projectId)



      setRequirement(project?.requirement ?? '')



      setTaskBreakdown({



        project_name: project?.project_name ?? 'Saved Project',



        tasks: data.tasks.map((task) => ({



          id: task.task_code,



          title: task.title,



          description: task.description,



          priority: task.priority,



          estimated_hours: task.estimated_hours,



          dependencies: task.dependencies,



          status: task.status,



        })),



        total_estimated_hours:



          project?.total_estimated_hours ??



          data.tasks.reduce((sum, task) => sum + task.estimated_hours, 0),



      })



      setView('saved-projects')



    } catch (err) {



      setSavedError(



        err instanceof Error ? err.message : 'Unable to load saved tasks.',



      )



    } finally {



      setTasksLoading(false)



    }



  }



  async function loadActivities() {



    setActivityLoading(true)



    setActivityError('')



    try {



      const response = await fetch(`${API_URL}/activities?limit=50`)



      if (!response.ok) throw new Error(`Unable to load activity history (${response.status})`)



      const data: { activities: Activity[] } = await response.json()



      setActivity(data.activities)



    } catch (err) {



      setActivityError(err instanceof Error ? err.message : 'Unable to load activity history.')



    } finally {



      setActivityLoading(false)



    }



  }



  async function loadProgress() {

    setProgressLoading(true)

    setProgressError('')

    try {

      const response = await fetch(`${API_URL}/projects/progress`)

      if (!response.ok) throw new Error(`Unable to load project progress (${response.status})`)

      const data: ProgressResponse = await response.json()

      setProgress(data)

    } catch (err) {

      setProgressError(err instanceof Error ? err.message : 'Unable to load project progress.')

    } finally {

      setProgressLoading(false)

    }

  }
async function loadAnalytics() {
    setAnalyticsLoading(true)
    setAnalyticsError('')
    try {
      const response = await fetch(`${API_URL}/analytics`)
      if (!response.ok) throw new Error(`Unable to load analytics (${response.status})`)
      const data: AnalyticsResponse = await response.json()
      setAnalytics(data)
    } catch (err) {
      setAnalyticsError(err instanceof Error ? err.message : 'Unable to load analytics.')
    } finally {
      setAnalyticsLoading(false)
    }
  }

  


  useEffect(() => {



    void checkBackend()



    void loadSavedProjects()



    void loadActivities()
    void loadProgress()
    void loadAnalytics()



  }, [])



  async function createProject(event: React.FormEvent<HTMLFormElement>) {



    event.preventDefault()



    if (requirement.trim().length < 10) {



      setError('Please describe your project in at least 10 characters.')



      return



    }



    if (!backendOnline) {



      setError('Your backend is offline. Start FastAPI and try again.')



      return



    }



    setLoading(true)



    setError('')



    setTaskError('')



    setPlan(null)



    try {



      const response = await fetch(`${API_URL}/projects`, {



        method: 'POST',



        headers: { 'Content-Type': 'application/json' },



        body: JSON.stringify({ requirement: requirement.trim() }),



      })



      if (!response.ok) {



        throw new Error(await response.text() || `Request failed (${response.status})`)



      }



      const data: ProjectPlan = await response.json()



      setPlan(data)



      void loadActivities()



    } catch (err) {



      setError(err instanceof Error ? err.message : 'Unable to create the project plan.')



    } finally {



      setLoading(false)



    }



  }



  async function generateTasks() {



    if (requirement.trim().length < 10) {



      setTaskError('Enter a project requirement of at least 10 characters first.')



      return



    }



    if (!backendOnline) {



      setTaskError('Your backend is offline. Start FastAPI and try again.')



      return



    }



    setTasksLoading(true)



    setTaskError('')



    setSelectedProjectId(null)



    try {



      const response = await fetch(`${API_URL}/tasks/breakdown`, {



        method: 'POST',



        headers: { 'Content-Type': 'application/json' },



        body: JSON.stringify({ requirement: requirement.trim() }),



      })



      if (!response.ok) {



        throw new Error(await response.text() || `Task breakdown failed (${response.status})`)



      }



      const data: TaskBreakdownResponse = await response.json()



      // The backend saves the breakdown before returning it.



      // Refresh the saved projects to obtain its database ID.



      const projectsResponse = await fetch(`${API_URL}/projects/saved`)



      if (!projectsResponse.ok) {



        throw new Error('Tasks were generated, but saved projects could not be refreshed.')



      }



      const projectsData: { projects: SavedProject[] } =



        await projectsResponse.json()



      setSavedProjects(projectsData.projects)



      const matchingProject = projectsData.projects.find(



        (project) =>



          project.project_name === data.project_name &&



          project.requirement === requirement.trim(),



      )



      if (!matchingProject) {



        throw new Error(



          'Tasks were generated, but their saved database record could not be identified.',



        )



      }



      setSelectedProjectId(matchingProject.id)



      // Load from SQLite so the UI reflects the actual persisted state.



      const tasksResponse = await fetch(



        `${API_URL}/projects/saved/${matchingProject.id}/tasks`,



      )



      if (!tasksResponse.ok) {



        throw new Error('Project saved, but its stored tasks could not be loaded.')



      }



      const stored: { tasks: Array<{



        task_code: string



        title: string



        description: string



        priority: string



        estimated_hours: number



        dependencies: string[]



        status: TaskStatus



      }> } = await tasksResponse.json()



      setTaskBreakdown({



        project_name: data.project_name,



        tasks: stored.tasks.map((task) => ({



          id: task.task_code,



          title: task.title,



          description: task.description,



          priority: task.priority,



          estimated_hours: task.estimated_hours,



          dependencies: task.dependencies,



          status: task.status,



        })),



        total_estimated_hours: data.total_estimated_hours,



      })



      void loadActivities()



    } catch (err) {



      setTaskError(



        err instanceof Error ? err.message : 'Unable to generate or load tasks.',



      )



    } finally {



      setTasksLoading(false)



    }



  }



  async function updateTaskStatus(taskId: string, status: TaskStatus) {



    if (selectedProjectId === null) {



      setTaskError('Select a saved project before updating task status.')



      return



    }



    setTaskError('')



    try {



      const response = await fetch(



        `${API_URL}/projects/saved/${selectedProjectId}/tasks/${encodeURIComponent(taskId)}/status`,



        {



          method: 'PATCH',



          headers: { 'Content-Type': 'application/json' },



          body: JSON.stringify({ status }),



        },



      )



      if (!response.ok) {



        throw new Error(await response.text() || 'Could not save task status.')



      }



      setTaskBreakdown((current) => {



        if (!current) return current



        return {



          ...current,



          tasks: current.tasks.map((task) =>



            task.id === taskId ? { ...task, status } : task,



          ),



        }



      })



      void loadActivities()



    } catch (err) {



      setTaskError(



        err instanceof Error ? err.message : 'Unable to save task status.',



      )



    }



  }



  const navigation: { id: View; icon: string; label: string }[] = [



    { id: 'overview', icon: '◫', label: 'Overview' },



    { id: 'new-project', icon: '+', label: 'New project' },



    { id: 'saved-projects', icon: '▤', label: 'Saved projects' },



    { id: 'activity', icon: '◷', label: 'Activity log' },



    { id: 'settings', icon: '⚙', label: 'Settings' },



  ]



  return (



    <div className="app-shell">

      <style>{`

        .progress-track { width: 100%; height: 8px; overflow: hidden; border-radius: 999px; background: rgba(148, 163, 184, 0.16); margin-top: 12px; }

        .progress-fill { height: 100%; border-radius: inherit; background: linear-gradient(90deg, #8b5cf6, #38bdf8); transition: width 250ms ease; }

        .progress-track-large { height: 10px; margin: 18px 0 12px; }

        .progress-breakdown { display: flex; flex-wrap: wrap; gap: 12px 20px; margin: 12px 0 18px; color: var(--muted, #94a3b8); font-size: 12px; }

        .progress-breakdown span { display: inline-flex; align-items: center; gap: 6px; }

        .progress-legend { display: inline-block; width: 7px; height: 7px; border-radius: 50%; }

        .done-legend { background: #34d399; } .active-legend { background: #38bdf8; } .pending-legend { background: #94a3b8; }

        .stat-unit { font-size: 14px; color: var(--muted, #94a3b8); }

        .progress-project-list { margin-top: 16px; }

      `}</style>



      <aside className="sidebar">



        <div className="brand">



          <div className="brand-mark">AI</div>



          <div>



            <div className="brand-name">Engineering</div>



            <div className="brand-caption">COMMAND CENTER</div>



          </div>



        </div>



        <div className="workspace-label">WORKSPACE</div>



        <nav className="navigation" aria-label="Main navigation">



          {navigation.map((item) => (



            <button



              key={item.id}



              className={`nav-item ${view === item.id ? 'active' : ''}`}



              onClick={() => {



                setView(item.id)



                if (item.id === 'saved-projects') void loadSavedProjects()



                if (item.id === 'activity') void loadActivities()



              }}



            >



              <span className="nav-icon">{item.icon}</span>



              <span>{item.label}</span>



            </button>



          ))}



        </nav>



        <div className="sidebar-bottom">



          <div className="system-card">



            <div className="system-card-title">



              <span className={`status-dot ${backendOnline ? 'online' : ''}`} />



              System status



            </div>



            <div className="system-status">



              {checkingBackend



                ? 'Checking connection…'



                : backendOnline



                  ? 'Backend connected'



                  : 'Backend offline'}



            </div>



            <button



              className="text-button"



              onClick={() => void checkBackend()}



              disabled={checkingBackend}



            >



              ↻ Check connection



            </button>



          </div>



          <div className="version-label">



            <span className="version-dot" />



            Development environment <span>v0.1.0</span>



          </div>



        </div>



      </aside>



      <main className="main-content">



        <header className="topbar">



          <div className="breadcrumb">



            <span>Workspace</span>



            <span className="breadcrumb-separator">/</span>



            <strong>{navigation.find((item) => item.id === view)?.label}</strong>



          </div>



          <div className="topbar-right">



            <span className="environment-badge">



              <span className="status-dot online" />



              LOCAL ENVIRONMENT



            </span>



            <div className="avatar">SV</div>



          </div>



        </header>



        <div className="page-content">



          {view === 'overview' && (



            <>



              <section className="page-heading">



                <div>



                  <div className="eyebrow">ENGINEERING WORKSPACE</div>



                  <h1>Command center<span className="heading-period">.</span></h1>



                  <p className="page-description">



                    Plan projects, organize development tasks, and track progress.



                  </p>



                </div>



                <button className="primary-button" onClick={() => setView('new-project')}>



                  + New project



                </button>



              </section>



              <section className="stats-grid">



                <article className="stat-card">



                  <div className="stat-top"><span>SAVED PROJECTS</span></div>



                  <div className="stat-value">{savedProjects.length}</div>



                  <div className="stat-foot">Projects stored in SQLite</div>



                </article>



                <article className="stat-card">



                  <div className="stat-top"><span>BACKEND API</span></div>



                  <div className="stat-value stat-status">



                    {checkingBackend ? 'Checking' : backendOnline ? 'Online' : 'Offline'}



                  </div>



                  <div className="stat-foot">{lastChecked}</div>



                </article>



                <article className="stat-card">



                  <div className="stat-top"><span>ACTIVE TASK LIST</span></div>



                  <div className="stat-value">{taskBreakdown?.tasks.length ?? 0}</div>



                  <div className="stat-foot">Tasks currently displayed</div>



                </article>



                <article className="stat-card">



                  <div className="stat-top"><span>WORKFLOW</span></div>



                  <div className="stat-value">Ready</div>



                  <div className="stat-foot">Local development environment</div>



                </article>



              </section>



              <section className="section-block">

                <div className="section-heading">

                  <div>

                    <h2>Project progress</h2>

                    <p>Live metrics calculated from your saved tasks.</p>

                  </div>

                  <button className="secondary-button" onClick={() => void loadProgress()} disabled={progressLoading}>

                    {progressLoading ? 'Refreshing…' : '↻ Refresh progress'}

                  </button>

                </div>



                {progressError && <div className="error-message" role="alert">{progressError}</div>}



                {progressLoading && !progress ? (

                  <div className="content-card loading-card"><div className="loading-spinner" /><p>Loading project progress…</p></div>

                ) : progress ? (

                  <>

                    <div className="stats-grid progress-stats-grid">

                      <article className="stat-card">

                        <div className="stat-top"><span>OVERALL COMPLETION</span></div>

                        <div className="stat-value">{progress.summary.completion_percentage}%</div>

                        <div className="progress-track"><div className="progress-fill" style={{ width: `${progress.summary.completion_percentage}%` }} /></div>

                      </article>

                      <article className="stat-card">

                        <div className="stat-top"><span>COMPLETED TASKS</span></div>

                        <div className="stat-value">{progress.summary.completed_tasks}</div>

                        <div className="stat-foot">of {progress.summary.total_tasks} total tasks</div>

                      </article>

                      <article className="stat-card">

                        <div className="stat-top"><span>IN PROGRESS</span></div>

                        <div className="stat-value">{progress.summary.in_progress_tasks}</div>

                        <div className="stat-foot">Tasks currently underway</div>

                      </article>

                      <article className="stat-card">

                        <div className="stat-top"><span>ESTIMATED HOURS</span></div>

                        <div className="stat-value">{progress.summary.completed_estimated_hours}<span className="stat-unit"> h</span></div>

                        <div className="stat-foot">of {progress.summary.total_estimated_hours} estimated hours completed</div>

                      </article>

                    </div>



                    {progress.projects.length ? (

                      <div className="saved-project-list progress-project-list">

                        {progress.projects.map((project) => (

                          <article className="content-card saved-project-card" key={project.id}>

                            <div className="result-header">

                              <div>

                                <div className="eyebrow">PROJECT #{project.id}</div>

                                <h2>{project.project_name}</h2>

                                <p>{project.completed_tasks} of {project.total_tasks} tasks completed</p>

                              </div>

                              <span className="connection-pill connected">{project.completion_percentage}% complete</span>

                            </div>

                            <div className="progress-track progress-track-large" role="progressbar" aria-label={`${project.project_name} completion`} aria-valuemin={0} aria-valuemax={100} aria-valuenow={project.completion_percentage}>

                              <div className="progress-fill" style={{ width: `${project.completion_percentage}%` }} />

                            </div>

                            <div className="progress-breakdown">

                              <span><i className="progress-legend done-legend" />Done: {project.completed_tasks}</span>

                              <span><i className="progress-legend active-legend" />In progress: {project.in_progress_tasks}</span>

                              <span><i className="progress-legend pending-legend" />Pending: {project.pending_tasks}</span>

                              <span>{project.completed_estimated_hours} / {project.total_estimated_hours} hours</span>

                            </div>

                            <button className="primary-button" onClick={() => { void loadSavedProjects(); void loadProjectTasks(project.id) }} disabled={tasksLoading}>

                              Open project tasks →

                            </button>

                          </article>

                        ))}

                      </div>

                    ) : (

                      <div className="content-card empty-state"><strong>No saved projects yet</strong><p>Create a task breakdown to see project progress here.</p></div>

                    )}

                  </>

                ) : !progressError ? (

                  <div className="content-card empty-state"><p>Progress data is not available yet.</p></div>

                ) : null}

              </section>
<section className="section-block analytics-section">
                <div className="section-heading">
                  <div><h2>Task analytics</h2><p>Task distribution, project comparison, and estimated effort from SQLite.</p></div>
                  <button className="secondary-button" onClick={() => { void loadAnalytics(); void loadProgress() }} disabled={analyticsLoading || progressLoading}>{analyticsLoading || progressLoading ? 'Refreshing…' : '↻ Refresh analytics'}</button>
                </div>
                {analyticsError && <div className="error-message" role="alert">{analyticsError}</div>}
                {analyticsLoading && !analytics ? <div className="content-card loading-card"><div className="loading-spinner" /><p>Loading analytics…</p></div> : analytics ? <>
                  <div className="stats-grid analytics-stats-grid">
                    {[
                      { label: 'DONE', value: analytics.summary.status_counts['Done'] ?? 0, foot: 'Tasks completed' },
                      { label: 'IN PROGRESS', value: analytics.summary.status_counts['In Progress'] ?? 0, foot: 'Tasks underway' },
                      { label: 'PENDING', value: analytics.summary.status_counts['Pending'] ?? 0, foot: 'Not started' },
                      { label: 'UNFINISHED TASKS', value: analytics.summary.unfinished_tasks_count, foot: 'Across all projects' },
                    ].map((item) => <article className="stat-card" key={item.label}><div className="stat-top"><span>{item.label}</span></div><div className="stat-value">{item.value}</div><div className="stat-foot">{item.foot}</div></article>)}
                  </div>
                  <div className="analytics-grid">
                    <article className="content-card analytics-card">
                      <h3>Task status distribution</h3>
                      {(['Done', 'In Progress', 'Pending'] as const).map((status) => {
                        const value = analytics.summary.status_counts[status] ?? 0
                        const total = analytics.summary.total_tasks
                        const percentage = total ? value / total * 100 : 0
                        const legendClass = status === 'Done' ? 'done-legend' : status === 'In Progress' ? 'active-legend' : 'pending-legend'
                        return <div className="analytics-bar-row" key={status}><div className="analytics-bar-label"><span><i className={`progress-legend ${legendClass}`} />{status}</span><strong>{value} · {percentage.toFixed(1)}%</strong></div><div className="progress-track"><div className="progress-fill" style={{ width: `${percentage}%` }} /></div></div>
                      })}
                    </article>
                    <article className="content-card analytics-card">
                      <h3>Estimated hours</h3><p className="settings-note">Completed estimated effort compared with the full estimate.</p>
                      <div className="hours-summary"><strong>{analytics.summary.completed_estimated_hours} h</strong><span>of {analytics.summary.total_estimated_hours} h completed</span></div>
                      <div className="progress-track progress-track-large"><div className="progress-fill" style={{ width: `${analytics.summary.total_estimated_hours ? Math.min(100, analytics.summary.completed_estimated_hours / analytics.summary.total_estimated_hours * 100) : 0}%` }} /></div>
                      <p className="settings-note">Remaining estimate: {Math.max(0, analytics.summary.total_estimated_hours - analytics.summary.completed_estimated_hours)} hours</p>
                    </article>
                  </div>
                  <article className="content-card analytics-card"><h3>Project completion comparison</h3>
                    {analytics.projects.length ? analytics.projects.map((project) => <div className="analytics-project-row" key={project.project_id}><div className="analytics-bar-label"><strong>#{project.project_id} {project.project_name}</strong><strong>{project.completion_percentage}%</strong></div><div className="progress-track"><div className="progress-fill" style={{ width: `${Math.max(0, Math.min(100, project.completion_percentage))}%` }} /></div><p className="settings-note">{project.completed_tasks}/{project.total_tasks} tasks done · {project.completed_estimated_hours}/{project.total_estimated_hours} hours completed</p></div>) : <p className="settings-note">No saved projects available yet.</p>}
                  </article>
                  <article className="content-card analytics-card"><div className="section-heading"><div><h3>Unfinished tasks</h3><p>Tasks that still need work.</p></div><span className="connection-pill">{analytics.summary.unfinished_tasks_count} remaining</span></div>
                    {analytics.unfinished_tasks.length ? <div className="analytics-unfinished-list">{analytics.unfinished_tasks.slice(0, 8).map((task) => <div className="analytics-unfinished-item" key={`${task.project_id}-${task.task_code}`}><div><strong>{task.task_code} · {task.title}</strong><p className="settings-note">{task.project_name} · {task.estimated_hours} hours · {task.priority} priority</p></div><span className="connection-pill">{task.status}</span></div>)}</div> : <p className="settings-note">All tasks are marked Done. Nice work!</p>}
                  </article>
                  <article className="content-card analytics-card">
                    <div className="section-heading">
                      <div>
                        <h3>Smart next tasks</h3>
                        <p>Recommendations based on priority and estimated effort.</p>
                      </div>
                      <span className="connection-pill">{recommendedTasks.length} suggestions</span>
                    </div>
                    {recommendedTasks.length ? (
                      <div className="analytics-unfinished-list">
                        {recommendedTasks.map((task, index) => (
                          <div className="analytics-unfinished-item" key={`${task.project_id}-${task.task_code}`}>
                            <div>
                              <strong>{index + 1}. {task.task_code} · {task.title}</strong>
                              <p className="settings-note">
                                Project #{task.project_id} · {task.estimated_hours} hours · {task.priority} priority · {task.status}
                              </p>
                              <p className="settings-note">{task.reason}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="settings-note">{analyticsLoading ? 'Loading recommendations...' : 'No unfinished tasks to recommend.'}</p>
                    )}
                    <p className="settings-note">Note: dependencies are not included in the analytics response, so recommendations use priority first and estimated effort as a tie-breaker.</p>
                  </article>
                </> : !analyticsError ? <div className="content-card empty-state"><p>Analytics data is not available yet.</p></div> : null}
              </section>

              


              <section className="hero-panel">



                <div className="hero-copy">



                  <div className="hero-badge">



                    <span className="hero-badge-dot" />



                    ENGINEERING WORKSPACE



                  </div>



                  <h2>From idea to<br />working software.</h2>



                  <p>Generate a project breakdown and keep your task progress saved locally.</p>



                  <button className="primary-button hero-button" onClick={() => setView('new-project')}>



                    Start a project →



                  </button>



                </div>



                <div className="workflow-visual" aria-label="Engineering workflow">



                  <div className="orbit orbit-one" />



                  <div className="orbit orbit-two" />



                  <div className="orbit-center">AI</div>



                  <div className="orbit-node node-one">01</div>



                  <div className="orbit-node node-two">02</div>



                  <div className="orbit-node node-three">03</div>



                  <div className="orbit-node node-four">04</div>



                  <div className="orbit-label">ENGINEERING LOOP</div>



                </div>



              </section>



              <section className="section-block">



                <div className="section-heading">



                  <div><h2>Recent activity</h2><p>Persistent project and task events stored in SQLite</p></div>



                  <button className="text-button" onClick={() => setView('activity')}>View all →</button>



                </div>



                <div className="content-card">



                  {activityLoading ? (



                    <div className="empty-state"><p>Loading activity…</p></div>



                  ) : activityError ? (



                    <div className="error-message" role="alert">{activityError}</div>



                  ) : activity.length ? (



                    <div className="activity-list">



                      {activity.slice(0, 5).map((item) => (



                        <div className="activity-item" key={item.id}>



                          <span className="activity-dot" />



                          <span>{item.description} · {new Date(item.created_at + (item.created_at.endsWith('Z') ? '' : 'Z')).toLocaleString()}</span>



                        </div>



                      ))}



                    </div>



                  ) : (



                    <div className="empty-state">



                      <strong>No activity yet</strong>



                      <p>Project creation and task status changes will appear here.</p>



                    </div>



                  )}



                </div>



              </section>



            </>



          )}



          {view === 'new-project' && (



            <>



              <section className="page-heading">



                <div>



                  <div className="eyebrow">PROJECT WORKSPACE</div>



                  <h1>New project<span className="heading-period">.</span></h1>



                  <p className="page-description">Describe your project and create a task breakdown.</p>



                </div>



                <span className={`connection-pill ${backendOnline ? 'connected' : 'disconnected'}`}>



                  {backendOnline ? 'API connected' : 'API offline'}



                </span>



              </section>



              <section className="content-card requirement-card">



                <div className="card-heading">



                  <span className="step-label">STEP 01</span>



                  <h2>Define your requirements</h2>



                  <p>Explain the application, its users, and key functionality.</p>



                </div>



                <form onSubmit={createProject}>



                  <label htmlFor="requirement">Project requirement</label>



                  <textarea



                    id="requirement"



                    value={requirement}



                    onChange={(event) => setRequirement(event.target.value)}



                    placeholder="Describe your application, users, features, and technology stack..."



                    rows={8}



                    minLength={10}



                    required



                  />



                  <div className="input-foot">



                    <span>Be specific about your requirements.</span>



                    <span>{requirement.length} characters</span>



                  </div>



                  {error && <div className="error-message" role="alert">{error}</div>}



                  <div className="form-actions">



                    <button



                      type="button"



                      className="secondary-button"



                      onClick={() => {



                        setRequirement('')



                        setError('')



                        setTaskError('')



                        setPlan(null)



                        setTaskBreakdown(null)



                        setSelectedProjectId(null)



                      }}



                    >



                      Clear



                    </button>



                    <button type="submit" className="primary-button" disabled={loading || !backendOnline}>



                      {loading ? 'Generating plan…' : 'Generate project plan →'}



                    </button>



                  </div>



                  <p className="api-notice">



                    Project planning may use paid API credits. Task breakdown uses your local rule-based generator.



                  </p>



                </form>



              </section>



              {loading && (



                <div className="content-card loading-card">



                  <div className="loading-spinner" />



                  <div><strong>Generating your project plan</strong><p>Please wait…</p></div>



                </div>



              )}



              {plan && (



                <section className="content-card result-card">



                  <div className="result-header">



                    <div>



                      <div className="eyebrow">GENERATED PROJECT PLAN</div>



                      <h2>{plan.name}</h2>



                      <p>{plan.description}</p>



                    </div>



                    <span className="connection-pill connected">Plan generated</span>



                  </div>



                  <div className="result-grid">



                    <ResultList title="Key features" items={plan.features} />



                    <ResultList title="Technologies" items={plan.technologies} />



                    <ResultList title="Testing requirements" items={plan.testing_requirements} />



                    <ResultList title="Deployment requirements" items={plan.deployment_requirements} />



                  </div>



                  <div className="database-box">



                    <span>RECOMMENDED DATABASE</span>



                    <strong>{plan.database}</strong>



                  </div>



                  <button className="secondary-button" onClick={() => downloadJson(plan, 'project-plan.json')}>



                    ↓ Export plan as JSON



                  </button>



                </section>



              )}



              <section className="content-card task-breakdown-card">



                <div className="card-heading">



                  <span className="step-label">STEP 02</span>



                  <h2>Break the project into tasks</h2>



                  <p>Generate tasks and save them permanently in SQLite.</p>



                </div>



                <button



                  className="primary-button"



                  onClick={() => void generateTasks()}



                  disabled={tasksLoading || loading || !backendOnline || requirement.trim().length < 10}



                >



                  {tasksLoading ? 'Generating and saving…' : 'Break Down Tasks →'}



                </button>



                <p className="api-notice">This task breakdown uses local Python rules and does not call OpenAI.</p>



                {taskError && <div className="error-message" role="alert">{taskError}</div>}



                {tasksLoading && (



                  <div className="loading-card">



                    <div className="loading-spinner" />



                    <div><strong>Processing tasks</strong><p>Saving and loading the database records.</p></div>



                  </div>



                )}



                {taskBreakdown && (



                  <TaskResults



                    breakdown={taskBreakdown}



                    selectedProjectId={selectedProjectId}



                    onStatusChange={updateTaskStatus}



                    onExport={() => downloadJson(taskBreakdown, 'task-breakdown.json')}



                    error={taskError}



                  />



                )}



                {selectedProjectId !== null && (



                  <p className="settings-note">Saved project database ID: {selectedProjectId}</p>



                )}



              </section>



            </>



          )}



          {view === 'saved-projects' && (



            <>



              <section className="page-heading">



                <div>



                  <div className="eyebrow">SQLITE STORAGE</div>



                  <h1>Saved projects<span className="heading-period">.</span></h1>



                  <p className="page-description">Open a saved project to restore its tasks and status.</p>



                </div>



                <button className="secondary-button" onClick={() => void loadSavedProjects()} disabled={savedLoading}>



                  {savedLoading ? 'Refreshing…' : '↻ Refresh'}



                </button>



              </section>



              {savedError && <div className="error-message" role="alert">{savedError}</div>}



              {savedLoading ? (



                <div className="content-card loading-card"><div className="loading-spinner" /><p>Loading saved projects…</p></div>



              ) : savedProjects.length === 0 ? (



                <div className="content-card empty-state">



                  <strong>No saved projects yet</strong>



                  <p>Generate a task breakdown first. The project will appear here.</p>



                  <button className="primary-button" onClick={() => setView('new-project')}>Create a project</button>



                </div>



              ) : (



                <div className="saved-project-list">



                  {savedProjects.map((project) => (



                    <article className="content-card saved-project-card" key={project.id}>



                      <div className="result-header">



                        <div>



                          <div className="eyebrow">PROJECT #{project.id}</div>



                          <h2>{project.project_name}</h2>



                          <p>{project.requirement}</p>



                        </div>



                        <span className="connection-pill connected">



                          {project.total_estimated_hours} hours



                        </span>



                      </div>



                      <p className="settings-note">Created: {project.created_at}</p>



                      <button



                        className="primary-button"



                        onClick={() => void loadProjectTasks(project.id)}



                        disabled={tasksLoading}



                      >



                        {tasksLoading && selectedProjectId === project.id ? 'Loading…' : 'Open saved tasks →'}



                      </button>



                    </article>



                  ))}



                </div>



              )}



              {taskBreakdown && selectedProjectId !== null && (



                <section className="content-card task-breakdown-card">



                  <TaskResults



                    breakdown={taskBreakdown}



                    selectedProjectId={selectedProjectId}



                    onStatusChange={updateTaskStatus}



                    onExport={() => downloadJson(taskBreakdown, 'saved-tasks.json')}



                    error={taskError}



                  />



                </section>



              )}



            </>



          )}



          {view === 'activity' && (



            <>



              <section className="page-heading">



                <div>



                  <div className="eyebrow">WORKSPACE HISTORY</div>



                  <h1>Activity log<span className="heading-period">.</span></h1>



                  <p className="page-description">Persistent project and task events stored in SQLite.</p>



                </div>



              </section>



              <section className="content-card">



                <div className="section-heading">



                  <div><h2>Recent events</h2><p>Newest activity appears first.</p></div>



                  <button className="secondary-button" onClick={() => void loadActivities()} disabled={activityLoading}>



                    {activityLoading ? 'Refreshing…' : '↻ Refresh'}



                  </button>



                </div>



                {activityError && <div className="error-message" role="alert">{activityError}</div>}



                {activityLoading ? (



                  <div className="empty-state"><p>Loading activity history…</p></div>



                ) : activity.length ? (



                  <div className="activity-list">



                    {activity.map((item) => (



                      <div className="activity-item" key={item.id}>



                        <span className="activity-dot" />



                        <div>



                          <span>{item.description}</span>



                          <p className="settings-note">{item.project_name} · {new Date(item.created_at + (item.created_at.endsWith('Z') ? '' : 'Z')).toLocaleString()}</p>



                        </div>



                      </div>



                    ))}



                  </div>



                ) : !activityError ? (



                  <div className="empty-state">



                    <strong>No recorded activity</strong>



                    <p>New project creation and task status changes will appear here.</p>



                  </div>



                ) : null}



              </section>



            </>



          )}



          {view === 'settings' && (



            <>



              <section className="page-heading">



                <div>



                  <div className="eyebrow">CONFIGURATION</div>



                  <h1>Settings<span className="heading-period">.</span></h1>



                  <p className="page-description">Local development connection details.</p>



                </div>



              </section>



              <section className="content-card settings-card">



                <div><h3>Backend API URL</h3><p>Local FastAPI server</p></div>



                <code>{API_URL}</code>



                <div><h3>Connection status</h3><p>{backendOnline ? 'Connected' : 'Offline'}</p></div>



                <div><h3>Database</h3><p>SQLite · backend/command_center.db</p></div>



                <button className="secondary-button" onClick={() => void checkBackend()} disabled={checkingBackend}>



                  ↻ Test connection



                </button>



              </section>



            </>



          )}



          <footer className="page-footer">



            <span>AI ENGINEERING COMMAND CENTER</span>



            <span>Built for intelligent software delivery.</span>



          </footer>



        </div>



      </main>



    </div>



  )



}



function TaskResults({



  breakdown,



  selectedProjectId,



  onStatusChange,



  onExport,



  error,



}: {



  breakdown: TaskBreakdownResponse



  selectedProjectId: number | null



  onStatusChange: (id: string, status: TaskStatus) => void



  onExport: () => void



  error: string



}) {



  return (



    <div className="task-results">



      <div className="result-header">



        <div>



          <div className="eyebrow">SAVED TASK BREAKDOWN</div>



          <h2>{breakdown.project_name}</h2>



          <p>{breakdown.tasks.length} tasks · {breakdown.total_estimated_hours} estimated hours</p>



        </div>



        <button className="secondary-button" onClick={onExport}>Export tasks</button>



      </div>



      {selectedProjectId === null && (



        <p className="settings-note">This task list has not been linked to a saved project yet.</p>



      )}



      {error && <div className="error-message" role="alert">{error}</div>}



      {breakdown.tasks.map((task) => (



        <article className="task-item" key={task.id}>



          <div className="task-item-top">



            <span className="task-id">{task.id}</span>



            <span className={`task-priority priority-${task.priority.toLowerCase()}`}>{task.priority}</span>



            <span className="task-hours">{task.estimated_hours} h</span>



          </div>



          <h3>{task.title}</h3>



          <p>{task.description}</p>



          <div className="task-meta">



            <span>Dependencies: {task.dependencies.length ? task.dependencies.join(', ') : 'None'}</span>



            <label>



              Status{' '}



              <select



                value={task.status}



                disabled={selectedProjectId === null}



                onChange={(event) => onStatusChange(task.id, event.target.value as TaskStatus)}



              >



                <option value="Pending">Pending</option>



                <option value="In Progress">In Progress</option>



                <option value="Done">Done</option>



              </select>



            </label>



          </div>



        </article>



      ))}



    </div>



  )



}



function ResultList({ title, items }: { title: string; items: string[] }) {



  return (



    <article className="result-section">



      <h3>{title}</h3>



      {items.length ? (



        <ul>{items.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}</ul>



      ) : (



        <p className="muted-text">No items provided.</p>



      )}



    </article>



  )



}



function downloadJson(data: unknown, filename: string) {



  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })



  const url = URL.createObjectURL(blob)



  const link = document.createElement('a')



  link.href = url



  link.download = filename



  link.click()



  URL.revokeObjectURL(url)



}



export default App
