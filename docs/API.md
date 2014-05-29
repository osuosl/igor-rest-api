# REST API Design

## Goals

The interface must allow the following operations from the client:

### IPMI Operations

   * Read and cycle machine power
   * View the serial-on-LAN console
   * View the system event log
   * View sensor readings

### User and Machine Management

   * Store machine credentials and assign tokens to permitted logged-in users
   * Update machines and machine credentials
   * Update access permissions for user-machine pairs

## Architecture

![Igor Architecture](https://docs.google.com/drawings/d/1KZ2L9Hj7nB1S1TfYvx17_ZtXdjvPtdZdmY92QE4KKlI/pub?w=960&amp;h=720 "Igor Architecture")

*[Diagram source](https://docs.google.com/drawings/d/1KZ2L9Hj7nB1S1TfYvx17_ZtXdjvPtdZdmY92QE4KKlI/edit?usp=sharing)*

A single REST server will serve as the gateway for all client users. The REST server is responsible for two main
tasks: user authentication and command execution. The architecture diagram above details these interactions.
