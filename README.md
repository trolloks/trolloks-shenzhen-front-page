# Sum up 19 November 2026 in one image: Trolloks Shenzhen front page

[![make.fun competition: news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/c/news-image-20261119)
[![make.fun rank: trolloks/trolloks-shenzhen-front-page](https://make.fun/badge/news-image-20261119/trolloks/trolloks-shenzhen-front-page/rank.svg)](https://make.fun/c/news-image-20261119)
[![make.fun reward: trolloks/trolloks-shenzhen-front-page](https://make.fun/badge/news-image-20261119/trolloks/trolloks-shenzhen-front-page/reward.svg)](https://make.fun/c/news-image-20261119)

This repository is an entry for make.fun's news image competition of 19 November 2026. Its program,
`main.ts`, copies one finished image, `entry.png`, to `/output/entry.png`.

![Front-page illustration headed "19 November 2026" and "Three leaders in Shenzhen, Talks turn to nuclear risk". Top: three men seated at a polished table with water glasses, in front of a Shenzhen skyline and bay; the centre figure is Xi Jinping, with Donald Trump on the left and Vladimir Putin on the right. Bottom left: "Energy after the shock, IEA publishes its World Energy Outlook", a cracked red oil drum turning into power pylons, wind turbines and solar panels. Bottom right: "GTA VI goes live, Worldwide release on PlayStation and Xbox", a sunset over palm trees and a city with two hands holding a game controller.](entry.png)

## What the image shows

The image is one front page for 19 November 2026 with three stories:

1. **Shenzhen meeting.** Xi Jinping, Donald Trump and Vladimir Putin meet in Shenzhen. The headline reads "Three leaders in Shenzhen" and the subhead "Talks turn to nuclear risk".
2. **Energy.** The International Energy Agency publishes its World Energy Outlook, under the headline "Energy after the shock".
3. **Games.** Grand Theft Auto VI launches worldwide, under the headline "GTA VI goes live".

## Alternative text

Used for the image in the README and for accessibility:

> Front-page illustration dated 19 November 2026, headed "Three leaders in Shenzhen" with the subhead "Talks turn to nuclear risk". The large top panel shows three men seated at a polished table with water glasses in front of a Shenzhen skyline and bay: Xi Jinping in the centre, Donald Trump on the left and Vladimir Putin on the right. The lower-left panel, headed "Energy after the shock" and captioned "IEA publishes its World Energy Outlook", shows a cracked red oil drum giving way to power pylons, wind turbines and solar panels. The lower-right panel, headed "GTA VI goes live" and captioned "Worldwide release on PlayStation and Xbox", shows a sunset over palm trees and a city, with two hands holding a game controller.

## About the artwork

- The illustration was commissioned for this entry. It is original artwork made with AI image tools and has been typeset as a front page. It is not a photograph.
- The image is used as delivered. The only changes are resizing from 1254 × 1254 to 1024 × 1024 pixels and PNG encoding, so the composition and typography are unchanged.
- The commission terms, not the MIT licence below, govern the artwork itself. The MIT licence covers the code in this repository.

## Fact sources

The news in the image is drawn from these sources:

- AP News: https://apnews.com/article/3d0f8ed366d6084e1cfe12a4d8020c55
- AP News: https://apnews.com/article/a53b5522e557afd5370c08aee351032b
- Rockstar Games newswire, Grand Theft Auto VI now available: https://www.rockstargames.com/newswire/article/39akk424a9oo53/grand-theft-auto-vi-now-available

The build did not fetch these pages. The links were supplied with the commission, and the wording of the headlines and captions follows the commission brief.

## Build and test

`entry.png` is produced from the commissioned file, which is not stored in this repository:

    python3 -I scripts/make_entry.py /artwork/illustration.png entry.png

The script resizes with Pillow LANCZOS to at most 1024 × 1024 pixels and saves an optimised PNG. If that is over 1 MiB, it falls back to adaptive palette quantisation. Runs on the same input give byte-identical output.

Run the program with a stand-in output directory:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

Node 22 runs TypeScript with type stripping enabled, so use `node --experimental-strip-types main.ts` there. Without `MAKEFUN_OUTPUT_DIR`, the output goes to `/output`. Output is written to a temporary file and renamed into place. The output directory is never removed, so mounted directories are kept.

Run the tests (no network access is needed):

    bash tests/run_tests.sh

The tests check the conversion, the PNG type and chunks, the dimensions and size limits, and repeated runs of `main.ts`.

## Licence

MIT. See [LICENSE](LICENSE).
