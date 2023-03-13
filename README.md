<p align="center">
<a href="https://podkosa.github.io/moni/" title="Moni Docs"><img src="https://repository-images.githubusercontent.com/557768275/74d0d325-9309-4293-af48-3daf6f129a1c"></a>
<br>
<em>a monitoring bot for your servers</em>
</p>

**Current features:**

- :robot: Bot: HTTP-server for on-demand checks
- :dog: Watchdog: Compact daemon for monitoring and alerting
- :mag: Checkers: Ping, Celery/Flower, Docker containers (through SSH)
- :loudspeaker: Handlers: Slack, Webhook, Log, Console
- :speech_balloon: Integrations: Slack
- :fire: Speed: Async requests, Python 3.11, uvloop and FastAPI ensure the max gauge of your *Python* 
speedometer
- :hibiscus: Settings: Declarative YAML. Fine tune to your liking or fire-and-forget.
- :whale2: Docker: Pull the latest image from <a href="https://hub.docker.com/repository/docker/podkosa/moni" title="DockerHub">podkosa/moni</a>
- :notebook: Docs: <a href="https://podkosa.github.io/moni/" title="Moni Docs">Moni Handbook</a>. Interactive docs at <a href="http://localhost:6767/docs" title="OpenAPI">/docs</a>

## Bot

HTTP server, handling incoming requests (REST, slash commands, integrations, webhooks etc.). On-demand checks.

## Watchdog

Periodically monitors servers with Checkers and alerts through Handlers.
Can be run in two ways:

1. Integrated (default).
Launch inside the bot async event loop. *Keep in mind that they both will share a single thread, therefore can impact performance and even block one another.*
More compact option, but not fit for scaling.
2. Standalone.
Run `watchdog.py` as a separate process/container, even without the bot.
3. Disabled.
You can turn off the watchdog completely and run checks from the bot at your own pace.

## Settings

Define your servers, handlers, integrations and other settings declaratively in `settings.yml`. See `example.settings.yml`.<br>

## Integrations

- Slack: alerts to channels and slash commands. Install Moni in your Workspace with `./integrations_docs/slack_app_manifest.yml`.

## TODO

- Telegram integration
- Email handler
- Slack timeout for /commands is 3 seconds. Refactor to delay the response.
- Slack button on an alert to open up related service
- Web interface for settings and checks
- Endpoint to show loaded checkers and handlers
- Endpoint to add servers to monitoring, turn on/off already configured ones
- More alert handlers
- More server checkers
- Proper loop exit
- Optional multiprocessing, when there will be more checkers
- Tests
