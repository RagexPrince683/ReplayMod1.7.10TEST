# ReplayMod
A Minecraft mod to record game sessions and replay them afterwards from any perspective.

## Building
Make sure your sub-projects are up-to-date: `git submodule update --init --recursive`

This project targets Minecraft Forge 1.7.10 only. Use Java 8 and the included Gradle 5.4.1 wrapper. After the initial clone, run `./gradlew :jGui:1.7.10:setupDecompWorkspace :1.7.10:setupDecompWorkspace`, then `./gradlew :1.7.10:build`. The final jar is placed in `versions/1.7.10/build/libs/`.

The current shared source is the authoritative source. The Gradle build preprocesses both jGui and ReplayMod through their version mapping chains before their Forge 1.7.10 `compileJava` tasks. To check compilation directly, run `./gradlew :jGui:1.7.10:compileJava :1.7.10:compileJava`.

For optional development mods, place Forge 1.7.10 `.jar` files directly in the project-root `devmods/` folder and run `./gradlew :1.7.10:runClient`. Add or remove jars there before the next launch; no build-script edit is needed. ForgeGradle remaps each local jar into `versions/1.7.10/build/generated-devmods/` using the project's stable 12 mappings: jars with SRG Minecraft member references use SRG-to-MCP, while other jars use Notch-to-MCP. The remapper uses the current ReplayMod and jGui development jars for inheritance lookup. The remapped jars join the initial launch classpath so their coremods, tweakers, and classes are available before mod discovery. Forge scans that classpath for their mods. Forge's `--mods` argument loads ReplayMod's current compiled development jar, and ReplayMod classes remain on the launch classpath for its early core plugin and tweaker.

If `devmods/` contains the UniMixins all-in-one coremod, its remapped jar is placed first on the launch classpath so its embedded Mixin runtime is available before ReplayMod's tweaker runs. ReplayMod's bundled Mixin 0.7 remains the development provider when UniMixins is absent. This runtime selection does not change the Mixin compile or annotation processor dependencies, or release packaging. Development jars are omitted from `--mods` because Forge already discovers them from the classpath and scanning both routes duplicates their mods.

Development jars must target Forge/Minecraft 1.7.10 and use a supported Notch or SRG Minecraft namespace. The tested MCHELI `476d0ef` jar also contains five preexisting SRG/MCP method aliases that collide under a plain SRG-to-MCP remap; the build preserves those aliases while remapping its other references. Other mixed-name jars may need their own mapping exceptions. The tested MCHELI jar lacks some assets referenced during client initialization, including `textures/items/ohiotrident1.png` and `sounds/aps_snd.ogg`; remapping does not supply missing resources. Remapping also cannot fix incompatible APIs or reflective references to obfuscated names. The ReplayMod project path cannot contain commas because Forge uses commas to separate the development jar's `--mods` entry. The local jars are not ReplayMod compile dependencies and are not included in release jars.

### IntelliJ
Ensure you have at least IDEA 2020.1.
Import the root Gradle project with Java 8.

### Eclipse

## Development
### Branches
Loosely based on [this branching model](http://nvie.com/posts/a-successful-git-branching-model/) with `stable` instead of `master`.

TL;DR:
Main development happens on the `develop` branch, snapshots are built from this branch.
The `stable` branch contains the most recent release.

The `master` branch is solely to be used for the `version.json` file that contains a list of all versions
used by the clients to check for updates of this mod.

### The Preprocessor
The shared Java and resource sources contain ReplayMod preprocessor directives. `versions/mainProject` and `jGui/versions/mainProject` select the current 1.16.4 source as the root of each mapping chain. Intermediate Gradle projects use `preprocess-only.gradle`: they expose source sets, mapping files, and signature-only class stubs to the retained preprocessor, but they do not apply Loom or ForgeGradle, compile Java, or build jars. Only `:1.7.10` and `:jGui:1.7.10` are Minecraft build targets, using ForgeGradle 1.2.

Pinned mapping and API signature inputs live in `preprocess-metadata/`. The API files contain class and member declarations only; generated stub jars stay under each project's `build/` directory. `preprocess-metadata/extract-api.py` regenerates a signature file from a mapping-era jar when these inputs need updating. The normal build does not use Python or download intermediate Minecraft versions.

### Versioning
The ReplayMod uses the versioning scheme outlined [here](http://mcforge.readthedocs.io/en/latest/conventions/versioning/)
with these changes:
- No `MAJORAPI`, the ReplayMod does not provide any external API
- The Minecraft target is fixed at Forge 1.7.10.
- For pre-releases the shorter `-bX` is used instead of `-betaX`

When a new version is (pre-)release, a new commit modifying the `version.txt` file should be added and the
`versions.json` file in the `master` branch should be updated. To simplify this process the gradle task `doRelease` can
be used: `./gradlew -PreleaseVersion=2.0.0-rc1 doRelease`. It will create the commit and update the version.json
accordingly.

Care should be taken that the updated `version.json` is not pushed before a jar file is available on the
download page (or Jenkins) as it will inform the users of the update.

### Bugs
GitHub should generally be used to report bugs.

In the past, bugs were tracked via [Bugzilla](https://bugs.replaymod.com/), so bug numbers in commits prior to 2020 such as `(fixes #42)` generally referred to Bugzilla unless noted otherwise.

## License
The ReplayMod is provided under the terms of the GNU General Public License Version 3 or (at your option) any later version.
See `LICENSE.md` for the full license text.
