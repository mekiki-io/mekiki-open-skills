# Mekiki Open Skills

<img src="mekiki.png" alt="Mekiki" width="160">

Open catalog of software engineering skills used by [Mekiki](https://mekiki.io),
a platform that helps interviewers prepare software engineering interviews.

Every release publishes one `skills.json` file as a GitHub release asset.
Mekiki loads it and users build interview templates from these skills.

## Format

One YAML file per category in `src/`. The file name is the category id.

```yaml
name: Python
description: Core language, runtime and ecosystem.

skills:
  decorators:
    name: Decorators
    level: middle
    aliases: [function wrappers]
    prerequisites: [closures, first-class-functions]

  gil:
    name: GIL
    level: senior
    aliases: [Global Interpreter Lock]
    related: [multiprocessing, asyncio]
```

| Field | Required | Meaning |
|---|---|---|
| `name` | yes | Human readable name |
| `level` | yes | `junior`, `middle` or `senior` |
| `aliases` | no | Other names of the skill |
| `prerequisites` | no | Keys of skills in the same file to know first |
| `related` | no | Keys of skills in the same file that are close to this one |

A skill is referenced everywhere as `category.key`, for example `python.gil`.
The full schema is in [`catalog/schema.json`](catalog/schema.json).

## Rules

- Category ids and skill keys are lowercase words joined by `-`.
- `prerequisites` and `related` point to existing skills of the same file.
- **Keys live forever.** Users reference skills by key, so a released key can not be
  removed or renamed. Change `name` or add `aliases` instead.

The pipeline checks all of this on every pull request.

## Contributing

1. Add or change skills in `src/`.
2. Run the checks locally with [uv](https://docs.astral.sh/uv/) and `make`:

   ```sh
   make install   # dependencies into .venv
   make check     # validate skills, compare keys with the latest tag
   make unit      # tests
   make lint      # ruff and mypy
   ```

3. Open a pull request.

Run `make help` to see all targets.

## Release

Publish a GitHub release with a tag like `1.4.0`. The pipeline validates the skills,
builds `skills.json` and attaches it to that release.

To build the file locally:

```sh
make build VERSION=1.4.0
```

`skills.json` looks like this:

```json
{
  "version": "1.4.0",
  "categories": [
    {
      "id": "python",
      "name": "Python",
      "description": "Core language, runtime and ecosystem.",
      "skills": [
        {
          "id": "gil",
          "name": "GIL",
          "level": "senior",
          "aliases": ["Global Interpreter Lock"],
          "prerequisites": [],
          "related": ["multiprocessing", "asyncio"]
        }
      ]
    }
  ]
}
```

## License

[MIT](LICENSE)
