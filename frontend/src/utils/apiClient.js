import axios from 'axios';
// import storage from './storage';

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
  // withCredentials: true
});

/**
 * Request Interceptor
 * - Runs before each request is sent.
 * - Its job is to attach the current access token to the Authorization header.
 */
apiClient.interceptors.request.use(
  (config) => {
    // const accessToken = storage.getAccessToken();
    // if (accessToken) {
    //   config.headers.Authorization = `Bearer ${accessToken}`;
    // }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    // If unauthorized (401), redirect to login page
    if (error.response && error.response.status === 401) {
      return Promise.reject(error);
    }
    // return Promise.reject(error);
    const errorMessage = error.response?.data?.detail || 'An unexpected error occurred.';
    return Promise.reject(new Error(errorMessage));
  }
);

/**
 * Performs a GET request.
 * @param {string} endpoint - The API endpoint to call (e.g., "/llms/provider_schema_configs").
 * @returns {Promise<any>} The response data.
 */
// export const getRequest = (endpoint) => {
//   return apiClient.get(endpoint);
// };

export const getRequest = (endpoint) => {
  return apiClient.get(endpoint).then((response) => response.data);
};

/**
 * Performs a POST request.
 * @param {string} endpoint - The API endpoint to call.
 * @param {object} body - The request payload.
 * @returns {Promise<any>} The response data.
 */
// export const postRequest = (endpoint, body) => {
//   return apiClient.post(endpoint, body);
// };

export const postRequest = (endpoint, body) => {
  return apiClient.post(endpoint, body).then((response) => response.data);
};

// ... other request methods (PUT, DELETE, PATCH) remain the same ...

/**
 * Performs a PUT request.
 * @param {string} endpoint - The API endpoint to call.
 * @param {object} body - The request payload.
 * @returns {Promise<any>} The response data.
 */
// export const putRequest = (endpoint, body) => {
//   return apiClient.put(endpoint, body);
// };

export const putRequest = (endpoint, body) => {
  return apiClient.put(endpoint, body).then((response) => response.data);
};

/**
 * Performs a DELETE request.
 * @param {string} endpoint - The API endpoint to call.
 * @returns {Promise<any>} The response data.
 */
export const deleteRequest = (endpoint) => {
  return apiClient.delete(endpoint).then((response) => response.data);
};

/**
 * Performs a PATCH request.
 * @param {string} endpoint - The API endpoint to call.
 * @param {object} body - The request payload.
 * @returns {Promise<any>} The response data.
 */
export const patchRequest = (endpoint, body) => {
  return apiClient.patch(endpoint, body).then((response) => response.data);
};
