.PHONY: \
	setup \
	setup-clean \
	version \
	update-docker \
	migration \
	update-db \
	load-osm \
	locale-compile \
	dev-start \
	dev-stop \
	dev-logs \
	dev-clean \
	zstd-tracks-download \
	zstd-tracks

setup:
	# compile cython
	pipenv run python setup.py build_ext --build-lib cython_lib

setup-clean:
	rm -rf build/ cython_lib/*{.c,.so,.html}

version:
	sed -i -r "s|VERSION = '([0-9.]+)'|VERSION = '\1.$$(date +%y%m%d)'|g" config.py

update-docker:
	docker push $$(docker load < $$(nix-build --no-out-link) | sed -En 's/Loaded image: (\S+)/\1/p')

migration:
	@read -p "Migration name: " name; \
	alembic revision --autogenerate --message "$$name"

update-db:
	alembic upgrade head

load-osm:
	python ./scripts/load_osm.py $$(find . -maxdepth 1 -name '*.osm' -print -quit)

locale-compile:
	./scripts/locale_compile.sh

dev-start:
	[ -d data/pgadmin ] || install -d -o 5050 -g 5050 data/pgadmin
	docker compose -f docker-compose.dev.yml up -d

dev-stop:
	docker compose -f docker-compose.dev.yml down

dev-logs:
	docker compose -f docker-compose.dev.yml logs -f

dev-clean:
	docker compose -f docker-compose.dev.yml down
	rm -rf data/db data/pgadmin

open-pgadmin:
	xdg-open http://localhost:5433

zstd-tracks-download:
	pipenv run python ./scripts/zstd_tracks_download.py

zstd-tracks:
	zstd -o zstd/tracks.dict -19 --train-fastcover $$(find zstd/tracks/ -type f -name '*.gpx' -print0 | xargs -0)
