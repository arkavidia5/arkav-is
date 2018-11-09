import axios from 'axios'
import qs from 'qs'

export const apiConfig = {
  baseURL: '/api',

  // Prevent sending cookies with cross-domain requests
  withCredentials: false,

  // Django sends the XSRF token in a cookie named csrftoken
  // https://docs.djangoproject.com/en/2.1/ref/csrf/#ajax
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',

  paramsSerializer: (params) => qs.stringify(params)
}

export function getCsrfToken() {
  const csrfCookieName = apiConfig.xsrfCookieName || 'csrftoken'
  let cookieValue = null
  if (document.cookie && document.cookie != '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, csrfCookieName.length + 1) === (csrfCookieName + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(csrfCookieName.length + 1))
        break
      }
    }
  }
  return cookieValue
}

const apiClient = axios.create(apiConfig)

apiClient.interceptors.response.use(
  (response) => response,
  (err) => {
    // Handle 401 Unauthorized and 403 Forbidden errors by resetting Vuex state (force reload app),
    // only if ignoreUnauthorizedError is not set or set to False in Axios request config
    if (err.response && !err.response.config.ignoreUnauthorizedError && (err.response.status === 401 || err.response.status === 403)) {
      location.reload(true)
    }
    return Promise.reject(err);
  }
)

export default apiClient;
