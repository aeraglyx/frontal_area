# Frontal Area Finder

Tool for calculating frontal area of a human body from images and finding how it relates to mass.

Under the hood, it uses [rembg](https://github.com/danielgatis/rembg) to generate mattes, their alpha gets summed and converted to area. Then, we can perform curve fitting to get the coefficients of a power law like this:

$$ A = a \cdot m ^ b $$

If we assume human bodies scale proportionally, then $b = \frac{2}{3}$. If we relate $m$ and $h$ using the BMI formula, we would get $b = \frac{3}{4}$. My data (4 lower BMI subjects, multiple photos each) suggests these coefficients (for a board sport stance):

$$a = 0.016 ± 0.010$$

$$b = 0.802 ± 0.149$$

If we assume the true $b$ is indeed $\frac{3}{4}$, then $a$ would be roughly $0.02$.

## Requirements

- python
- rembg, cv2, numpy, pandas, scipy, matplotlib

## Usage

The `input` directory should contain subdirectories for different subjects/measurements, each containing at least one photo of the person.

> TIP - Shoot from far away with bigger zoom to approximate orthographic projection.

You should also have one photo from the same distance where the person holds a 1 meter stick perpendicular to the camera. Measure it in pixels (e.g. in [Gimp](https://www.gimp.org/)) and record it along with the persons mass to `data_in.csv`:

| Field | Description |
| ----- | ----------- |
| name | Subdirectory name of input photos |
| mass | Subjects mass in kilograms |
| height | For testing purposes, use a dummy value |
| calib | 1 meter represented in pixels |

For privacy reasons, I left the `input` directory empty.

`matte` is where the generated matte images are stored. There you can inspect the quality of background removal. Only new, unprocessed inputs are turned into mattes, to regenerate certain images using a different model, first delete them from the `matte` folder. Some mattes are already included for reference.

By default, this project used the *birefnet-general* model for matte generation, since it seems to work really well even with busy backgrounds. If you shoot your photos with clean background and soft lighting, you can get away with more light weight models like *u2net* or *silueta*.

Run `generate_data.py` to regenerate mattes and areas. Finally, run `main.py` to analyze the new data.

## Discussion

[This article](https://link.springer.com/article/10.1007/s004210100424) mentioned a 0.762 exponent, which makes sense. But then they write about how the drag coefficient might be proportional to m raised to the –0.45 power, sort of negating the effect of frontal area and taking down the combined exponent for drag area ($C_d \cdot A$) to a 0.312 power. (however, they are writing about cycling)

I find this confusing, as it's usually taught that the frontal area and drag coefficient are independent, so I don't know what to think. Unfortunately, I don't have access to the full article.

## Random Related Stuff

- https://en.wikipedia.org/wiki/Drag_(physics)
- https://en.wikipedia.org/wiki/Body_mass_index
- https://en.wikipedia.org/wiki/Allometry