# 创建k8s集群部署jupyterhub
## 安装sealos
   下载并安装sealos, sealos是个golang的二进制工具，直接下载拷贝到bin目录即可, release页面也可下载
   ```
   wget -c https://sealyun.oss-cn-beijing.aliyuncs.com/latest/sealos && chmod +x sealos && mv sealos /usr/bin
   ```
## 安装k8s集群
   安装一个master的kubernetes集群
   ```
   sealos init --passwd 'Newland@eduAI' --master 192.168.133.220 --pkg-url ./kube1.18.18.tar.gz --version v1.18.18
   ```
   设置主节点可起pod
   ```
   kubectl taint nodes --all node-role.kubernetes.io/master-
   ```
## 部署jupyterhub
   部署storgeclass
   ```
   kubectl apply -f local-path-storage.yaml
   ```
   设置默认的storageclass
   ```
   kubectl patch storageclass local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
   ```
   安装helm，使用helm部署jupyterhub
   ```
   helm upgrade --cleanup-on-fail --install jupyterhub ./jupyterhub-1.1.3.tgz --namespace hub --create-namespace --values jupyterhub-config.yaml --set-file hub.extraFiles.my_config.stringData=jupyterhub_config.py
   ```
