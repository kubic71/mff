using OpenTK;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _087fireworks
{


  // used primarily by Launcher to create instances of shooted particles/rockets/exploding objects
  public abstract class ParticleFactory
  {
    protected Vector3? color;
    protected double randomColorState = 0;

    protected virtual Vector3 GetActualColor(double updateStep=50) { 
      if (color == null)
      {
        randomColorState += Fireworks.rnd.RandomDouble(0.5, 1)*updateStep;
        return Fireworks.RandomColor(randomColorState);
      } else
      {
        return color.Value;
      }
    }


    // caled from Launcher.Simulate
    public abstract Particle Create (Vector3d pos, Vector3d vel, Vector3d _up, double time);
    

  }

  class BasicParticleFactory : ParticleFactory
  {
    double extinctionRate = 0.9;
    Vector3 color = new Vector3(1f, 0.45f, 0.6f);
    double size = 1;
   

    public override Particle Create (Vector3d pos, Vector3d vel, Vector3d _up, double time)
    {
      
      return new BasicParticle(pos, vel, _up, color, size, time, extinctionRate);
    }
  }

  class CometParticleFactory : ParticleFactory
  {
    double frequency;
    double variance;
    double extinctionRate=0.9;
    double size;

    public CometParticleFactory(Vector3? color, double size, double frequency, double variance, double extinctionRate)
    {
      this.color = color;
      this.size = size;
      this.frequency = frequency;
      this.variance = variance;
      this.extinctionRate = extinctionRate;
    }



    protected override Vector3 GetActualColor (double updateStep = 2)
    {
      if (color == null)
      {
        randomColorState += Fireworks.rnd.RandomDouble(0.5, 1) * updateStep;
        return Fireworks.RandomColor(randomColorState, 0.4, 0.6);
      }
      else
      {
        return color.Value;
      }
    }

    public override Particle Create (Vector3d pos, Vector3d vel, Vector3d _up, double time)
    {
      return new CometParticle(pos, vel, _up, GetActualColor(), size, time, frequency, variance, extinctionRate);
    }
  }


  class ShellFactory : ParticleFactory
  {
    double shellSize;

    double shellFreq = 100;
    double shellVariance = 0.03;
    int leafs = 30;
    double secondaryExtinctionRate = 0.5;

    public ShellFactory (Vector3? color, double shellSize)
    {
      this.color = color;
      this.shellSize = shellSize;
    }

    
    public ShellFactory(Vector3? color, double shellSize, double secondaryExtinctionRate, double shellFreq, double shellVariance, int leafs):this(color, shellSize) 
    {
      // advanced options
      this.shellSize = shellSize;
      this.secondaryExtinctionRate = secondaryExtinctionRate;
      this.shellVariance = shellVariance;
      this.leafs = leafs;
      this.shellFreq = shellFreq;
         
    }

    public override Particle Create (Vector3d pos, Vector3d vel, Vector3d _up, double time)
    {

      

      Shell shell = new Shell(pos, vel, _up, GetActualColor(), shellSize, time);
      shell.shellVariance = shellVariance;
      shell.shellFreq = shellFreq;
      shell.leafs = leafs;
      shell.secondaryExtinctionRate = secondaryExtinctionRate;

      return shell;
    }
  }




}
