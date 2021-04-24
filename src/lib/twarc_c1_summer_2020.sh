#!/bin/sh
#SBATCH --time 100:00:00
#SBATCH -o testing%j.out
#SBATCH -e testing%j.err
#SBATCH -p large-gpu -N 1
#SBATCH --mail-user=adimaini@gwu.edu 
#SBATCH --mail-type=ALL

module load python3/3.7.2
source "/lustre/groups/caliskangrp/adimaini/twitter-corpus/twitter-env/bin/activate"
cd /lustre/groups/caliskangrp/adimaini/twitter-corpus

# LA - East Baton Rouge
twarc2 search \
--archive \
--start-time "2020-07-01" \
--end-time "2020-09-30" \
--limit 500000 \
--flatten \
"bounding_box:[-91.284416 30.332508 -90.848349 30.726238] -is:reply -is:retweet lang:"en" place_country:US" \
> LA_EBR_tweets_07-2020_09-2020_c1.jsonl

# LA - Jefferson
twarc2 search \
--archive \
--start-time "2020-07-01" \
--end-time "2020-09-30" \
--limit 500000 \
--flatten \
"bounding_box:[-90.277611 29.662277 -90.032534 30.040002] -is:reply -is:retweet lang:"en" place_country:US" \
> LA_JEF_tweets_07-2020_09-2020_c1.jsonl

# HI - Hawaii
twarc2 search \
--archive \
--start-time "2020-07-01" \
--end-time "2020-09-30" \
--limit 500000 \
--flatten \
"bounding_box:[-155.404230 19.474646 -155.095811 19.755616] -is:reply -is:retweet lang:"en" place_country:US" \
> HI_HAW_tweets_07-2020_09-2020_c1.jsonl

# HI - Kauai
twarc2 search \
--archive \
--start-time "2020-07-01" \
--end-time "2020-09-30" \
--limit 500000 \
--flatten \
"bounding_box:[-159.612855 21.916744 -159.322923 22.228947] -is:reply -is:retweet lang:"en" place_country:US" \
> HI_KAU_tweets_07-2020_09-2020_c1.jsonl

# VT - Chittenden
twarc2 search \
--archive \
--start-time "2020-07-01" \
--end-time "2020-09-30" \
--limit 500000 \
--flatten \
"bounding_box:[-73.274369 44.349467 -72.821253 44.631342] -is:reply -is:retweet lang:"en" place_country:US" \
> VT_CHI_tweets_07-2020_09-2020_c1.jsonl

# VT - Rutland
twarc2 search \
--archive \
--start-time "2020-07-01" \
--end-time "2020-09-30" \
--limit 500000 \
--flatten \
"bounding_box:[-73.101825 43.461015 -72.817746 43.741994] -is:reply -is:retweet lang:"en" place_country:US" \
> VT_RUT_tweets_07-2020_09-2020_c1.jsonl

# VT - Washington
twarc2 search \
--archive \
--start-time "2020-07-01" \
--end-time "2020-09-30" \
--limit 500000 \
--flatten \
"bounding_box:[-72.720511 44.096394 -72.393903 44.336403] -is:reply -is:retweet lang:"en" place_country:US" \
> VT_WAS_tweets_07-2020_09-2020_c1.jsonl

# ME - Cumberland
twarc2 search \
--archive \
--start-time "2020-07-01" \
--end-time "2020-09-30" \
--limit 500000 \
--flatten \
"bounding_box:[-70.681413 43.599176 -70.193221 43.913792] -is:reply -is:retweet lang:"en" place_country:US" \
> ME_CUM_tweets_07-2020_09-2020_c1.jsonl

# ME - York
twarc2 search \
--archive \
--start-time "2020-07-01" \
--end-time "2020-09-30" \
--limit 500000 \
--flatten \
"bounding_box:[-70.838873 43.344209 -70.362393 43.627955] -is:reply -is:retweet lang:"en" place_country:US" \
> ME_YOR_tweets_07-2020_09-2020_c1.jsonl

# ME - Penobscot
twarc2 search \
--archive \
--start-time "2020-07-01" \
--end-time "2020-09-30" \
--limit 500000 \
--flatten \
"bounding_box:[-68.983410 44.729124 -68.506447 45.089437] -is:reply -is:retweet lang:"en" place_country:US" \
> ME_PEN_tweets_07-2020_09-2020_c1.jsonl


