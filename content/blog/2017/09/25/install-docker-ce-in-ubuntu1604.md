Title: Ubuntu 16.04 LTSにDocker CE stable最新版をインストール
Date: 2017-09-25 23:29:44
Category: Linux
Tags: Ubuntu
Slug: install-docker-ce-in-ubuntu1604
Authors: raimon
Summary: Ubuntu 16.04 LTSにaptパッケージ版のDocker CE stable最新版をインストールしてsudo不要で使えるようにする

Docker Community EditionをUbuntu 16.04 LTS向けに用意されているaptパッケージ版でインストールした。

## 環境

```sh
$ cat /etc/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=16.04
DISTRIB_CODENAME=xenial
DISTRIB_DESCRIPTION="Ubuntu 16.04.2 LTS"
```

## Docker repositoryのために準備

HTTPS経由でaptパッケージ導入できるよう、関連パッケージを準備しておく。

インストール済みであると言われた時は、気にせず次に進んで構わない。

```sh
$ sudo apt-get update
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```

Docker公式のGPG keyを追加して確認。

```sh
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
OK
$ sudo apt-key fingerprint 0EBFCD88
pub   4096R/0EBFCD88 2017-02-22
      フィンガー・プリント = 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
uid                  Docker Release (CE deb) <docker@docker.com>
sub   4096R/F273FCD8 2017-02-22
```

## Docker repositoryからdocker-ceパッケージをインストール

アーキテクチャ別に用意されている中から `x86_64` 向けリポジトリを選択して追加し、 `docker-ce` パッケージをインストールする。

```sh
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

$ sudo apt-get update
$ sudo apt-get install -y docker-ce

$ sudo docker version
Client:
 Version:      17.06.2-ce
 API version:  1.30
 Go version:   go1.8.3
 Git commit:   cec0b72
 Built:        Tue Sep  5 20:00:17 2017
 OS/Arch:      linux/amd64

Server:
 Version:      17.06.2-ce
 API version:  1.30 (minimum version 1.12)
 Go version:   go1.8.3
 Git commit:   cec0b72
 Built:        Tue Sep  5 19:59:11 2017
 OS/Arch:      linux/amd64
 Experimental: false
```

Dockerサービスの自動起動が設定されたかは、  `systemctl` コマンドで確認できる。

```sh
# docker.serviceがenabledとなっていれば有効になっている
$ systemctl list-unit-files
```

## sudo権限不要でdockerコマンドが実行できるようにグループ追加

これでDockerエンジンとdockerクライアントコマンドが使えるようになったが、sudo権限付きで実行しないとパーミッション違反となり、実行を拒否されてしまう。

```sh
$ docker run hello-world
docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post http://%2Fvar%2Frun%2Fdocker.sock/v1.30/containers/create: dial unix /var/run/docker.sock: connect: permission denied.
```

開発環境用途においては不便なため、dockerグループを追加して、開発者アカウント（ここでは自分自身）をグループに所属させる。

```sh
# dockerグループが居なければ追加
$ sudo groupadd docker

# 自分自身をdockerグループに所属
$ sudo usermod -aG docker $USER

# 一度ログアウト
$ logout

# 再度ログインし、dockerグループに所属していることを確認
$ groups
sudo docker
```

自身のアカウントがdockerグループに所属していると、sudo不要でdockerコマンドが利用できる。

Docker Hubからhello-worldのイメージを取得して実行させる時にも、sudo権限は無くても拒否されなくなっている。

```sh
$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
5b0f327be733: Pull complete
Digest: sha256:1f19634d26995c320618d94e6f29c09c6589d5df3c063287a00e6de8458f8242
Status: Downloaded newer image for hello-world:latest
```

## 参考情報

* [Get Docker CE for Ubuntu | Docker Documentation](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-repository "Get Docker CE for Ubuntu | Docker Documentation")
* [Post-installation steps for Linux | Docker Documentation](https://docs.docker.com/engine/installation/linux/linux-postinstall/#manage-docker-as-a-non-root-user "Post-installation steps for Linux | Docker Documentation")
