using OpenTK;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _087fireworks
{
  public static class Physics
  {

    const double LinearCoeff = 1;
    const double QuadraticCoeff = 0;


    const double Gravity = 0.3;
    public static Vector3d GravityVector { get; } = new Vector3d(0, -1, 0);

    // updates position and velocity of an object according to laws of physics (air resistance, gravity)
    public static void Update(Vector3d position, Vector3d velocity, double size, double dt, out Vector3d newPosition, out  Vector3d newVelocity)
    {
      // velocity after dt=1
      var velocity2 = ApplyGravity(velocity, dt);
      newVelocity = ApplyAirResistance(velocity2, size, dt);
      newPosition = position + newVelocity * dt;
    }

    // assume unit dt
    public static void Update (Vector3d position, Vector3d velocity, double size, out Vector3d newPosition, out Vector3d newVelocity)
    {
      Update(position, velocity, size, 1, out newPosition, out newVelocity);
    }




    public static Vector3d ApplyAirResistance(Vector3d velocity, double size, double dt)
    {
      var v = velocity.Length;
      var accel = LinearCoeff * v / Math.Pow(size, 1.5) + QuadraticCoeff * v*v / size;
      return velocity - accel * velocity * dt;
    }

    public static Vector3d ApplyGravity (Vector3d velocity, double dt)
    {
      return velocity + GravityVector * Gravity * dt;
    }
  }
}
