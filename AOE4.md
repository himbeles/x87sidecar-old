# AoE IV helper source

This branch carries the combined software-fault/x87 helper used by the Highball
AoE IV engine. Build it with CMake for arm64 and sign `build/bin/x87sidecar`.

Based on [NerRobDog/x87sidecar](https://github.com/NerRobDog/x87sidecar/tree/c407ddfabbbe6bc5f5d56a258a4866ac89b04d8e),
which builds on athei and Lifeisawful. The following changes are the MIT-licensed
patches from [MacGames](https://github.com/tarikbc/macgames/tree/1579841b15ce569807b92af95b478c752c26df3d/patches/x87sidecar):

- Compose the software-fault and x87 decoders.
- Hand GS/TLS blocks back to Rosetta before custom x87 emission.
- Flush deferred FBLD pops before allocating input registers.

The original license notices remain in the source. Highball pins a full commit
SHA in `inputs.json` and builds this source in its engine workflow.
