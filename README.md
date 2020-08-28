# meetup-token-manager

Manages 0Auth2 access token for the [Meetup API](https://secure.meetup.com/meetup_api) in memory and in [Redis](https://redis.io/). Refreshes expired tokens automatically.


## Installation

### Dependencies

- You need to create a new 0Auth consumer [here](https://secure.meetup.com/meetup_api/oauth_consumers/).
- This package depends on a [Redis](https://redis.io/) to connect to.

### User Installation

```shell
pip install meetup-token-manager
```

## Usage Example

- Place your 0Auth consumers client id, client secret and redirect uri in the corresponding environment variables.
- Start Redis and have it available at `http://localhost:6379`.

```python
>>> import os

>>> from redis import Redis

>>> from meetup.token_cache import TokenCache
>>> from meetup.token_cache.utils import make_authorization_url


>>> redis_client = Redis.from_url("redis://@localhost:6379?db=0&decode_responses=True")

>>> token_cache = TokenCache(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    redirect_uri=os.environ["REDIRECT_URI"],
    redis_client=redis_client,
)

# Navigate to the following url, authorize the consumer, copy the `code` parameter
# from the redirect uri and store it in the `CODE` environment variable.
# You will only have to do this step once, as long as you persist the tokens in Redis.
>>> make_authorization_url(
    client_id=os.environ["CLIENT_ID"],
    redirect_uri=os.environ["REDIRECT_URI"],
)
>>> token_cache.authorize(code=os.environ["CODE"])

# Whenever you access the `token` property the package will validate whether your token
# has expired and if so, will request a fresh token from the API.
>>> token_cache.token
```

You can find an interactive example in the [example.py](notebooks/example.py) notebook ([jupytext](https://github.com/mwouts/jupytext) required).

## License

Please see the [LICENSE](LICENSE) for details.

## Changelog

Please see the [CHANGELOG.md](CHANGELOG.md) for details.

## Development

We welcome new contributions to the project!

### Requirements

- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)

### Source Code

You can check out the latest source code at: `https://github.com/janjagusch/meetup-token-cache`.

### Linting

`make lint`

### Testing

`make test_redis`

## Help

### Authors

- Jan-Benedikt Jagusch <jan.jagusch@gmail.com>

### Acknowledgements

- This project was heavily inspired by [oauth-token-cache](https://github.com/NikolaiGulatz/oauth-token-cache).
