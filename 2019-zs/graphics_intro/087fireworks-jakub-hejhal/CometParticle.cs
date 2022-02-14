using MathSupport;
using OpenglSupport;
using OpenTK;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _087fireworks
{
  
  public class CometParticle : Particle
  {

    public double variance;
    public double extinctionRate;
    public double extinction = 1;
    public double colorVariance { get; set; } = 0.15;

    public double frequency;
    static RandomJames rnd = new RandomJames();

    public CometParticle (Vector3d pos, Vector3d vel, Vector3d _up, Vector3 col, double size, double time, double freq, double variance, double extinctionRate = 0.9)
    {
      this.extinctionRate = extinctionRate;
      position = pos;
      velocity = vel;
      up = _up;
      color = col;
      this.size = size;
      simTime = time;
      frequency = freq;
      this.variance = variance;
    }

    static Vector3 clip(Vector3 vector, double min, double max)
    {
      var v = new Vector3(vector.X, vector.Y, vector.Z);
      v.X = (float)Arith.Clamp(v.X, min, max);
      v.Y = (float)Arith.Clamp(v.Y, min, max);
      v.Z = (float)Arith.Clamp(v.Z, min, max);
      return v;
    }

    public override bool Simulate (double time, Fireworks fw)
    {
      if (time <= simTime)
        return true;

      if (extinction < 0.2)
      {
        return false;
      }

      // fly the particle:
      double dt = time - simTime;
      double extinctionDiff = Math.Pow(extinctionRate, dt);
      extinction = extinction * extinctionDiff;

      Physics.Update(position, velocity, size,  dt, out var newPosition, out var newVelocity);
      position = newPosition;
      velocity = newVelocity;

      size *= extinctionDiff;
      color *= (float)extinctionDiff;

      double probability = dt * frequency;
      while (probability > 1.0 ||
             rnd.UniformNumber() < probability)
      {
        
        // sample emmited particle color
        Vector3 pColor = clip(Geometry.RandomDirectionNormal(rnd, color, colorVariance), 0, 1);

        // emitted particles should be of smaller size than the CometParticle, so that they are slowed down more by air resistance
        double pSize = rnd.RandomDouble(0.2, 1);
        double extRate = 0.5;


        Vector3d emmitedParticleVelocity = Geometry.RandomDirectionNormal(rnd, velocity, variance) * velocity.Length;         
        BasicParticle p = new BasicParticle(position, emmitedParticleVelocity, up,
                                  pColor,
                                  pSize, time, extRate);
        fw.AddParticle(p);
        probability -= 1.0;
      }


      simTime = time;

      return true;
    }
  }
 }
