# ReplayMod
A Minecraft mod to record game sessions and replay them afterwards from any perspective.

## Building
Make sure your sub-projects are up-to-date: `git submodule update --init --recursive`

This project targets Minecraft Forge 1.7.10 only. Use Java 8 and the included Gradle 5.4.1 wrapper. After the source conversion described below, run `./gradlew :jGui:1.7.10:setupDecompWorkspace :1.7.10:setupDecompWorkspace` after the initial clone, then `./gradlew :1.7.10:build`. The final jar is placed in `versions/1.7.10/build/libs/`.

The current shared Java source is still in the old 1.16.4 naming and conditional format. It must be converted to 1.7.10 source before a clean compile is possible; Gradle no longer configures intermediate Minecraft projects to perform that conversion.

### IntelliJ
Ensure you have at least IDEA 2020.1.
Import the root Gradle project after the 1.7.10 source conversion is complete.

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
The shared Java and resource sources still contain ReplayMod preprocessor directives. The 1.7.10 Gradle project keeps the preprocessor with `MC=10710` and `FABRIC=0`. The old mapping chain and intermediate Minecraft projects have been removed. The shared source tree still needs a one-time 1.7.10 source and name conversion before compilation.

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
