# rle-decoder

CLI App to decode binary RLE Segments


## Installation
```bash
git clone https://github.com/efraintorlo/rle-decoder
cd rle-decoder
make install PYTHON=python3.12 # or any other python3 version >= 3.8
```

The `make install` will install the `rle-decoder` cli inside the `venv` environment, you can also install it in your system by running `make install-system`.

After installation you should need to activate the virtual environment by running `source venv/bin/activate`.

## Usage

Read `help` menu
## Help
```bash
rle-decoder --help
```

Help menu for subcommands
```bash
rle-decoder decode --help
rle-decoder metrics --help
```

Get the `contours`

```bash
rle-decoder decode --counts 600 500 --size="_lm26^b09I4L4M2M3N2O1N2N2O1N101N101O0O100000O1O100N2K6L3M3N2N2O2N1O3L5L3N2M`bb5"
```

Use the `metrics` subcommand to get the metrics of the decoded segment, supported metrics are: `area,perimeter,compactness,bbox,centroid,contours`

```bash
rle-decoder metrics --counts 600 500 --size="_lm26^b09I4L4M2M3N2O1N2N2O1N101N101O0O100000O1O100N2K6L3M3N2N2O2N1O3L5L3N2M`bb5" --metric area,perimeter,compactness,bbox,centroid,contours
```

Send the output to a file
```bash
rle-decoder metrics --counts 600 500 --size="_lm26^b09I4L4M2M3N2O1N2N2O1N101N101O0O100000O1O100N2K6L3M3N2N2O2N1O3L5L3N2M`bb5" --metric area,perimeter,compactness,bbox,centroid,contours --output metrics.json
```

```bash
rl-decoder decode --counts 600 500 --size="_lm26^b09I4L4M2M3N2O1N2N2O1N101N101O0O100000O1O100N2K6L3M3N2N2O2N1O3L5L3N2M`bb5" --metric area,perimeter,compactness,bbox,centroid,contours --output my_contours.csv
```

## Uninstall
```bash
make uninstall
```

## License