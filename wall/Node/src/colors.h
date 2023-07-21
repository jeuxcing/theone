
#ifndef COLORS_H
#define COLORS_H

const int intensity = 30;
const int default_colors[][3] = {
    {0, 0, 0},
    {intensity, 0, 0}, {0, intensity, 0}, {0, 0, intensity},
    {intensity, intensity, 0}, {intensity, 0, intensity}, {0, intensity, intensity},
    {intensity, intensity, intensity}
};
int num_default_colors = sizeof(default_colors) / (3 * sizeof(int));

#endif