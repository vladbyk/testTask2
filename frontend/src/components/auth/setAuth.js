import axios from "axios";

export const BASE_URL = "http://127.0.0.0:80/api/"
export const send_request = axios.create();

send_request.interceptors.request.use(
  (config) => {
    const accessToken = sessionStorage.getItem("access");
    if (accessToken) {
      config.headers["Authorization"] = "JWT " + accessToken;
    }
    return config;
  },
  (error) => {
    Promise.reject(error);
  }
);

send_request.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const originalRequest = error.config;
    let refreshToken = sessionStorage.getItem("refresh");
    if (
      refreshToken &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      return axios
        .post(`${BASE_URL}jwt/refresh`, { refresh: refreshToken })
        .then((res) => {
          if (res.status === 200) {
            sessionStorage.setItem("access", res.data.access);
            console.log("Access token refreshed!");
            console.log(originalRequest)
            return send_request(originalRequest)
          }
        })
        .catch((err) => {
          sessionStorage.clear()
          window.location.replace(window.location.origin+'/login/');
        });
    }
    return Promise.reject(error);
  }
);