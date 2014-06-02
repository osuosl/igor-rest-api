# REST API Design

## Goals

The interface must allow the following operations from the client:

### User and Machine Management

   * Store machine credentials and assign tokens to permitted logged-in users
   * Update machines and machine credentials
   * Update access permissions for user-machine pairs

### IPMI Operations

   * Read and cycle machine power
   * View the serial-on-LAN console
   * View the system event log
   * View sensor readings

## Architecture

![Igor Architecture](https://docs.google.com/drawings/d/1KZ2L9Hj7nB1S1TfYvx17_ZtXdjvPtdZdmY92QE4KKlI/pub?w=960&amp;h=720 "Igor Architecture")

*[Diagram source](https://docs.google.com/drawings/d/1KZ2L9Hj7nB1S1TfYvx17_ZtXdjvPtdZdmY92QE4KKlI/edit?usp=sharing)*

A single REST server will serve as the gateway for all client users. The REST server is responsible for two main
tasks: user authentication and command execution. The architecture diagram above details these interactions.

## Interface

All operations will be implemented via HTTP verbs on URLS; see [here](http://blog.luisrei.com/articles/rest.html) for a nice REST reference.

### User and Machine Management Endpoints

`/machines`

   * `GET`: Lists the available machines
   * `POST`: Creates a new entry in the `CREDENTIALS` table

`/machines/:hostname`

   * `GET`: Get details for the `hostname` machine (credentials and permitted users)
   * `DELETE`: Deletes the entry for `hostname` from the `CREDENTIALS` table
   * `PUT/PATCH`: Update the entry for `hostname` in the `CREDENTIALS` table (credentials and permitted users)

`/users`

   * `GET`: Gets the list of users in the `USERS` table
   * `POST`: Create a new user in the `USERS` table

`/users/:username`

   * `GET`: Gets details for user `username` (eg. permitted machines)
   * `DELETE`: Delete user `username` from the `USERS` table
   * `PUT`: Update password for user `username` in the `USERS` table

`/login`

   * `GET`: Returns an authentication token to be sent with all future requests for this user

### IPMI Operations' Endpoints

`/machines/:hostname/chassis`

   * `GET`: Status information for `hostname` related to power, buttons, cooling, drives and faults.

`/machines/:hostname/chassis/power`

   * `GET`: Get the power status for `hostname`
   * `POST`: Set the power `on|off|cycle|reset` for `hostname`

`/machines/:hostname/sol`

   * `TODO`: What is a good way to both view and control SOL over a persistent HTTP connection?

`/machines/:hostname/sel`

   * `GET`: Prints the system event log (`first|last n` lines options can be provided via headers)

`/machines/:hostname/sensors`

   * `GET`: Lists the available sensors

`/machines/:hostname/sensors/:id`

   * `GET`: Returns the reading of the sensor `id`
   * `POST`: Updates the threshold of the sensor `id`
