import Axios from "axios";
Axios.defaults.withCredentials=true

const request = Axios.create({
  timeout: 400000
});

request.interceptors.request.use(
  function(config) {
    return config;
  },
  function() {
    return Promise.reject("数据发送失败，请检查网络配置");
  }
);

// 业务使用的错误代码
request.interceptors.response.use(
  // 响应成功
  res => {
    return res;
  },
  // 响应失败
  function(e) {
    return Promise.reject({
      error_text: "链接服务器超时，请检查您的网络"
    });
  }
);

export { request };

//
// request.get()
