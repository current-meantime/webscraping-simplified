# Web Scraping Simplified
## Introduction

This repository provides a straightforward introduction to web scraping, designed for those new to the topic. The materials here - `webscraping_simplified.md` and `webscraping_simplified.py` - offer a concise, practical guide without overwhelming detail.

## Aim

The goal is to explain web scraping basics in a clear, accessible way. This guide covers:

- **Manipulating URL query parameters** to access specific data.
- **Automating the scraping process** using Python.
- An introduction to two widely used Python libraries for web scraping: **requests** and **BeautifulSoup**.
- A **general workflow** for scraping, demonstrated with a real website as an example.


## Example Source
I have recently scraped texts from the [American Presidency Project Website](https://www.presidency.ucsb.edu/) for another project of mine, and it is used here as an example. This site is ideal for beginners because:
- It does not require handling user agents or cookies to access content.
- There are no complex anti-scraping measures or hidden API calls.
- The structure is simple, allowing you to focus on the fundamentals of web scraping without extra complications.

Many modern websites employ techniques that make scraping more challenging (such as blocking requests, requiring authentication, or hiding data behind APIs). The American Presidency Project does not, so you can practice basic scraping techniques here without needing to address those advanced topics.

## Scope and Constraints

This guide intentionally does **not** cover:

- Cookies or user agent management.
- Handling JSON files or APIs.
- Advanced anti-scraping countermeasures, etc.
- Libraries such as `selenium` or `playwright`.

The focus is on simplicity.

The code in the script may require additional explanations despite the comments that are already there.

## Prerequisites
As a learner: basic knowledge of Python - familiarity with things such as imports, functions, for loops, etc.

If you plan to teach or demonstrate the mentioned concepts, consider using live examples in your browser and IDE to be more effective. The screenshots I have included are helpful, but hands-on exploration is even better. This guide is just a starting point and does not exhaust the topic.