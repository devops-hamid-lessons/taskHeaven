# TaskHeaven: A Sample Rest gRPC to Create Redmine Tasks (Issues)

```text
TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
T      ==**==    **      *()-   *K *            TT
T      ******   *  *    ($$)    * *             TT
T        **    ******   ($)     **              TT
T        **    **  **   | \     * ** Heaven **  TT
TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
```

This service provides a gRPC method which accepts a Redmine server credentials plus an Task details and then writes it to the Redmine Server.

Redmine is a known Project Management Tool.

## Requirement

Requirement         | Specification
------------------- | ----------------------
OS                  | Ubuntu 20.04 LTS
Language            | Python, bash
Interpreter         | Python 3.7+

## Enable rest on the Redmine server
First step to use this service is to enable `rest` on your Redmine server using steps below:
1. Go to `Administration -> Settings -> API`
2. Tick `Enable REST web service` and then Save it like following screenshot.


## Install and Run

Clone project to a folder and then Simply run,

```bash
sudo chmod +x install.sh && sudo ./install.sh
```
It will install all required packages and prepare a python virtual environment.

then run,

```bash
./run.sh --bind <ip>:<port>
```

Which will run the gRPC service and `<ip>` and `<port>` denote the address and port to bind the service.

After execution, the service will respond to `gRPC` requests from clients.
In order to close the service run,

```bash
Ctrl + C
```

__Note__  
`TRACE`s are written to `stdout` and `LOG`s are written to `stderr`.

