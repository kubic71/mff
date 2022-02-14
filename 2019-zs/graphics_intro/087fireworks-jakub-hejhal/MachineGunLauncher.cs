using OpenTK;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _087fireworks
{
  public class MachineGunLauncher : Launcher
  {

    bool actionInProgress = false;
    int n;
    double currentAngle;
    double angle;
    double lastShot;
    double delay = 0.1;
    bool twoSided;


    public MachineGunLauncher(bool twoSided, int n, double angle, ParticleFactory pFactory, double freq, Vector3d? pos = null, Vector3d? _aim = null, Vector3d? _up = null) : base(pFactory, freq, pos, _aim, _up)
    {
      this.twoSided = twoSided;
      this.n = n;
      this.angle = angle;
    }

    private Vector3 ToVector3(Vector3d v)
    {
      return new Vector3((float)v.X, (float)v.Y, (float)v.Z);
    }

    public override bool Simulate (double time, Fireworks fw)
    {
      if (time <= simTime)
        return true;

      double dt = time - simTime;
      // generate new particles for the [simTime-time] interval:

      if (actionInProgress)
      {
        if (time - lastShot < delay)
          return true;

        lastShot = time;

        if (currentAngle >= angle)
          actionInProgress = false;


        Shoot(time, fw, aim);
        if(twoSided)
        {
          var projection = new Vector3d(aim.X, 0, aim.Z);
          var left = Vector3d.Cross(projection, aim).Normalized();
          var rotAngle = Math.Acos(Vector3d.Dot(new Vector3d(0, 1, 0), aim.Normalized()));
          Matrix4d.CreateFromAxisAngle(left, 2*rotAngle, out Matrix4d rotMatrix);
          var currentAim = Vector3d.Transform(aim, rotMatrix);

          Shoot(time, fw, currentAim, true);

        }

        var step = 2*angle / n;
        currentAngle += step;


      }
      else
      {
        double probability = dt * frequency;
        if (probability > 1.0 ||
               rnd.UniformNumber() < probability)
        {
          actionInProgress = true;
          currentAngle = -angle;
          lastShot = time;
        }
      }

      simTime = time;

      return true;
    }

    private void Shoot(double time, Fireworks fw, Vector3d aim1, bool reverse = false)
    {
      Vector3d axis;
      if (Vector3d.Dot(aim1, new Vector3d(0, 1, 0)) > 0.99)
        axis = new Vector3d(1, 0, 0);
      else
      {
        var projection = new Vector3d(aim1.X, 0, aim1.Z);
        axis = projection.Normalized();
      }


      Matrix4d.CreateFromAxisAngle(axis, (reverse ? -1 : 1) * currentAngle, out Matrix4d rotMatrix);
      var currentAim = Vector3d.Transform(aim1, rotMatrix);

      Particle p = pFactory.Create(position, currentAim, up, time);
      fw.AddParticle(p);
    }
  }
}
