pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
        google()
        maven("https://jitpack.io")
        // The retained preprocessor resolves tiny-mappings-parser from Fabric's Maven.
        maven("https://maven.fabricmc.net")
    }
    resolutionStrategy {
        eachPlugin {
            when (requested.id.id) {
                "com.replaymod.preprocess" -> {
                    useModule("com.github.ReplayMod.preprocessor:preprocessor:${requested.version}")
                }
            }
        }
    }
}

val jGuiVersions = listOf("1.7.10")
val replayModVersions = listOf("1.7.10")

rootProject.buildFileName = "root.gradle.kts"

include(":jGui")
project(":jGui").apply {
    projectDir = file("jGui")
    buildFileName = "preprocess.gradle.kts"
}
jGuiVersions.forEach { version ->
    include(":jGui:$version")
    project(":jGui:$version").apply {
        projectDir = file("jGui/versions/$version")
        buildFileName = "../../build.gradle"
    }
}

replayModVersions.forEach { version ->
    include(":$version")
    project(":$version").apply {
        projectDir = file("versions/$version")
        buildFileName = "../../build.gradle"
    }
}
