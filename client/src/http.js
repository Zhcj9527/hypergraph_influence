import axios from "axios"//配置前后端交互的网络设置

//axios 响应拦截器
axios.interceptors.request.use(function (request) {
    return request//对响应数据做些事
})

// 请求方式的配置
export default {
    post(url, data){// post
        return axios({
            method:'post',//是创建请求时使用的方法
            url,//用于请求的服务器
            data,
            baseURL:'http://localhost:5000/',//便于为 axios 实例的方法传递相对的 URL
            headers:{//是即将被发送的自定义的请求头
                'Content-Type':'application/json;charset=UTF-8'
            },
            transformRequest:[function (data) {//
                return JSON.stringify(data)
            }]
        })

    },
    get(url, params){// get
        return axios({
            baseURL:'http://localhost:5000/',
            method:'get',
            url,
            params, // get 请求时带的参数
            headers:{
                'X-Requested-With':'XMLHttpRequest'
            },
            transformRequest:[function (data) {
                return JSON.stringify(data)
            }]
        })
    }
}