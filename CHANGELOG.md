# v0.3.0

- remove update (use the callbacks instead)
- ability to register callbacks per id

# v0.3.1

- more typings

# v0.3.3

- add fan modes

# v0.3.4

- Add jobhandler to ensure only one command happens at a time [fixes](https://github.com/home-assistant/core/issues/134840)

# v0.3.5

- debug
- fix is return while it should raise

# v0.3.6

- ignore energy & thermostat events

# v0.3.9

- fix event not running

# v0.4.0

- port to async
- initial thermostat support
- initial energy support

# v0.4.1

- executions don't need their data returned and would block the events

# v0.4.2

- fix missing write

# v0.4.3

- let `connection.write` handle the string

# v0.4.4

- remove asyncio from requirements

# v0.4.5

- update the way thermostat and energy ids are handled

# v0.4.6

- fix energy id

# v0.4.7

- fix thermostat state
- cleanup controller a bit

# v0.4.10

- fix thermostat execution

# v0.4.11

- handle thermostat and dimmable light unit conversion internal

# v0.4.12

- Fix Dict error

# v0.4.13

- Remove unused logging setup from controller.py
- Add reverse mapping for thermostat modes

# v0.5.O

- Add scene support

# v0.5.1

- add nhcscene to nhcAction

# v0.5.2

- better typings

# v0.5.3

- fix scenes missing

# v0.6.1

- Fix brightness not set when toggling.

# v0.7.0

- Add blinds as a cover (temporary minimal support for blinds)
