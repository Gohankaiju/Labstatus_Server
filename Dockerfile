# cuda,cudnn環境構築
FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-devel

# RUN apt-key del 3bf863cc
# RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub

# 必要なパッケージのインストール。Advanceにて書き換える箇所。
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    git \
    vim \
    sudo \
    curl \
    unzip \
    mysql-server \
    iputils-ping \
    net-tools \
    tmux && \
    rm -rf /var/lib/apt/lists/*
    
# user設定
ARG user=${user:-user}
ARG uid=${uid:-uid}
ARG gid=${gid:-gid}

# Anaconda環境構築
# ENV ANACONDA_ROOT=/opt/conda
# RUN curl -o ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
#     chmod +x ~/miniconda.sh && \
#     ~/miniconda.sh -b -p ${ANACONDA_ROOT} && \
#     rm ~/miniconda.sh && \
#     ${ANACONDA_ROOT}/bin/conda clean -ya 

# condaのpathを通す
# ENV PATH ${ANACONDA_ROOT}/bin:$PATH

# condaのpathが通っているか確認
# ARG PYTHON_VERSION=3.7.9
# RUN conda install -y python=$PYTHON_VERSION

# root権限で作成したディレクトリなどがsudo権限がないと操作できない問題対策
# dockerという仮のグループを作成し、ユーザーを追加することで権限を下げる。
RUN groupadd -g ${gid} docker && \
    useradd -g docker -u ${uid} -s /bin/bash ${user}

# sudoerに自分を追加、パスワードなしでsudoコマンドを使えるようにする
RUN echo ${user} ALL=NOPASSWD: ALL >> /etc/sudoers

# ホームディレクトリを最初に表示する
WORKDIR /home/${user}

# ホームディレクトリの権限をユーザに下げる
RUN chown -R ${user} /home/${user}

# pytorch installation
# RUN conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.6 -c pytorch -c nvidia
# RUN conda install pytorch torchvision torchaudio pytorch-scatter pytorch-cuda=11.8 -c pytorch -c nvidia -c pyg
# RUN pip install --no-index torch-scatter -f https://data.pyg.org/whl/torch-2.0.1+cu118.html
RUN conda install pytorch-scatter -c pyg
RUN pip install matplotlib
RUN pip install numpy
RUN pip install PyYAML
RUN pip install torchmetrics
RUN pip install torcheval
RUN pip install tensorboard
RUN pip install pillow

# 共通
RUN pip install Cython
RUN pip install tqdm
RUN pip install numba
RUN pip install Numpy-indexed
# RUN pip install strictyaml
### end ###

### slack通知用 ###
RUN pip install slackweb
RUN pip install slack-sdk

RUN pip install mysql-connector-python
RUN pip install Django
RUN pip install google-api-python-client
RUN pip install oauth2client
RUN pip install google-api-python-client oauth2client google-auth-httplib2 google-auth-oauthlib docopt
# 作成したユーザーに切り替える
USER ${uid}

# pipする際に警告を出さないためにpathを通す
ENV PATH /home/${user}/.local/bin:$PATH

RUN conda init
