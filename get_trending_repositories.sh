#!/usr/bin/env zsh

DATE_CMD="gdate"
PAST_MONTH=$($DATE_CMD -d "-1 month" +%Y-%m-%d)

curl -G https://api.github.com/search/repositories \
  --data-urlencode "sort=stars"             \
  --data-urlencode "order=desc"             \
  --data-urlencode "q=created:>$PAST_MONTH" \
  --data-urlencode "q=language:cpp"
