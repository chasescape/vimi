import axios from 'axios';

// 创建 axios 实例
const instance = axios.create({
    baseURL: 'http://localhost:5000', // 后端服务地址
    timeout: 15000, // 请求超时时间
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    },
    // 允许跨域携带cookie
    withCredentials: true
});

// 请求拦截器
instance.interceptors.request.use(
    (config) => {
        // 添加调试信息
        console.log('发送请求:', {
            url: config.url,
            method: config.method,
            headers: config.headers,
            data: config.data
        });
        return config;
    },
    (error) => {
        console.error('请求配置错误:', error);
        return Promise.reject(error);
    }
);

// 响应拦截器
instance.interceptors.response.use(
    (response) => {
        // 添加调试信息
        console.log('收到响应:', {
            status: response.status,
            data: response.data,
            headers: response.headers
        });
        return response;
    },
    (error) => {
        if (error.response) {
            // 服务器返回错误状态码
            console.error('服务器响应错误:', {
                status: error.response.status,
                data: error.response.data,
                headers: error.response.headers
            });

            switch (error.response.status) {
                case 404:
                    console.error('请求的资源不存在');
                    break;
                case 500:
                    console.error('服务器错误');
                    break;
                default:
                    console.error('网络请求失败:', error.response.data?.error || '未知错误');
            }
        } else if (error.request) {
            // 请求发出但没有收到响应
            console.error('无法连接到服务器，请检查:', {
                baseURL: instance.defaults.baseURL,
                timeout: instance.defaults.timeout,
                error: error.message
            });
        } else {
            // 请求配置出错
            console.error('请求配置错误:', error.message);
        }
        return Promise.reject(error);
    }
);

// 测试连接
instance.get('/api/test')
    .then(() => console.log('后端服务连接正常'))
    .catch(error => console.error('后端服务连接失败:', error));

export default instance; 