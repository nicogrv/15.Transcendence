
curl -F grant_type=authorization_code \
-F client_id=u-s4t2ud-9198daa6a4877961ff5b7a3ca58e5990fd4f618ddc61420e8aa18e18ed316472 \
-F client_secret=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 \
-F code=2baf581e9d095ef58e498b2b44517632b4dd8c4dce7ea98dd5ba99da42ee27d3 \
-F redirect_uri=http://127.0.0.1:8000/api/auth/test \
-X POST https://api.intra.42.fr/oauth/token