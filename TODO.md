# TODO

## Skeleton

- [ ] Make one branch for Tkinter projects, one branch for PyGTK projects, one branch for PyQT projects, ...
- [ ] Add docs/
- [ ] Add tests/
- [ ] Add common tools: travis, ...

## Version 0.1

- [ ] Rename this project "SAp CTA Data Pipeline"
- [ ] Simtel should be a class to load files only once
- [ ] Add the following command: "dp-simtel-ls-telescopes [telid]" (dp-simtel-count is based on this function)
- [ ] Add the following command: "dp-simtel-ls-events [evid]"
- [ ] Update the following command: "dp-simtel-show" (options to save images, set min/max, ...)
- [ ] Add the following command: "dp-simtel-show-pe [telid, evid, layer]"
- [ ] Add the following command: "dp-simtel-show-histogram"
- [ ] Add the following command: "dp-simtel-show-pe-histogram"
- [ ] Manage simtel files: list content, extract, ...
- [ ] Manage images: get histogram, display histogram, ...
- [ ] Add a setup.py file to get commands: dp-simtel-ls, dp-simtel-extract, dp-denoise-tailcut, dp-denoise-fft, dp-denoise-wavelets, ...
- [ ] Add a README.md with usage examples
- [ ] Avoid redundancies with FitsViewer in io.images (FITS/PNG conversion, ...)
