# AoE IV helper source

Based on [athei/x87sidecar](https://github.com/athei/x87sidecar/tree/052944fc613e187f5e238bfa362b411787045d6b).
This branch adds AoE IV software-fault handling composed with the x87 decoder,
plus an FBLD deferred-pop fix and regression case. Build with CMake for arm64
and sign `build/bin/x87sidecar`. Highball pins a full commit SHA in `inputs.json`
and builds the source in its engine workflow.

The software-fault hook comes from [NerRobDog's port of Marc Ibrahim's decoder](https://github.com/NerRobDog/x87sidecar/commit/4b6bad8).
Decoder composition and the FBLD fix are MIT-licensed [MacGames patches](https://github.com/tarikbc/macgames/tree/1579841b15ce569807b92af95b478c752c26df3d/patches/x87sidecar).
Original source and license notices are retained.

After building the tests, run `python3 scripts/test_aoe_softfault.py /path/to/build`
to check software-fault delivery and its composition with the generic decoder.
