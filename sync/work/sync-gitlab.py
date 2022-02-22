#!/usr/bin/env python3
# encoding: utf-8

__Author__ = 'Mango'
__Date__ = '2022-01-20'

import os
import sys
import time
import gitlab
import subprocess
import configparser

class GitlabAPI(object):
    def __init__(self, *args, **kwargs):
        cf = configparser.ConfigParser()
        self.home = os.getenv('HOME')

        if os.path.exists('/etc/python-gitlab.cfg'):
            self.gl = gitlab.Gitlab.from_config('public', ['/etc/python-gitlab.cfg'])
            cf.read('/etc/python-gitlab.cfg')
        elif os.path.exists(os.getenv('HOME') + '/.python-gitlab.cfg'):
            self.gl = gitlab.Gitlab.from_config('public', [os.getenv('HOME') + '/.python-gitlab.cfg'])
            cf.read(os.getenv('HOME') + '/.python-gitlab.cfg')
        else:
            print('You need to make sure there is a file named "/etc/python-gitlab.cfg" or "~/.python-gitlab.cfg"')
            sys.exit(5)

        self.name = cf.get("public", "name")
        self.passwd = cf.get("public", "passwd")
        self.namel = cf.get("school", "name")
        self.passwdl = cf.get("school", "passwd")
        self.host = cf.get("school", "host")

    def get_allprojects(self):
        #######获取gitlab的所有projects###
        projects = self.gl.projects.list(all=True)
        return projects

    def get_allgroups(self):
        #######获取gitlab的所有group名称以及ID###
        all_groups = self.gl.groups.list(all=True)
        return all_groups

    def get_allusers(self):
        #######获取gitlab的所有user名称以及ID###
        users = self.gl.users.list(all=True)
        return users

    def ass_group(self):
        #######获取gitlab指定组内所有user以及project名称以及ID信息，本例中组ID为58###
        gid = 34
        group = self.gl.groups.get(gid)
        members = group.members.list()
        projects = group.projects.list()
        for project in projects:
            print(group.name,project.path)

    def get_projectinfo(self, pid):
        #######获取项目信息#######
        project = self.gl.projects.get(pid)
        return project
    
    def need_to_pull(self, name, id):
        r = os.popen("cat "+ self.home + "/work/commit_id_map | grep '\[" + name + "\]' | awk '{print $2}'")
        for line in r.readlines():
            if line[:8] == id[:8]:
                return False
        return True

    def update_map_id(self, name, id):
        r = os.popen("cat "+ self.home + "/work/commit_id_map | grep '\[" + name + "\]' | awk '{print $2}'")
        for line in r.readlines():
            subprocess.call(["sed -i 's/"+ line[:8] + "/" + id + "/g' " + self.home + "/work/commit_id_map"], shell=True)
            return
        ########不在文件里面则写入########
        subprocess.call(["echo [" + name + "] " + id + " >> " + self.home + "/work/commit_id_map"], shell=True)

    def do_sync(self, project):
        os.chdir(self.home + "/work/repo/" + project.path);
        ret = subprocess.call(["git pull"], shell=True)
        if ret != 0:
            print("git pull faild", project.path)
            return False

        ret = subprocess.call(["git push school master"], shell=True)
        if ret != 0:
            print("git push faild", project.path)
            return False

        return True

    def do_sync_new(self, project):
        os.chdir(self.home + "/work/repo/")
        ret = subprocess.call(["git clone http://" + self.name + ":" + self.passwd + "@" + project.http_url_to_repo[7:]], shell=True)
        if ret != 0:
            print("git clone faild", project.path)
            return False

        os.chdir(self.home + "/work/repo/" + project.path);
        ret = subprocess.call(["git remote add school http://" + self.namel + ":" + self.passwdl + "@" + self.host + "/newland/" + project.path + ".git"], shell=True)
        if ret != 0:
            print("git remote add faild", project.path)
            return False

        ret = subprocess.call(["git push school master"], shell=True)
        if ret != 0:
            print("git push faild", project.path)
            return False

        return True
            
    def create_project(self, name):
        #######创建项目##########
        project = self.gll.projects.create({'name':name})
        project.branches.create({'branch':'origin','ref':'master'})

if __name__ == '__main__':
    git = GitlabAPI()

    projects = git.get_allprojects()
    for project in projects:
        if project.jobs_enabled == False:
            continue
        dirs = os.listdir(git.home + "/work/repo")
        if project.path in dirs:
            #######同步过的项目########
            print(project.http_url_to_repo)
            need = git.need_to_pull(project.path, project.commits.list()[0].short_id)
            ########有新的push########
            if need == True:
                print("syncing project", project.path)
                ret = git.do_sync(project)
                if ret == True:
                    ########更新commit id########
                    git.update_map_id(project.path, project.commits.list()[0].short_id)
        else:
            #######新的项目########
            print(project.http_url_to_repo)
            print("creating project", project.path)
            ret = git.do_sync_new(project) 
            if ret == True:
                ########新增commit id########
                git.update_map_id(project.path, project.commits.list()[0].short_id)
