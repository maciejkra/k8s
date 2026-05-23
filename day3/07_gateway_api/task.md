# Zadanie — Gateway API

Wystaw aplikacje na świat przez **Gateway API** (Envoy Gateway) zamiast Ingress.
Backendy gotowe w `backends.yaml`: `demo-app` (nginx) i `echo-app` (echo-server).

## Część 0 — instalacja i ekspozycja

1. Zainstaluj Envoy Gateway (`kubectl apply` z `install.yaml` — patrz `README.md`, Krok 1).
2. Doprowadź do tego, żeby `curl http://localhost/` trafił do klastra:
   - **Docker Desktop** — nic nie trzeba.
   - **kind** — `envoyproxy-hostport.yaml` + patch GatewayClass (Krok 2).
3. Sanity check z `README.md` (Krok 3): `curl http://localhost/` zwraca stronę nginx.
   Status Gateway: `kubectl get gateway training-gateway` → `PROGRAMMED=True`.

## Część 1 — routing po ścieżce

1. Zaaplikuj `fanout/httproute-path.yaml`.
2. Sprawdź:
   - `curl http://demo.127-0-0-1.nip.io/` → nginx
   - `curl http://demo.127-0-0-1.nip.io/echo` → echo-server
3. **Pytanie:** dlaczego `/echo` trafia do echo, a `/` do nginx, skoro `/` pasuje
   też do `/echo`? (most-specific-match)

## Część 2 — routing po nazwie hosta

1. Zaaplikuj `host/httproute-host.yaml`.
2. Sprawdź `nginx.127-0-0-1.nip.io` i `echo.127-0-0-1.nip.io`.
3. **Pytanie:** czego Envoy używa do wyboru reguły? (nagłówek `Host`)

## Część 3 — URLRewrite

1. Zaaplikuj `fanout/httproute-rewrite.yaml`.
2. `curl http://demo.127-0-0-1.nip.io/legacy/v1` — w odpowiedzi echo-server pokaże,
   jaką ścieżkę dostał backend. Jaka to ścieżka i dlaczego?
3. **Pytanie:** jak to samo zrobiłbyś w starym Ingress? (adnotacja `rewrite-target`)

## Część 4 — TLS

1. Wariant A (openssl) **lub** B (cert-manager `selfSigned`) z `tls/README.md` —
   doprowadź do działającego `https://demo.127-0-0-1.nip.io/` (z `-k`).
2. W `curl -kv` znajdź linie `subject:` i `issuer:`. Co potwierdza, że cert jest self-signed?
3. **Pytanie:** dlaczego Let's Encrypt z HTTP-01 nie zadziała dla `127-0-0-1.nip.io`
   z lokalnego klastra? Co zrobić zamiast tego?

## Pytania podsumowujące

- Wymień **3** różnice między `HTTPRoute` a starym `Ingress`.
- Jaką rolę pełni `GatewayClass`, a jaką `Gateway`?
- Co to jest "annotation hell" w Ingress i jak Gateway API go unika?

## Bonus

Skonfiguruj przekierowanie **HTTP → HTTPS** (cały ruch z `:80` na `:443`) — przez
`HTTPRoute` z filterem `RequestRedirect`.
