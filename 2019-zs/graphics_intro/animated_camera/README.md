Code for smooth control and interpolation of camera position and orientation given a sequence of key-frames.

Position is interpolated using Catmull-Rom splines. Orientation of camera is either automatic (derived from trajectory), or manual. 

In manual mode, sequence of key-frame rotations are given. Each rotation is represented by quaternions. which can be quadratically interpolated by SQUAD (Spherical Spline Quaternion interpolation). 
Spherical linear interpolation (SLERP) feels very jerky and snatchy, which makes it unsuitable for smooth camera controll. 

On the other hand, squad interpolation gives us continuous angular velocity, which is in agreement with physical laws (conservation of momentum) and feels more natural.
