# news-image-20261123 — The World's News in One Image

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/gugugagagugugaga313-boop/news-image-20261123-entry/rank.svg)](https://make.fun/c/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/gugugagagugugaga313-boop/news-image-20261123-entry/reward.svg)](https://make.fun/c/news-image-20261123)

Entry for the [make.fun](https://make.fun) competition
[news-image-20261123](https://make.fun/c/news-image-20261123):
sum up the world's news of Monday 23 November 2026 in one image.

## What it is

`main.py` (Python 3, standard library only) draws a 1024x1024
newspaper-style image with a small 5x7 bitmap font and a hand-written
PNG encoder — no network, no external files, no randomness. Running
it twice writes identical bytes to `/output/entry.png`.

## The day, in the image

- **COP31 collapses with no deal** — talks in Antalya, Turkiye end
  with no agreement; the final draft leaves out fossil fuels.
- **Drone hits the Kyiv region** — a Russian drone hits a building;
  at least 14 people are missing, President Zelenskiy says.
- **Factory fire search resumes** — in Cikande, Java, Indonesia;
  police remove 24 body bags and dozens of workers are missing.
- **Cartel boss captured** — Mexico captures FBI most-wanted
  cartel boss El Chapo Isidro; firefights in Sinaloa leave
  11 people dead.
- **Nepal PM meets Modi** — Nepal PM Balendra Shah holds bilateral
  talks with PM Modi in New Delhi.
- Also today: South Korea's education minister quits over an AI
  exam-cheating scandal, and India post a record 720/9d in the
  Wellington Test against New Zealand.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
