# CU Course Timetable API
<p align="center">
  <p align="center">Chulalongkorn university course API from web scrapping.</p>
  <p align="center">
    <a href="/LICENSE.md"><img alt="Software License" src="https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square"></a>
    <a href="https://github.com/y-pakorn/cutimetable-api/issues"><img alt="Actions" src="https://img.shields.io/github/issues/y-pakorn/cutimetable-api"></a>
    <a href="https://github.com/y-pakorn/cutimetable-api/pulls"><img alt="Doc" src="https://img.shields.io/github/issues-pr/y-pakorn/cutimetable-api"></a>
    <img alt="Gitter" src="https://img.shields.io/github/stars/y-pakorn/cutimetable-api?style=social">
  </p>
</p>

## About the project

Since Chula doesn't have the API for student developer to directly use, I managed to create course API for whoever want to use!

Built using flask for web API framework, request and bs4 for web scraping.

Used in [CU Course Timetable](https://apps.apple.com/ag/app/chula-class-timetable/id1527905632) application! (iOS Only)

## Documentation

It's on [SwaggerHub](https://app.swaggerhub.com/apis-docs/y-pakorn/cutimetable-api/1.0.0)!

## Getting Started

### Prerequisites
- Python 3.8
- pip

### Installation

1. Clone the repo
```
git clone https://github.com/y-pakorn/cutimetable-api.git
```
2. Install dependencies
```
cd cutimetable-api
```
```
pip install -r requirements.txt
```

### Usage

Simply ```python3 run.py``` and the app will be served at https://localhost:5000/cutimetable/v1/ (Refer to docs for API path)

## Contributing

Any contributions you make are **greatly appreciated**.

Please open an issue or open a pull request!

## License

MIT


