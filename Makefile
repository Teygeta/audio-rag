show-db:
	python3 rag_system/verifier.py

.PHONY: verify

clean-db:
	python3 rag_system/cleaner.py

.PHONY: clean

clean-full-db:
	python3 rag_system/cleaner.py delete-all

.PHONY: clean-full-db

upload:
	python3 main.py --upload

.PHONY: upload

ask:
	python3 main.py --query "$(QUERY)"

.PHONY: ask

check-setup:
	python3 verify_setup.py

.PHONY: check-setup

setup:
	./setup.sh

.PHONY: setup