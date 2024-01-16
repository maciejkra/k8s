Add readyness & liveness probe to python pod

* Redyness - should check TCP port
* Liveness - should check endpoind `/healthz` via HTTP

If the taks is completed the application should restart every 30 seconds and be ready all the time.