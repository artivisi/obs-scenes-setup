# Scene Collections

This directory contains pre-built OBS scene collections that can be imported directly into OBS Studio.

## Available Collections

Scene collections are generated from the templates and resources in this repository and published via GitHub Pages for easy access.

## Usage

1. Download the desired `.json` file
2. In OBS Studio: Scene Collection → Import → Select the downloaded file
3. Configure your camera and screen sources as needed

## Custom Collections

To generate your own scene collection, use the main workflow:

```bash
python scripts/generate-scenes.py --resource resources/event.yaml --output my-workshop/
python scripts/serve-scenes.py my-workshop/
python scripts/inject-obs.py --collection my-workshop --webserver http://localhost:8080
```