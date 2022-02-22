window.config = {

    domain: "",

    // ------------- 应用配置 ------------- 

    app_id: "",
    app_secret: "",
    app_version: "1.0.0.5", //本前端版本
    app_socker_compatibility: ["1.0.0.3"], //助手向下兼容版本

    // ------------- sso 相关 ------------- 

    web_host: "http://192.168.133.220:30097", // 本平台服务接口（部署环境下由网关统一授权验证）
    opt_host: "http://192.168.133.220:30095", // 本平台服务接口（部署环境下由网关统一授权验证）
    cloud_host: "http://192.168.133.220:30093/", // 云服务接口（获取用户信息等）
    redirect_uri: "http://192.168.133.220:30091/login?style=login_online&", // 统一登录
    redirect_register: "http://192.168.133.220:30091/register", // 统一注册
};


//window.onload = function () {
//    let script = document.createElement('script');
//    script.type = 'text/javascript';
//    script.src = window.config.emulator_host + '/lib/nleEmulatorLib.js';
//    document.getElementsByTagName('head')[0].appendChild(script);
//}
