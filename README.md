# EMC for Relics

Adds authored ProjectE EMC values for Relics in Forge 1.20.1 and NeoForge 1.21.1. Trained relics have the same base EMC as fresh relics. ProjectE learns and reproduces the default fresh state; trained relic duplication is not intended.

Prices are author design choices. With the pinned Forge host, representative Roller Skates were measured at 4096 EMC in trained and fresh states. A level-5 item was sellable, while table and condenser reproduction returned default, untrained state. Table output survived save/reopen; condenser output was saved with zero ability points and no leveling tag. Other individual prices were not all measured. With the pinned NeoForge host, instrumented level-5 Roller Skate was also sellable for 4096 EMC, and table reproduction returned a fresh 4096-EMC stack with zero points/default leveling. The fresh stack survived save/reopen and remained 4096 EMC after datapack reload. The NeoForge condenser produced two 4096-EMC default-state stacks from one diamond with the trained item as target; both saved outputs had zero ability points and default leveling. Public CurseForge publication awaits the earlier project approval sequence.

Forge target: Relics 0.8.0.13 / ProjectE PE1.0.1; NeoForge target: Relics 0.12.8 / ProjectE PE1.1.0.

Both ports are data-only lowcodefml JARs. Canonical source is under `ports/`.

Build both ports with Python 3.11+: `python3 build.py`. Use `--cell forge1201` or `--cell neoforge1211` to build one port. Outputs are deterministic data-only JARs under `build/`; no Gradle or host downloads are needed.
