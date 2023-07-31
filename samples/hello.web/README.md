# Hello World

### Start OpenSearch

```bash
./gradlew run -Dopensearch.experimental.feature.extensions.enabled=true
```

### Start the App

```bash
poetry install
petry run src/hello/hello.py
```

Try `curl http://localhost:1234`.

### Register the Extension

```bash
curl -XPOST "localhost:9200/_extensions/initialize" -H "Content-Type:application/json" --data @src/hello/hello.json
```
