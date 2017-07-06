[![Build Status](https://travis-ci.org/jladdjr/mobius.svg?branch=master)](https://travis-ci.org/jladdjr/mobius)

# Mobius

A micro search engine.

## Why build a micro search engine?

I chose to build a simple search engine because the challenge
scales well and because it provides an opportunity to explore a number of
fields / technologies.

### A project that scales well

Search engines can be naive or they can obviously be enormously complex. 
A naive implementation could be based on parsing keywords provided 
in the metadata of a webpage to determine what the page is about. 
A more sophisticated implementation would take into account a given
page's place in a network of linked sites.

This range - from simple to complex implementation - gives me a chance
to quickly develop a working prototype, but then continue to develop
a more sophisticated application as my own skills develop.

### Exploring a range of technologies

Building a search engine gives an opportunity to:

* Build a full stack web application
* Explore natural language processing
* Explore network theory, and
* Wrestle with interesting challenges inherent to the project - 
  how to build an efficient web crawler and an efficent search
  based on the metadata retrieved; how to return relevant search
  results; how to build an intuitive interface (both UI
  and API) for searching.

## Requirements

None

## Tests

To run tests, use:

py.test mobius/tests

## Contributors

Project authors include:

* James Ladd Jr
