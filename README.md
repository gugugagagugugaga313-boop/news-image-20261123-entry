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
  with no agreement; the final draft leaves out fossil fuels, the
  first climate summit to collapse since 2009.
- **Huang returns to Nvidia** — Nvidia reinstates Jensen Huang as
  chief executive, 11 days after he quit; shares jump 31 percent.
- **Factory fire search resumes** — in Cikande, Java, Indonesia;
  officials confirm 24 killed and about 30 still missing.
- **Ukraine sinks a Russian warship** — Ukrainian sea drones sank
  the Russian corvette Merkury in Benghazi, Libya, and hit a cargo
  ship carrying weapons.
- **India gives Nepal 1.62 billion** — Nepal PM Balendra Shah holds
  talks with PM Modi in New Delhi. India announces a 1.62 billion
  dollar package and 8 deals.
- Also today: 11 dead and 2 missing after a Russian drone hits a
  building in the Kyiv region, and a Delta tech failure delays
  1,300 flights before Thanksgiving.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
