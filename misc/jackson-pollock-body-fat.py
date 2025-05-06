"""Jackson-Pollock 3-Site Body Fat Formula

Resources:

1.  A reddit-compiled set of pictures of people with known body fat percentages:
    https://imgur.com/T2wgsW5
2.  Body fat percent norms (American Council on Exercise):
    https://www.acefitness.org/resources/everyone/tools-calculators/percent-body-fat-calculator/

Description     Women   Men
Essential Fat   10-13%  2-5%
Athletes        14-20%  6-13%
Fitness         21-24%  14-17%
Acceptable      25-31%  18-24%
Obesity         >32%    >25%
"""

from statistics import mean

age = 33
pectoral_samples = [16, 17, 16]
abdominal_samples = [28, 26, 27]
thigh_samples = [13, 17, 13]
sum_of_skinfolds = (
    mean(pectoral_samples) + mean(abdominal_samples) + mean(thigh_samples)
)

body_density = (
    1.10938
    - 0.0008267 * sum_of_skinfolds
    + 0.0000016 * sum_of_skinfolds**2
    - 0.0002574 * age
)
body_fat = 495 / body_density - 450
print(f"Estimated body fat: {body_fat:.2f}%")
