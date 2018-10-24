import axios from 'axios'
import qs from 'qs'

const apiConfig = {
  baseURL: '/api',

  // Prevent sending cookies with cross-domain requests
  withCredentials: false,

  // Django sends the XSRF token in a cookie named csrftoken
  // https://docs.djangoproject.com/en/2.1/ref/csrf/#ajax
  xsrfCookieName: 'csrftoken',

  paramsSerializer: (params) => qs.stringify(params)
}

const apiClient = axios.create(apiConfig)

apiClient.interceptors.response.use(
  (response) => response,
  (err) => {
    // Handle 401 Unauthorized errors as if logging out (force reload app)
    if (err.response && err.response.status === 401) {
      location.reload(true)
    }
    return Promise.reject(err);
  }
)

/**
 * Get current session without having to pass through the 401 error handler
 */
export async function getCurrentSession() {
  let response = await axios.get('/session', apiConfig)
  return response.data
}

export default apiClient;
