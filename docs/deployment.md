# Deployment

The production Docker image must serve the prebuilt Angular app with `nginx`.
It must not run `ng serve`, because Angular's development server watches files,
rebuilds repeatedly in containers, and can eventually exhaust the Node.js heap.

## Production Start

```bash
docker compose down --remove-orphans
docker compose build --no-cache navigator
docker compose up -d --force-recreate navigator
```

Check that the running process is `nginx`:

```bash
docker compose exec navigator ps aux
```

Expected output should include `nginx: master process` and `nginx: worker process`.
If it shows `ng serve` or `npm start`, the VPS is still running an old image,
an old `Dockerfile`, or a different compose override.

## Useful Checks

```bash
docker compose logs --tail=50 navigator
docker compose exec navigator wget -qO- http://127.0.0.1:4200/ | head
docker image inspect veil --format '{{.Config.Cmd}} {{.Config.Entrypoint}}'
```

Production logs should look like normal `nginx` access/error logs. They should
not show repeated Angular messages such as `Browser application bundle generation
complete`, `Compiled successfully`, or Node.js heap errors.
