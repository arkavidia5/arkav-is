import store from './store.js'
import api from './api.js'

/**
 * Get current session without having to pass through the 401 error handler
 */
async function getCurrentSession() {
  try {
    let response = await api.get('/auth/', { ignoreUnauthorizedError: true })
    return response.data
  } catch (err) {
    return null
  }
}

export async function requireLogin(to, from, next) {
  // Will redirect here if not logged in
  const redirectTo = { name: 'login', replace: true }

  // If we are logged in according to the store state, allow navigation
  // (cases where the cookie is invalid even though the store state says we're logged in
  // will be handled by the API call error handler)
  if (store.getters['auth/isLoggedIn']) {
    next()
    return
  }

  // If user state is empty, try checking the current session from API
  // (perhaps we still have a valid cookie?)
  let user = await getCurrentSession()
  if (user) {
    store.commit('auth/setUser', user)
    next()
    return
  }

  // We don't have a valid cookie, redirect to login
  if (to.name !== redirectTo.name) {
    store.commit('auth/setLoginRedirect', to)
  }
  next(redirectTo)
}

export async function requireGuest(to, from, next) {
  // Will redirect here if logged in
  const redirectTo = { name: 'teams' }

  // If we are logged in according to store state, redirect
  if (store.getters['auth/isLoggedIn']) {
    next(redirectTo)
    return
  }

  // If user state is empty, try checking the current session from API
  // (perhaps we still have a valid cookie?)
  let user = await getCurrentSession()
  if (user) {
    store.commit('auth/setUser', user)
    next(redirectTo)
    return
  }

  // We are not logged in, allow navigation
  next()
}
