# Containers (Linux)
- **docker** doesn't use all the new kernel features for containerization
    - dockerd uses root to manipulate namespaces and cgroups
- **RedHat's podman**
    - modern, user-level container manipulation
    - daemonless

## Namespaces
- 8 druhu
- kazdy namespace tvori hierarchii
- ovlada se pres `/proc/<pid>/uid_map`
- vytvareni novych namespacu - unshare, clone

### Current unresolved problems
- process with PID=1 has two special roles
    - controls daemons - controlled by systemclt via named pipe
    - collests zombie
- but inside typical container, PID=1 is shell, not special daemon
    - cannot respond to systemctl requests
    - systemctl doesn't work
- sudo refuses to work, because `sudo.conf` is owned by `nobody`


## Different container philosofies
- who wins, nobody knows
### Docker
- container are lightweight, typically only one process
- connection between processes handled outside the containers
    - connections managed and orchestrated by Kubernetes 
- software update
    - drop container, start another

### Red Hat
- containers shall be like computers
- container contains entire business application
    - consists of many processes (apache, mysql, java, cron, tomcat, ...)
- application configuration in sophisticated installation scripts
- installation scripts shall work inside containers

## What *are* containers exactly?
- **image**
    - read-only filesystem (like .iso image)
    - plus additional metadata (interface declarations, defaults, container setup)
- **container**
    - image
    - writable layer above the image filesystem
        - keeps tracks of changed files (CoW)
        - destroyed on container kill
    - set of mounts
        - host directories visible from container
        - survives container restart (like during container update from updated image)
        - set of ports mapped via virtual networks
- **running container**
    - container process running

### Image, writable layer on top
- image is created by adding layers
    - to another image or empty filesystem ("From scratch")
- each layer can be
    - files copied from elsewhere
    - result of installation process
        - when done, freezed to RO image
- layers combined using *union filesystems*
    - unionfs, overlays
    - must support deleting - **whiteout**
- container manager may reuse lower layers
    - when layers were created by the same command
    - lowered disk space consumption

### Docker
#### Dockerfile
- sequential script of commands
    - commands may create new writable layer
- commands
    - direct filesystem modifications
        - FROM
        - COPY
    - indirect filesystem modifications
        - RUN
            - create writable top layer
            - run specified command in WORKDIR
            - freeze writable layer
    - set startup process
        - ENV
        - CMD/ENTRYPOINT
    - metadata
        - VOLUME - mounts
        - EXPOSE - port list
- ENV, CMD, VOLUME, EXPOSE don't change the freezed image

### Docker container build and management
- docker build
    - read Docker file
    - pull base images from docker hub
    - produce container image
- docker image pull/push
    - download/publish image to registry
- docker create
    - create writable layers
    - link mountpoints
    - connect ports
    - result: stopped container

- docker start/exec
    - start different process than the one specified by CMD in Dockerfile
- docker stop/kill
    - sends UNIX signals to container processes
- docker-compose
    - config: docker-compose.yml
    - build and test containers
    - repo operations
    - combining more containers together
        - connecting multiple service containers
    - useful for deployment




# Virtualization (history)
- creating illusion, that OS has hardware all for himself

## IMB S/370
- 1971
- 512 KB RAM, ~ $1M 
- cloned by USSR - [ES EVM](https://en.wikipedia.org/wiki/ES_EVM)

