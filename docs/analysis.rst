.. _analysis:

Analysis note
**************

Goals and algorithms overview
-----------------------------

The goal of the analysis is to find out the full set of alignment constants of the whole system that is composed of the
following elements: L1, L2, L3, Filter and Detector plane.
Each of these has a position :math:`(x, y , z)` and rotations as Euler angles
:math:`(\theta, \phi, \psi)`.
One should also consider the beam position and rotation angles but I'll leave that out for now.

The number of parameters to constrain is hence :math:`6\times6 = 36`, that is quite large!

The mechanical uncertainties on each of these parameters varies quite a bit from one element to the other.
For instance, the Filter that is a moving part will clearly have larger uncertainties than the L1/L2 assembly.
Another example is the Detector plane that is by designed plane to a few microns level, so :math:`z_{det}` is very constrained.
Work is needed to get a correct estimate of these uncertainties.

The beam will generate one main image, and 36 secondary images that will have gone through 2 reflections, and hence will
be of the order of :math:`10^{-4}` dimmer than the main image. For the secondary images to be above the detector
threshold, the beam power needs to be strong enough, and the main image will likely be always highly saturated.

The position of the beam spots are correlated to the initial beam position and orientation and to the position and
orientation of each of the component of the optical system. By taking images at different beam positions and orientations,
one can determine with high precision the full alignment of the system.

Note that the ghosts images dimension and intensity do also depend upon the alignment and transmission of each of the
optical elements. Ghosts images diameter is probably helpful to identify a beam spot with a given ghost.

Two procedures that can be developed to go from the images of ghosts to alignment constants:

- Analyze beam spots positions, diameter and intensity
- Full image analysis

These two procedures are detailed below.

Beam spots
----------
Each beam data taking will produce 1 (saturated) main image and 36 (dim) secondary images.
Each of this secondary beam spot has a position, diameter and intensity.

The idea is to minimize the `distance` between beam spots from real data (potentially fake)
and beam spots from (similar) simulated data, for different beam configurations.


image analysis
==============
In the simulations provided by this package, each beam spot is well identified to a given ghost via the known light path.
Each ghost has an id as an integer and a name as a pair of optical component names, the two optical components on which
happened the two reflections: `33 = (Detector, Filter_entrance)`.

In real data, we'll only have a full or partial focal plane image, hopefully calibrated and reduced, with some kind of
background subtracted signal in each pixel. Some algorithm needs to be designed to get from this full image to a list of
beam spots characterized with position, diameter and intensity. That I'll do later.

It remains to be understood if we want to push the simulation to be real data like up to the point where we'll be able
to run the beam spots search on simulated image. I do not see any obvious advantage to that now.

parameters
==========
For each beam configuration (simulated or data taking), the image analysis produces a list of beam spots.

.. list-table:: Beam spots table
   :widths: 25 50 25 25 25 25
   :header-rows: 1

   * - id
     - name
     - pos_x
     - pos_y
     - radius
     - intensity
   * - 0
     - (L1_exit, L1_entrance)
     - 0.1
     - 0.2
     - 0.002
     - :math:`10^{-4}`
   * - 1
     - (L2_exit, L1_entrance)
     - -0.15
     - 0.25
     - 0.0025
     - :math:`10^{-4}`
   * - ...
     - ...
     - ...
     - ...
     - ...
     - ...
   * - 36
     - (Detector, L3_exit)
     - 0.5
     - 0.1
     - 0.005
     - :math:`0.2\times10^{-4}`

A couple of notes:

- the beam spots id and names will have a real meaning only for the simulations.
- the number of beam spots will depend upon the image analysis and will not always be 37 or 36.


distance / likelihood
=====================
For each beam configuration, we have data taking on one side, that is reduced to a list of characterized beam spot.
On the other side, we produce simulations with the same beam configuration and different possible alignment constants.

The `distance` between to sets of beam spots can be defined in different ways, here is the simplest one that is just the Euclidean one on the focal plane, ignoring the spot sizes and intensities:

- let's consider 2 sets of beam spots: :math:`S_r, S_s`, composed of :math:`n, m` ghosts spots as :math:`[g_{r,1}, g_{r,2}, ..., g_{r,n}]` and :math:`[g_{s,1}, g_{s,2}, ..., g_{s,m}]`
- ghost spot :math:`g_{r,i}` has parameters :math:`[x_{r, i}, y_{r, i}, d_{r, i}, p_{r, i}]` for position in x and y, radius and intensity.
- the Euclidean distance between 2 ghosts spots is defined as:
    .. math::
        d(g_{r,j}, g_{s,i}) = \sqrt{(x_{s, i} - x_{r, j})^2 + (y_{s, j} - y_{r, j})^2}
- with the distances spot to spot between the 2 lists :math:`(g_{r,j 1..m}, g_{s,i 1..n})`, one can them associate each spot in the :math:`S_s` set with the closest spot in the :math:`S_r` set.
- we note :math:`g_{r,k_i}` the closest ghost spot in :math:`S_r` to the ghost spot :math:`g_{s,i}` in :math:`S_s`.
- the reduced distance between 2 sets of ghosts spots may then be defined as follow:
    .. math::
        L = \frac{\sqrt{\sum_{i=1}^{n} d(g_{s,i}, g_{r,k_i})^2}}{n}
- if 2 sets of beam spots are the same :math:`L=0`, and if they are really close then :math:`L` should be small.


A couple of additional notes:

- uncertainties, statistical and systematic errors should be taken into account.
- the distance probably should probably take into account the spot radius as well, it should improve the spot to spot matching.
- the distance could potentially also take the intensity of the spot into account, but AB said uncertainties were really large (coating).


method
======
In principle, minimizing the distance :math:`L` should lead to finding the alignment constant that best match the data analyzed.
Each simulation with a given beam configuration and telescope geometry produces a list of beam spots for which we can compute the distance :math:`L` to the reference data.

The point is how to run this minimization process:  usual minizer, MCMC, other?

Without any optimization, each simulation takes a bunch of seconds to run:

- is that too much time?
- is there no hope, even with 100 times faster simulations?
- is the phase space too large, and should be break into pieces, fitting the simples spots first?
- shall I run many simulations in advance to have a bank to take these from instead of running these on the fly?


Full Images
-----------
An alternative method to run this analysis would be to work directly with full images.
Indeed, assuming that we can produce simulations that are closed enough to real data, the `distance` between simulated and real data could be just the quadratic difference pixel per pixel.

image analysis
==============
The image analysis is somewhat simpler as all is needed is:

- cleaned images from the data taking, i.e. flat and noiseless. It's to be understood if we want just signal or signal to noise ration, or something else.
- very realistic simulations and simulated images, treated in the same way as real images.
    + It probably requires to implement some electronic response and a real focal plane with rafts and amps.

In order to subtract images pixel by pixel properly, they also have to be aligned in some way with respect to some reference point on the focal plane.


parameters
==========
The number of parameters is basically the number of pixels, the one with no signal counting almost as the one with beam signal.

Images might be down sample from the original number of pixel to some more manageable number for fast computations and reduced data size.

distance / likelihood
=====================
The `distance` between 2 images is just defined as the reduced quadratic difference.

For an image with :math:`n` pixel, i'ts just:
    .. math::
        L = \frac{\sqrt{\sum_{i=1}^{n} (S_i_s - S_i_r)^2}}{n}
where :math:`S_i_s` is the signal in the :math:`i^{th}` pixel of the simulated image,
and  :math:`S_i_r` is the signal in the :math:`i^{th}` pixel of the real data image.

And one should divide the signal by some error.

method
======
Minimizing :math:`L` should lead to find the correct parameters.

The main issue here is to have simulations that match data really well:
    - the real data image must be really clean
    - the simulation model must be much more advanced

Some intermediate procedure could be to find spots in real data and make a real data "model" that would be easier to match with the simulated images.

