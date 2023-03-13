# Settings

Main concept behind Moni is simplicity. For that, it uses declarative YAML settings. Choose what you like from Checkers, Handlers and Integrations, set up Bot/Watchdog and you're ready to go.<br>
Consult with `example.settings.yml` or follow up with an **Example**.

## Basic server parameters
Shared across all checkers are `cycle`, `handlers`, `protocol`, `port`, `back_to_normal`, `back_to_normal_cycle`.

-   `cycle`: `integer | float`<br>
    Seconds to wait between checks. Defaults to 300 seconds or 5 minutes. 
!!! info "Precision"
    Since Moni relies heavily on asynchronicity, this is implemented as a sleep between checks. For that, `cycle` is not absolute and may be slightly delayed
    by other running code.

-   `handlers`: `list[str]`<br>
    List of handlers, through which alerts will be sent. For example `[console, log, slack]` will output to `STDOUT`, write to `./logs/moni.log`
    and send a message to a *Slack* channel. Those 3 **Handlers** would have to be explicitly defined in the settings as well. 

-   `protocol`: `http`, `https`<br>
    Protocol to use for the requests. Defaults to `https`. 

-   `port`: `int`<br>
    Port to use for the requests. Defaults to not `None`, so 443(HTTPS) and 22(SSH) are used. 

-   `back_to_normal`: `bool`<br>
    Optional "back to normal" messages. On a negative check alert normally, on further negative checks do not alert again, on a successful check send "back to normal" message. Defaults to `False`.

-   `back_to_normal_cycle`: `integer | float`<br>
    Optional back to normal follow up cycle. Set this to less than `cycle` to do follow up checks faster. Defaults to `cycle`. 

-   `not_normal_for`: `integer`<br>
    Alert only when server check fails this number of cycles. Defaults to 1. 

## Defaults
Default parameters might be specified to avoid repeating them for each server. Can be defined on a specific Checker or Global level.<br>
Lookup order is Server, Checker, Global.

## Request timeout
You can set a custom timeout for **Checkers** requests to your servers. Default is:
~~~~ YAML title="settings.yml"
request_timeout: 10
~~~~

## Moni self alert
Moni can send messages when it is starting up or shutting down.
~~~~ YAML title="settings.yml"
on_startup_handlers: [...]
on_shutdown_handlers: [...]
~~~~

## Datetime format
For certain **Handlers** (like **ConsoleHandler** and **LogHandler**) a timestamp is used. You can customize the format. Default is:
~~~~ YAML title="settings.yml"
dttm_format: '%Y-%m-%d %H:%M:%S'
~~~~


## Logging
If you want to make sure that you've set everything correctly and checks are actually running, you can set Moni internal logging level from default `info` to `debug`.
~~~~ YAML title="settings.yml"
logger_level: debug
~~~~
And see something like:
~~~~ console
Running PingChecker(podkosa.github.io)
Finished PingChecker(podkosa.github.io)
~~~~
