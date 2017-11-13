# Personify
Markov Chain based text generator. Reads a Twitter user's tweets and produces similar tweets.

## Branches
### Prod
The prod branch is for the code which will run on the server, posting every hour to Twitter.

### Master
The master branch is for the current up-to-date code. It's separate from prod because things like absolute file paths
inevitably make it through and must be weeded out before pushing to prod.

-------------------------

## Roadmap
- Implement burn-from-both-sides algorithm for sentence generation
- Add support for YML/JSON config files
- More graphing
- Tidy the pre-processor even more
- Tests...
- More tests...

------------------------

## Bots
There is a bot currently running on Twitter
- [@DonaldoNumber9](https://twitter.com/DonaldoNumber9)
