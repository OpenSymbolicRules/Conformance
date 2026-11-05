# Entry points for the OSR conformance suites.

# Validate every suite against the schema and check digests.
check: validate digests

# Validate suites against schemas/cases.schema.json.
validate:
	check-jsonschema --schemafile schemas/cases.schema.json suites/*/*.cases.json

# Each suite must come from the rule set shipped next to it.
digests:
	python3 scripts/check_digests.py

# Refresh a suite from an OpenSymbolicRules/Lean export directory.
update lean_generated suite="trigonometry":
	cp {{lean_generated}}/conformance/{{suite}}.cases.json suites/{{suite}}/
	cp {{lean_generated}}/{{suite}}.osr.json suites/{{suite}}/
	just check
