# Tiny Chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/xiaojiaxiaoce/tiny-chess-01-4kb/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) [![reward](https://make.fun/badge/tiny-chess-01/xiaojiaxiaoce/tiny-chess-01-4kb/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A deterministic Python chess engine for the Tiny Chess gauntlet.

## Engine

`main.py` is the complete engine and uses only Python's standard library. It reads the game state from `MAKEFUN_ENV_URL`, sends moves through the `/game` and `/move` JSON endpoints, and chooses only from the legal UCI moves supplied by the environment. Its fixed four-ply negamax alpha-beta search uses capture/promotion ordering and a material-plus-position evaluation. It does not use randomness, wall-clock search, external packages, or model calls.

## Local checks

A locally authored perft regression test matched known depth-three counts on five standard chess positions. The start-position move choice was legal and identical across repeated calls. These checks do not invoke the competition kit or its evaluator.

## License

MIT; see `LICENSE`.
