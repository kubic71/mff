using MathSupport;
using OpenTK;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _087fireworks
{
  public class Shell : CometParticle
  {
    public double shellFreq = 100;
    public double shellVariance = 0.03;
    public int leafs = 30;
    public double shellSize;
    public double secondaryExtinctionRate = 0.5;
    public Vector3 shellColor;


    public Shell (Vector3d pos, Vector3d vel, Vector3d _up, Vector3 col, double shellSize, double time) : base(pos, vel, _up, new Vector3(255, 255, 220), 4, time, 150, 0.03, 0.7)
    {
      shellColor = col;
      this.shellSize = shellSize;
    }


    Vector3d GetRandomSpherePoint () => new Vector3d((float)Fireworks.rnd.Normal(0.0, 1), (float)Fireworks.rnd.Normal(0.0, 1), (float)Fireworks.rnd.Normal(0.0, 1)).Normalized();

    public override bool Simulate (double time, Fireworks fw)
    {
      base.Simulate(time, fw);

      // if reached the top, explode
      if (velocity.Y < 0.1)
      {
        for(int i = 0; i < leafs; i ++)
        {
          var velocity = GetRandomSpherePoint() * (Fireworks.rnd.RandomDouble(0.8, 1) * shellSize);

          CometParticle p = new CometParticle(position, velocity, up, shellColor, shellSize*2, time, shellFreq, shellVariance, secondaryExtinctionRate);
          fw.AddParticle(p);
        }

        return false;
      }
      return true;
    }
  }
}
