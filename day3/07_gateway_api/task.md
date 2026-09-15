# Zadanie

Wystaw aplikację python-api (z day2/11) przez Gateway API pod adresem `api.127-0-0-1.nip.io`.

Prereq: Envoy Gateway zainstalowany — patrz `README.md` → Kroki 1–3.

1. Upewnij się, że Gateway `training-gateway` istnieje i jest `PROGRAMMED=True`
   (`kubectl apply -f gateway-http.yaml`).
2. Napisz `HTTPRoute`, który dla hosta `api.127-0-0-1.nip.io` kieruje cały ruch
   na Service `python-service` (port **5002**).
3. Sprawdź:
   ```sh
   kubectl get gateway training-gateway
   curl http://api.127-0-0-1.nip.io/api/v1/info
   ```

EXTRA: dodaj do swojego HTTPRoute filter tak, żeby **każda** ścieżka trafiała na `/api/v1/info`.

```sh
curl http://api.127-0-0-1.nip.io/cokolwiek    # to samo co /api/v1/info
curl http://api.127-0-0-1.nip.io/foo/bar/baz  # to samo
```

Podpowiedź: filter `URLRewrite` z `path.type: ReplaceFullPath` (`ReplacePrefixMatch` zostawia resztę ścieżki).
