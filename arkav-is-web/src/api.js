import axios from 'axios'
import qs from 'qs'

const apiConfig = {
  baseURL: '/api',

  // Prevent sending cookies with cross-domain requests
  withCredentials: false,

  // Django sends the XSRF token in a cookie named csrftoken
  // https://docs.djangoproject.com/en/2.1/ref/csrf/#ajax
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',

  paramsSerializer: (params) => qs.stringify(params)
}

const apiClient = axios.create(apiConfig)

apiClient.interceptors.response.use(
  (response) => response,
  (err) => {
    // Handle 401 Unauthorized errors by resetting Vuex state (force reload app),
    // only if ignoreUnauthorizedError is not set or set to False in Axios request config
    if (err.response && !err.response.config.ignoreUnauthorizedError && err.response.status === 401) {
      location.reload(true)
    }
    return Promise.reject(err);
  }
)

export default apiClient;
