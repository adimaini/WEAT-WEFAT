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

# ND- Cass County
twarc2 search \
--archive \
--start-time "2020-10-01" \
--end-time "2021-03-31" \
--limit 500000 \
--flatten \
"bounding_box:[-97.164261 46.688553 -96.640385 46.974124] -is:reply -is:retweet lang:"en" place_country:US" \
> ND_CAS_tweets_10-2020_03-2021_c1.jsonl

# ND- Burleigh County
twarc2 search \
--archive \
--start-time "2020-10-01" \
--end-time "2021-03-31" \
--limit 500000 \
--flatten \
"bounding_box:[-100.921654 46.621676 -100.421477 46.923955] -is:reply -is:retweet lang:"en" place_country:US" \
> ND_BUR_tweets_10-2020_03-2021_c1.jsonl

# ND- Grand Forks County
twarc2 search \
--archive \
--start-time "2020-10-01" \
--end-time "2021-03-31" \
--limit 500000 \
--flatten \
"bounding_box:[-97.433293 47.776940 -96.976284 48.073388] -is:reply -is:retweet lang:"en" place_country:US" \
> ND_GRA_tweets_10-2020_03-2021_c1.jsonl

# SD- Minnehaha County
twarc2 search \
--archive \
--start-time "2020-10-01" \
--end-time "2021-03-31" \
--limit 500000 \
--flatten \
"bounding_box:[-96.967452 43.433960 -96.564094 43.705332] -is:reply -is:retweet lang:"en" place_country:US" \
> SD_MIN_tweets_10-2020_03-2021_c1.jsonl

# SD- Pennington County
twarc2 search \
--archive \
--start-time "2020-10-01" \
--end-time "2021-03-31" \
--limit 500000 \
--flatten \
"bounding_box:[-103.525412 43.834956 -103.047240 44.181360] -is:reply -is:retweet lang:"en" place_country:US" \
> SD_PEN_tweets_10-2020_03-2021_c1.jsonl

# SD- Lincoln County
twarc2 search \
--archive \
--start-time "2020-10-01" \
--end-time "2021-03-31" \
--limit 500000 \
--flatten \
"bounding_box:[-96.914541 43.350976 -96.536781 43.646837] -is:reply -is:retweet lang:"en" place_country:US" \
> SD_LIN_tweets_10-2020_03-2021_c1.jsonl

# OR- Multnomah County
twarc2 search \
--archive \
--start-time "2020-10-01" \
--end-time "2021-03-31" \
--limit 500000 \
--flatten \
"bounding_box:[-122.900033 45.423187 -122.455136 45.776293] -is:reply -is:retweet lang:"en" place_country:US" \
> OR_MUL_tweets_10-2020_03-2021_c1.jsonl









