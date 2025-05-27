
How open the camera stream so it can be used in frigate, Home Assistant....?

Note, the data is not secure! So everybody on your network has full access to the images.


# Installation

## Update your sofware

    sudo apt update

    sudo apt upgrade -y

    sudo apt install -y libcamera0 libfreetype6




## Install mediamtx

- Download te latest version and unzip

    cd /diy/

    wget https://github.com/bluenviron/mediamtx/releases/download/v1.12.2/mediamtx_v1.12.2_linux_arm64.tar.gz

    tar -xvf mediamtx_v1.12.2_linux_arm64.tar.gz --one-top-level

    rm *.gz

    mv mediamtx_v1.12.2_linux_arm64/* mediamtx/. 

    rm mediamtx_v1.12.2_linux_arm64/ -Rf

    cd mediamtx/

    vim mediamtx.yml 


- Add following to the 'path' section (path is here as reference, so make sure you don't have it twice in your config):

    paths:

      cam:

        source: rpiCamera

        rpiCameraWidth: 1280

        rpiCameraHeight: 720


## Test

- To test it, run:

     ./mediamtx mediamtx.yml 

- Open VLC on your desktop, and connect to:

    rtsp://<RP-IP-Adress>:8554/cam


## Auto-start

Create a service file using

    vim /etc/systemd/system/mediamtx.service


Add follwoing:

    [Unit]

    Description=MediaMTX service

    Wants=network.target

    [Service]

    ExecStart=/diy/mediamtx/mediamtx /diy/mediamtx/mediamtx.yml

    [Install]

    WantedBy=multi-user.target


To enable and run it?

    sudo systemctl daemon-reload

    sudo systemctl enable mediamtx.service
