# Development

## Docker

Override the default compose setup with the dev one:

```
ln -s docker-compose.dev.yml docker-compose.override.yml
```


## Debugging

The Flask debugger is automatically enabled by `docker-compose.dev.yml`. Just trigger an
error and enter the PIN from the logs.


## Profiling

### Python profiling

Uncomment the relevant lines in `docker-compose.dev.yml`. Ensure you have a self-owned
`.prof` directory created before running the container.

Visualize the debugger results:

```
conda install snakeviz
snakeviz --hostname 0.0.0.0 --port 5001 -s .prof
```


### Dask profiling

Uncomment the relevant lines in `docker-compose.dev.yml`. Read `__init__.py` comments
very carefully. The Dask Dashboard is very flaky in this app configuration. Is it
because of Flask somehow?
